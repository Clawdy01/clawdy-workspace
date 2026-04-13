#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from workspace_secrets import get_secret, load_mail_config

ROOT = Path('/home/clawdy/.openclaw/workspace')
HUMAN_VERIFY = ROOT / 'browser-automation' / 'proton_human_verification.js'
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
    value = get_secret('proton.password')
    return value or None


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
    mailbox_address = args.email or load_mailbox_address()
    if not mailbox_address:
        return {
            'ok': False,
            'reason': 'missing-mailbox-address',
            'username': args.username,
        }

    password = load_password(args.password)
    if not password:
        return {
            'ok': False,
            'reason': 'missing-password',
            'username': args.username,
            'mailbox_address': mailbox_address,
        }

    cmd = [
        'node', str(HUMAN_VERIFY), args.username, password,
        '--email', mailbox_address, '--send',
    ]
    result = run_capture(cmd)
    parsed = result.get('parsed') or {}
    final = parsed.get('final') or {}
    summary = {
        'ok': result.get('returncode') == 0,
        'reason': 'requested' if result.get('returncode') == 0 else 'automation-failed',
        'username': args.username,
        'mailbox_address': mailbox_address,
        'returncode': result.get('returncode'),
        'verification_screen': final.get('verificationScreen'),
        'dialog_text': (final.get('dialogText') or '')[:500],
        'button_texts': [row.get('text') for row in (final.get('buttons') or []) if row.get('text')],
        'email_action': parsed.get('emailAction'),
        'screenshot': parsed.get('screenshot'),
        'stderr': result.get('stderr'),
    }
    return summary


def render_text(summary):
    if not summary.get('ok'):
        if summary.get('reason') == 'missing-mailbox-address':
            return 'Proton request code: mailboxadres ontbreekt'
        if summary.get('reason') == 'missing-password':
            return 'Proton request code: opgeslagen Proton-wachtwoord ontbreekt'
        return f"Proton request code: mislukt ({summary.get('reason')})"

    return '\n'.join([
        'Proton request code',
        f"- username={summary.get('username')}, mailbox={summary.get('mailbox_address')}",
        f"- verification_screen={summary.get('verification_screen')}, buttons={', '.join(summary.get('button_texts') or []) or 'geen'}",
    ])


def main():
    parser = argparse.ArgumentParser(description='Vraag automatisch een Proton verificatiecode aan voor de huidige human-verification flow')
    parser.add_argument('username', nargs='?', default=DEFAULT_USERNAME)
    parser.add_argument('password', nargs='?')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--email', help='optioneel mailboxadres om in te vullen in plaats van state/mail-config.json')
    args = parser.parse_args()

    summary = build_summary(args)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))
    raise SystemExit(0 if summary.get('ok') else 2)


if __name__ == '__main__':
    main()
