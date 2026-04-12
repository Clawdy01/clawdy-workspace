#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys

from secrets import get_secret, load_mail_config
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
MAIL_CODES = ROOT / 'scripts' / 'mail-verification-codes.py'
EXTERNAL_FINISH = ROOT / 'browser-automation' / 'proton_external_finish_with_code.js'
STATE = ROOT / 'state'
DEFAULT_USERNAME = 'clawdy01'


def load_mailbox_address():
    try:
        data = load_mail_config()
    except Exception:
        return None
    return data.get('username') or None


def load_password(explicit_password=None):
    if explicit_password:
        return explicit_password
    value = get_secret('proton_pass_password')
    return value or None


def run_json(cmd, timeout=60, default=None):
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


def latest_code(limit=20, sender='proton'):
    rows = run_json([
        'python3', str(MAIL_CODES), '--json', '--sender', sender, '-n', str(limit)
    ], default=[])
    if not isinstance(rows, list):
        return None, []
    for row in rows:
        codes = row.get('codes') or []
        if codes:
            return {
                'uid': row.get('uid'),
                'from': row.get('from'),
                'subject': row.get('subject'),
                'date': row.get('date'),
                'code': str(codes[0]),
                'all_codes': codes,
            }, rows
    return None, rows


def run_capture(cmd, timeout=180):
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    parsed = None
    try:
        parsed = json.loads(proc.stdout)
    except Exception:
        parsed = None
    return {
        'command': cmd,
        'returncode': proc.returncode,
        'stdout': (proc.stdout or '').strip(),
        'stderr': (proc.stderr or '').strip(),
        'parsed': parsed,
    }


def build_summary(args):
    code_row, scanned = latest_code(limit=args.limit, sender=args.sender)
    if not code_row:
        return {
            'ok': False,
            'reason': 'no-code-found',
            'username': args.username,
            'mailbox_address': load_mailbox_address(),
            'scanned_messages': len(scanned),
        }

    password = load_password(args.password)
    if not password:
        return {
            'ok': False,
            'reason': 'missing-password',
            'username': args.username,
            'mailbox_address': load_mailbox_address(),
            'code_source': code_row,
        }

    mailbox_address = args.email or load_mailbox_address()
    if not mailbox_address:
        return {
            'ok': False,
            'reason': 'missing-mailbox-address',
            'username': args.username,
            'code_source': code_row,
        }

    cmd = [
        'node', str(EXTERNAL_FINISH), mailbox_address, password,
    ]

    result = run_capture(cmd)
    parsed = result.get('parsed') or {}
    flow_result = parsed.get('result') or {}
    summary = {
        'ok': result.get('returncode') == 0,
        'reason': 'verified' if result.get('returncode') == 0 else 'automation-failed',
        'username': args.username,
        'mailbox_address': mailbox_address,
        'code_source': code_row,
        'send_requested': bool(args.send),
        'verify_requested': True,
        'flow_mode': 'external-email-finish',
        'returncode': result.get('returncode'),
        'verification_screen': 'verification' in (flow_result.get('text') or '').lower(),
        'dialog_text': (flow_result.get('text') or '')[:500],
        'button_texts': [],
        'code_action': parsed.get('fillResult'),
        'used_code': parsed.get('fetchedCode'),
        'retry_code': parsed.get('retryCode'),
        'final_start_visible': parsed.get('finalStartVisible'),
        'final_start_disabled': parsed.get('finalStartDisabled'),
        'screenshot': parsed.get('screenshot'),
        'stderr': result.get('stderr'),
    }
    return summary


def render_text(summary):
    if not summary.get('ok'):
        if summary.get('reason') == 'no-code-found':
            return f"Proton use code: geen verificatiecode gevonden in recente Proton-mail ({summary.get('scanned_messages', 0)} berichten gescand)"
        if summary.get('reason') == 'missing-password':
            return 'Proton use code: opgeslagen Proton-wachtwoord ontbreekt'
        if summary.get('reason') == 'missing-mailbox-address':
            return 'Proton use code: mailboxadres ontbreekt'
        return f"Proton use code: mislukt ({summary.get('reason')})"

    source = summary.get('code_source') or {}
    return '\n'.join([
        'Proton use code',
        f"- username={summary.get('username')}, mailbox={summary.get('mailbox_address') or 'onbekend'}, flow={summary.get('flow_mode')}",
        f"- code uit mail #{source.get('uid')}: {source.get('subject')} [{source.get('code')}]",
        f"- gebruikte code={summary.get('used_code')}, retry={summary.get('retry_code') or 'geen'}, verify_field={summary.get('code_action')}",
        f"- verification_screen={summary.get('verification_screen')}, final_start_visible={summary.get('final_start_visible')}, final_start_disabled={summary.get('final_start_disabled')}",
    ])


def main():
    parser = argparse.ArgumentParser(description='Gebruik automatisch de nieuwste Proton verificatiecode in de Human Verification-flow')
    parser.add_argument('username', nargs='?', default=DEFAULT_USERNAME)
    parser.add_argument('password', nargs='?')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--sender', default='proton')
    parser.add_argument('-n', '--limit', type=int, default=20)
    parser.add_argument('--email', help='optioneel emailadres om tegelijk opnieuw in te vullen')
    parser.add_argument('--send', action='store_true', help='klik ook eerst op Get verification code (optioneel, alleen samen met --email zinvol)')
    args = parser.parse_args()

    summary = build_summary(args)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))
    raise SystemExit(0 if summary.get('ok') else 2)


if __name__ == '__main__':
    main()
