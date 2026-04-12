#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
OUT = ROOT / 'browser-automation' / 'out'
BROWSER = ROOT / 'browser-automation'

PROBES = [
    {
        'name': 'visible-inputs',
        'command': ['node', str(BROWSER / 'proton_probe_visible_inputs.js')],
        'artifact': OUT / 'proton-visible-inputs.json',
        'timeout': 90,
    },
    {
        'name': 'input-proxy',
        'command': ['node', str(BROWSER / 'proton_probe_input_proxy.js')],
        'artifact': OUT / 'proton-input-proxy.json',
        'timeout': 90,
    },
    {
        'name': 'to-password-step',
        'command': ['node', str(BROWSER / 'proton_to_password_step.js')],
        'artifact': OUT / 'proton-to-password-step.json',
        'timeout': 120,
    },
    {
        'name': 'password-step',
        'command': ['node', str(BROWSER / 'proton_probe_password_step.js')],
        'artifact': OUT / 'proton-password-step.json',
        'timeout': 120,
    },
]


def load_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def iso_age_seconds(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except Exception:
        return None
    return max(0, int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()))


def run_probe(spec):
    try:
        proc = subprocess.run(
            spec['command'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=spec['timeout'],
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = exc
        timed_out = True
    return {
        'name': spec['name'],
        'command': spec['command'],
        'returncode': 124 if timed_out else proc.returncode,
        'ok': (not timed_out) and proc.returncode == 0,
        'timed_out': timed_out,
        'stdout': (getattr(proc, 'stdout', '') or '').strip(),
        'stderr': (getattr(proc, 'stderr', '') or '').strip(),
        'artifact': str(spec['artifact']),
    }


def maybe_refresh(enabled):
    if not enabled:
        return []
    return [run_probe(spec) for spec in PROBES]


def pick_button_texts(rows, limit=5):
    texts = []
    for item in rows or []:
        text = ' '.join((item.get('text') or '').split())
        if not text:
            continue
        if item.get('tag') == 'button' or any(word in text.lower() for word in ['create free account', 'get started', 'use your current email']):
            if text not in texts:
                texts.append(text)
        if len(texts) >= limit:
            break
    return texts


def build_report():
    visible = load_json(OUT / 'proton-visible-inputs.json', {}) or {}
    proxy = load_json(OUT / 'proton-input-proxy.json', {}) or {}
    to_password = load_json(OUT / 'proton-to-password-step.json', {}) or {}
    password = load_json(OUT / 'proton-password-step.json', {}) or {}

    visible_age = iso_age_seconds(visible.get('checkedAt'))
    proxy_age = iso_age_seconds(proxy.get('checkedAt'))
    route_age = iso_age_seconds(to_password.get('checkedAt'))
    password_age = iso_age_seconds(password.get('checkedAt'))

    visible_buttons = pick_button_texts(visible.get('data') or [])
    proxy_buttons = pick_button_texts(proxy.get('candidates') or [])
    password_buttons = pick_button_texts(password.get('interesting') or [])

    iframe_titles = [item.get('title') for item in (proxy.get('iframes') or []) if item.get('title')]
    iframe_srcs = [item.get('src') for item in (proxy.get('iframes') or []) if item.get('src')]
    username_proxy_visible = any(item.get('id') == 'username' and item.get('visible') for item in (proxy.get('candidates') or []))
    username_chain_hidden = any(item.get('id') == 'username' and not item.get('visible') for item in (proxy.get('usernameChain') or []))
    propagated_value = ((to_password.get('propagated') or {}).get('value') or '').strip()
    excerpt = (to_password.get('excerpt') or '').strip()
    password_ids = [item.get('id') for item in (password.get('passwordInputs') or []) if item.get('id')]

    findings = []
    if propagated_value:
        findings.append('username-propagatie werkt nog')
    if iframe_titles:
        findings.append(f"e-mailinvoer zit achter iframe(s): {', '.join(iframe_titles[:3])}")
    if username_chain_hidden and not username_proxy_visible:
        findings.append('verborgen username-proxy blijft aanwezig op de startpagina')
    if not to_password.get('reachedPasswordStep'):
        findings.append('na submit blijft de flow op de startpagina hangen')
    if any(pid in {'password', 'password-confirm'} for pid in password_ids):
        findings.append('losse password-step probe ziet nog wel passwordvelden')

    diagnosis = 'geen duidelijke regressie-signalen'
    if propagated_value and not to_password.get('reachedPasswordStep') and any(pid in {'password', 'password-confirm'} for pid in password_ids):
        diagnosis = 'waarschijnlijke transition/selectorrace: startflow klikt door, maar de gecombineerde route landt niet stabiel op de password-step'
    elif propagated_value and not to_password.get('reachedPasswordStep'):
        diagnosis = 'waarschijnlijke Proton-flow regressie of selectorverandering tussen username-submit en password-step'

    return {
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'ages': {
            'visible_inputs_seconds': visible_age,
            'input_proxy_seconds': proxy_age,
            'to_password_seconds': route_age,
            'password_step_seconds': password_age,
        },
        'route_state': {
            'username': to_password.get('username'),
            'propagated_value': propagated_value,
            'reached_password_step': to_password.get('reachedPasswordStep'),
            'password_visible': to_password.get('passwordVisible'),
            'password_confirm_visible': to_password.get('passwordConfirmVisible'),
            'get_started_visible': to_password.get('getStartedVisible'),
            'url': to_password.get('url'),
        },
        'ui_signals': {
            'visible_buttons': visible_buttons,
            'proxy_buttons': proxy_buttons,
            'password_buttons': password_buttons,
            'iframe_titles': iframe_titles,
            'iframe_src_hosts': [src.split('/')[2] for src in iframe_srcs[:5] if '://' in src],
            'username_proxy_visible': username_proxy_visible,
            'username_chain_hidden': username_chain_hidden,
            'password_ids': password_ids,
            'password_probe_active_id': password.get('activeId'),
        },
        'excerpt': excerpt[:500],
        'findings': findings,
        'diagnosis': diagnosis,
        'recommended_next_action': 'stabilize-password-transition' if 'transition/selectorrace' in diagnosis else 'refresh-or-adjust-selectors',
        'artifacts': {
            'visible_inputs': str(OUT / 'proton-visible-inputs.json'),
            'input_proxy': str(OUT / 'proton-input-proxy.json'),
            'to_password': str(OUT / 'proton-to-password-step.json'),
            'password_step': str(OUT / 'proton-password-step.json'),
        },
    }


def render_text(report, refresh_results):
    lines = ['Proton password regression report']
    lines.append(f"- diagnose={report.get('diagnosis')}")
    route = report.get('route_state') or {}
    lines.append(
        f"- route: propagated={route.get('propagated_value')}, reached_password_step={route.get('reached_password_step')}, password_visible={route.get('password_visible')}, get_started_visible={route.get('get_started_visible')}"
    )
    ui = report.get('ui_signals') or {}
    if ui.get('iframe_titles'):
        lines.append(f"- iframes={', '.join(ui.get('iframe_titles')[:3])}")
    buttons = ui.get('visible_buttons') or ui.get('password_buttons') or ui.get('proxy_buttons') or []
    if buttons:
        lines.append(f"- buttons={'; '.join(buttons[:4])}")
    if report.get('findings'):
        lines.append(f"- findings={'; '.join(report.get('findings')[:4])}")
    lines.append(f"- next={report.get('recommended_next_action')}")
    if refresh_results:
        ok = sum(1 for item in refresh_results if item.get('ok'))
        fail = sum(1 for item in refresh_results if not item.get('ok'))
        lines.append(f"- refreshed={len(refresh_results)}, ok={ok}, fail={fail}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Diagnoseer Proton password-step regressies met compacte probe-samenvatting')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--refresh', action='store_true', help='ververs eerst de relevante Proton regression probes')
    args = parser.parse_args()

    refresh_results = maybe_refresh(args.refresh)
    report = build_report()
    payload = {
        'refresh_results': refresh_results,
        'report': report,
        'ok': all(item.get('ok') for item in refresh_results) if refresh_results else True,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(report, refresh_results))

    raise SystemExit(0 if payload['ok'] else 1)


if __name__ == '__main__':
    main()
