#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from workspace_secrets import get_secret, load_mail_config

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATE = ROOT / 'state'
EXTERNAL_FINISH = ROOT / 'browser-automation' / 'proton_external_finish_with_code.js'
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


def run_capture(cmd, timeout=240):
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
    password = load_password(args.password)
    if not password:
        return {
            'ok': False,
            'reason': 'missing-password',
            'username': args.username,
            'mailbox_address': load_mailbox_address(),
        }

    mailbox_address = args.email or load_mailbox_address()
    if not mailbox_address:
        return {
            'ok': False,
            'reason': 'missing-mailbox-address',
            'username': args.username,
        }

    result = run_capture(['node', str(EXTERNAL_FINISH), mailbox_address, password])
    parsed = result.get('parsed') or {}
    flow_result = parsed.get('result') or {}
    text = (flow_result.get('text') or '').lower()
    signals = set(flow_result.get('interestingSignals') or [])
    summary = {
        'ok': result.get('returncode') == 0,
        'reason': 'continued' if result.get('returncode') == 0 else 'automation-failed',
        'username': args.username,
        'mailbox_address': mailbox_address,
        'flow_mode': 'external-email-finish',
        'returncode': result.get('returncode'),
        'used_code': parsed.get('fetchedCode'),
        'retry_code': parsed.get('retryCode'),
        'verify_button_visible': parsed.get('verifyButtonVisible'),
        'final_start_visible': parsed.get('finalStartVisible'),
        'final_start_disabled': parsed.get('finalStartDisabled'),
        'recovery_kit_ready': ('recovery' in text and 'kit' in text) or ('recovery' in signals),
        'account_created': ('account' in signals and 'recovery' in text and 'kit' in text),
        'dialog_text': (flow_result.get('text') or '')[:500],
        'screenshot': parsed.get('screenshot'),
        'stderr': result.get('stderr'),
    }
    if summary['recovery_kit_ready']:
        summary['next_state'] = 'recovery-kit'
    elif summary['final_start_visible']:
        summary['next_state'] = 'password-setup'
    else:
        summary['next_state'] = 'unknown'
    return summary


def render_text(summary):
    if not summary.get('ok'):
        if summary.get('reason') == 'missing-password':
            return 'Proton continue password setup: opgeslagen Proton-wachtwoord ontbreekt'
        if summary.get('reason') == 'missing-mailbox-address':
            return 'Proton continue password setup: mailboxadres ontbreekt'
        return f"Proton continue password setup: mislukt ({summary.get('reason')})"

    return '\n'.join([
        'Proton continue password setup',
        f"- username={summary.get('username')}, mailbox={summary.get('mailbox_address') or 'onbekend'}, flow={summary.get('flow_mode')}",
        f"- gebruikte code={summary.get('used_code')}, retry={summary.get('retry_code') or 'geen'}, verify_button_visible={summary.get('verify_button_visible')}",
        f"- final_start_visible={summary.get('final_start_visible')}, final_start_disabled={summary.get('final_start_disabled')}, recovery_kit_ready={summary.get('recovery_kit_ready')}",
        f"- next_state={summary.get('next_state')}",
    ])


def main():
    parser = argparse.ArgumentParser(description='Trek de Proton signup-flow veilig verder vanaf de password-setup / external-email finish route')
    parser.add_argument('username', nargs='?', default=DEFAULT_USERNAME)
    parser.add_argument('password', nargs='?')
    parser.add_argument('--email', help='optioneel mailboxadres om te gebruiken')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    summary = build_summary(args)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))
    raise SystemExit(0 if summary.get('ok') else 2)


if __name__ == '__main__':
    main()
