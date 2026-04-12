#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
OUT = ROOT / 'browser-automation' / 'out'
VERIFY = ROOT / 'scripts' / 'proton-verification-status.py'


def load_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def run_json(cmd, default=None, timeout=12):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def build_summary():
    start = load_json(OUT / 'proton-status.json', {}) or {}
    to_password = load_json(OUT / 'proton-to-password-step.json', {}) or {}
    password = load_json(OUT / 'proton-password-step.json', {}) or {}
    submit_ready = load_json(OUT / 'proton-to-submit-ready.json', {}) or {}

    strength_levels = []
    for text in (submit_ready.get('strengthTexts') or []):
        lowered = text.lower()
        for level in ['vulnerable', 'weak', 'medium', 'strong']:
            if level in lowered and level not in strength_levels:
                strength_levels.append(level)

    verify = run_json(['python3', str(VERIFY), '--json'], default={}) or {}
    manual_boundary = bool(verify.get('account_created')) or bool(verify.get('recovery_kit_ready'))

    summary = {
        'start': {
            'checked_at': start.get('checkedAt'),
            'signup_visible': (start.get('flags') or {}).get('signupVisible'),
            'captcha_likely': (start.get('flags') or {}).get('captchaLikely'),
            'blocked': (start.get('flags') or {}).get('blocked'),
        },
        'route': {
            'checked_at': to_password.get('checkedAt'),
            'username': to_password.get('username'),
            'propagated_value': (to_password.get('propagated') or {}).get('value'),
            'reached_password_step': to_password.get('reachedPasswordStep'),
            'password_visible': to_password.get('passwordVisible'),
            'password_confirm_visible': to_password.get('passwordConfirmVisible'),
            'get_started_visible': to_password.get('getStartedVisible'),
        },
        'password_step': {
            'checked_at': password.get('checkedAt'),
            'active_id': password.get('activeId'),
            'username_value_length': next((x.get('valueLength') for x in (password.get('passwordInputs') or []) if x.get('id') == 'username'), None),
            'password_ids': [x.get('id') for x in (password.get('passwordInputs') or []) if x.get('id') in {'password', 'password-confirm'}],
        },
        'submit_ready': {
            'checked_at': submit_ready.get('checkedAt'),
            'submit_ready': submit_ready.get('submitReady'),
            'submit_disabled': submit_ready.get('submitDisabled'),
            'password_length': submit_ready.get('passwordLength'),
            'strength_signals': strength_levels,
        },
        'manual_boundary': manual_boundary,
        'account_created': bool(verify.get('account_created')),
        'recovery_kit_ready': bool(verify.get('recovery_kit_ready')),
        'verification_source': verify.get('source'),
    }
    summary['regression_suspected'] = False if manual_boundary else bool(
        summary['start'].get('signup_visible')
        and summary['route'].get('propagated_value')
        and not summary['route'].get('reached_password_step')
    )
    return summary


def render_text(summary):
    lines = ['Proton status']
    start = summary['start']
    route = summary['route']
    pw = summary['password_step']
    submit_ready = summary['submit_ready']
    lines.append(f"- start: signup zichtbaar={start.get('signup_visible')}, captcha={start.get('captcha_likely')}, blocked={start.get('blocked')}")
    lines.append(
        f"- route: password-step={route.get('reached_password_step')}, username={route.get('username')}, propagated={route.get('propagated_value')}"
    )
    lines.append(
        f"- password: velden={','.join(pw.get('password_ids') or []) or 'geen'}, actieve focus={pw.get('active_id')}, username-len={pw.get('username_value_length')}"
    )
    strength = ', '.join(submit_ready.get('strength_signals') or []) or 'geen'
    lines.append(
        f"- submit: ready={submit_ready.get('submit_ready')}, disabled={submit_ready.get('submit_disabled')}, pw-len={submit_ready.get('password_length')}, strength={strength}"
    )
    lines.append(f"- regressie-verdenking: {summary.get('regression_suspected')}")
    if summary.get('manual_boundary'):
        lines.append(
            f"- manual-boundary: account_created={summary.get('account_created')}, recovery_kit={summary.get('recovery_kit_ready')}, source={summary.get('verification_source')}"
        )
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte Proton signup status uit probe-output')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    summary = build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
