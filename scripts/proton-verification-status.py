#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
OUT = ROOT / 'browser-automation' / 'out'
STATE = ROOT / 'state'
CACHE = STATE / 'proton-verification-status.json'
CACHE_MAX_AGE = 300
CACHE_DEPENDENCIES = [
    OUT / 'proton-submit-probe.json',
    OUT / 'proton-human-verification.json',
    OUT / 'proton-request-verification-code.json',
    OUT / 'proton-external-finish-with-code.json',
    OUT / 'proton-finish-signup-with-code.json',
]


def load_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def newer_dependency_exists(cached_at):
    cached_dt = iso_parse(cached_at)
    if not cached_dt:
        return True
    for path in CACHE_DEPENDENCIES:
        try:
            if datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc) > cached_dt:
                return True
        except Exception:
            continue
    return False



def load_cache(max_age=CACHE_MAX_AGE):
    data = load_json(CACHE)
    if not isinstance(data, dict):
        return None
    cached_at = data.get('_cached_at')
    age = iso_age_seconds(cached_at)
    if max_age is not None and (age is None or age > max_age):
        return None
    if newer_dependency_exists(cached_at):
        return None
    data.pop('_cached_at', None)
    data['cache_age_seconds'] = age
    data.setdefault('email_request_sent', False)
    return data


def save_cache(summary):
    STATE.mkdir(parents=True, exist_ok=True)
    payload = dict(summary)
    payload['_cached_at'] = datetime.now(timezone.utc).isoformat()
    CACHE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def run_json(command, default=None, timeout=12):
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def refresh_probe(do_submit=False):
    cmd = ['node', str(ROOT / 'browser-automation' / 'proton_submit_probe.js'), 'clawdy01']
    if do_submit:
        cmd.append('--submit')
    try:
        subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=90)
    except subprocess.TimeoutExpired:
        pass


def auto_advance(max_steps=2):
    actions = []
    for _ in range(max_steps):
        current = build_summary(use_cache=False)
        action = current.get('recommended_action')
        if action == 'refresh':
            refresh_probe(do_submit=False)
            actions.append('refresh')
            continue
        if action == 'refresh-submit':
            refresh_probe(do_submit=True)
            actions.append('refresh-submit')
            continue
        break
    summary = build_summary()
    summary['auto_actions'] = actions
    return summary


def iso_parse(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except Exception:
        return None



def iso_age_seconds(value):
    dt = iso_parse(value)
    if not dt:
        return None
    return max(0, int((datetime.now(timezone.utc) - dt).total_seconds()))


def date_age_seconds(value):
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except Exception:
        return None
    return max(0, int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()))



def file_iso_or_mtime(path):
    data = load_json(path, {}) or {}
    checked_at = data.get('checkedAt')
    if checked_at:
        return checked_at, data
    try:
        checked_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
    except Exception:
        checked_at = None
    return checked_at, data



def build_summary(use_cache=True):
    if use_cache:
        cached = load_cache()
        if cached:
            return cached

    probe = load_json(OUT / 'proton-submit-probe.json', {}) or {}
    human = load_json(OUT / 'proton-human-verification.json', {}) or {}
    request_checked_at, request = file_iso_or_mtime(OUT / 'proton-request-verification-code.json')
    finish_checked_at, finish = file_iso_or_mtime(OUT / 'proton-external-finish-with-code.json')
    legacy_finish_checked_at, legacy_finish = file_iso_or_mtime(OUT / 'proton-finish-signup-with-code.json')
    post = probe.get('post') or {}
    human_final = human.get('final') or {}
    request_post = request.get('postRequest') or {}
    finish_result = finish.get('result') or {}
    legacy_finish_result = legacy_finish.get('result') or {}
    probe_text = (post.get('text') or '').lower()
    human_text = (human_final.get('dialogText') or '').lower()
    request_text = (request_post.get('text') or '').lower()
    finish_text = (finish_result.get('text') or '').lower()
    legacy_finish_text = (legacy_finish_result.get('text') or '').lower()
    combined_text = ' '.join(part for part in [probe_text, human_text, request_text, finish_text, legacy_finish_text] if part).strip()
    codes = run_json([
        'python3', str(ROOT / 'scripts' / 'mail-verification-codes.py'),
        '--json', '--sender', 'proton', '-n', '20'
    ], default=[]) or []

    probe_age_seconds = iso_age_seconds(probe.get('checkedAt'))
    human_age_seconds = iso_age_seconds(human.get('checkedAt'))
    request_age_seconds = iso_age_seconds(request_checked_at)
    finish_age_seconds = iso_age_seconds(finish_checked_at)
    legacy_finish_age_seconds = iso_age_seconds(legacy_finish_checked_at)
    probe_stale = probe_age_seconds is None or probe_age_seconds > 900
    human_stale = human_age_seconds is None or human_age_seconds > 900
    request_stale = request_age_seconds is None or request_age_seconds > 900
    finish_stale = finish_age_seconds is None or finish_age_seconds > 900
    legacy_finish_stale = legacy_finish_age_seconds is None or legacy_finish_age_seconds > 900

    verification_screen = (
        ('human verification' in combined_text)
        or bool(human_final.get('verificationScreen'))
        or ('enter the verification code' in request_text)
    )
    verification_method_email = any(term in combined_text for term in ['email address', 'get verification code', 'verification code', 'resend code'])
    code_entry_ready = 'enter the verification code' in request_text or 'verification code' in request_text
    password_setup_ready = bool(finish.get('finalStartVisible')) and any(term in finish_text for term in ['set your password', 'get started'])
    recovery_kit_ready = any(
        term in text for text in [finish_text, legacy_finish_text]
        for term in ['save your recovery kit', 'download pdf proton-recovery-kit.pdf']
    )
    account_created = recovery_kit_ready or any(
        term in text for text in [finish_text, legacy_finish_text]
        for term in ['restore your proton account if you’re locked out', "restore your proton account if you're locked out"]
    )
    email_request_sent = bool(
        (human.get('emailProvided') and human.get('sendRequested') and human.get('emailAction'))
        or request.get('email_action')
        or code_entry_ready
    )

    legacy_finish_dt = iso_parse(legacy_finish_checked_at)
    finish_dt = iso_parse(finish_checked_at)
    account_created_active = bool(account_created)
    if account_created_active and password_setup_ready and finish_dt and legacy_finish_dt and finish_dt > legacy_finish_dt:
        account_created_active = False

    source = 'submit-probe'
    checked_at = probe.get('checkedAt')
    age_seconds = probe_age_seconds
    stale = probe_stale
    if account_created_active and legacy_finish_checked_at:
        source = 'finish-with-code'
        checked_at = legacy_finish_checked_at
        age_seconds = legacy_finish_age_seconds
        stale = legacy_finish_stale
    elif (account_created or password_setup_ready) and finish_checked_at:
        source = 'external-finish'
        checked_at = finish_checked_at
        age_seconds = finish_age_seconds
        stale = finish_stale
    elif verification_screen and code_entry_ready and not request_stale:
        source = 'request-code'
        checked_at = request_checked_at
        age_seconds = request_age_seconds
        stale = request_stale
    elif verification_screen and not human_stale:
        source = 'human-verification'
        checked_at = human.get('checkedAt') or checked_at
        age_seconds = human_age_seconds if human_age_seconds is not None else age_seconds
        stale = human_stale and probe_stale
    elif checked_at is None and human.get('checkedAt'):
        source = 'human-verification'
        checked_at = human.get('checkedAt')
        age_seconds = human_age_seconds
        stale = human_stale
    elif verification_screen and code_entry_ready and request_checked_at:
        source = 'request-code'
        checked_at = request_checked_at
        age_seconds = request_age_seconds
        stale = request_stale

    latest_code_age_seconds = None
    if codes:
        latest_code_age_seconds = date_age_seconds(codes[0].get('date'))

    recommended_action = 'noop'
    if account_created_active:
        recommended_action = 'account-created'
        stale = False
    elif password_setup_ready:
        recommended_action = 'password-setup-ready'
    elif verification_screen and codes and email_request_sent and latest_code_age_seconds is not None:
        if not stale or age_seconds is None or latest_code_age_seconds <= age_seconds + 600:
            recommended_action = 'use-code'
        else:
            recommended_action = 'refresh'
    elif stale:
        recommended_action = 'refresh'
    elif verification_screen and verification_method_email and not email_request_sent:
        recommended_action = 'request-code'
    elif verification_screen and not codes:
        recommended_action = 'wait-for-mail'
    elif probe.get('submitReady') and not probe.get('submitAttempted'):
        recommended_action = 'refresh-submit'

    signals = list(post.get('interestingSignals') or [])
    signals.extend(finish_result.get('interestingSignals') or [])
    signals.extend(legacy_finish_result.get('interestingSignals') or [])
    if human.get('emailProvided'):
        signals.append('email-provided')
    if human.get('codeProvided'):
        signals.append('code-provided')
    if finish.get('fetchedCode'):
        signals.append('code-used')
    if recovery_kit_ready:
        signals.append('recovery-kit-ready')
    if account_created:
        signals.append('account-created')
    if password_setup_ready:
        signals.append('password-setup-ready')
    signals = list(dict.fromkeys(signals))

    summary = {
        'checked_at': checked_at,
        'source': source,
        'age_seconds': age_seconds,
        'stale': stale,
        'submit_attempted': probe.get('submitAttempted'),
        'submit_ready': probe.get('submitReady'),
        'verification_screen': verification_screen,
        'verification_method_email': verification_method_email,
        'code_entry_ready': code_entry_ready,
        'signals': signals,
        'email_request_sent': email_request_sent,
        'verification_mail_matches': len(codes),
        'latest_code_age_seconds': latest_code_age_seconds,
        'latest_codes': codes[:3],
        'latest_used_code': finish.get('fetchedCode') or legacy_finish.get('fetchedCode'),
        'password_setup_ready': password_setup_ready,
        'recovery_kit_ready': recovery_kit_ready,
        'account_created': account_created_active,
        'account_created_seen': account_created,
        'recommended_action': recommended_action,
    }
    save_cache(summary)
    return summary


def render_text(summary):
    lines = ['Proton verification status']
    if summary.get('auto_actions'):
        lines.append(f"- auto_actions={','.join(summary.get('auto_actions') or [])}")
    lines.append(
        f"- source={summary.get('source')}, submit_attempted={summary.get('submit_attempted')}, submit_ready={summary.get('submit_ready')}, stale={summary.get('stale')}"
    )
    lines.append(
        f"- verification_screen={summary.get('verification_screen')}, email_method={summary.get('verification_method_email')}, code_entry_ready={summary.get('code_entry_ready')}, password_setup_ready={summary.get('password_setup_ready')}"
    )
    lines.append(
        f"- mail_matches={summary.get('verification_mail_matches')}, latest_code_age={summary.get('latest_code_age_seconds')}, email_requested={bool(summary.get('email_request_sent'))}, used_code={summary.get('latest_used_code')}, account_created_seen={summary.get('account_created_seen')}, signals={','.join(summary.get('signals') or []) or 'geen'}, next={summary.get('recommended_action')}"
    )
    for row in summary.get('latest_codes') or []:
        code_text = ', '.join(row.get('codes') or []) or 'geen code'
        lines.append(f"- mail #{row.get('uid')}: {row.get('subject')} [{code_text}]")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Combineer Proton verificatiestatus met mailbox-code lookup')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--refresh', action='store_true', help='ververs eerst de submit probe zonder echte submit')
    parser.add_argument('--refresh-submit', action='store_true', help='ververs eerst de submit probe met echte submit-attempt')
    parser.add_argument('--auto', action='store_true', help='voer automatisch de aanbevolen vervolgstap uit als dat veilig/logisch is')
    args = parser.parse_args()
    if args.refresh_submit:
        refresh_probe(do_submit=True)
        summary = build_summary(use_cache=False)
    elif args.refresh:
        refresh_probe(do_submit=False)
        summary = build_summary(use_cache=False)
    elif args.auto:
        summary = auto_advance()
    else:
        summary = build_summary(use_cache=True)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
