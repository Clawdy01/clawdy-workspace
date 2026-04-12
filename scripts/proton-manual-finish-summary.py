#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
VERIFY = ROOT / 'scripts' / 'proton-verification-status.py'
NEXT = ROOT / 'scripts' / 'proton-next-step.py'


def run_json(command, timeout=20, default=None):
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


def build_summary():
    verification = run_json(['python3', str(VERIFY), '--json'], default={}) or {}
    next_step = run_json(['python3', str(NEXT), '--json'], default={}) or {}

    latest_codes = verification.get('latest_codes') or []
    latest_code = latest_codes[0] if latest_codes else {}

    manual_boundary = bool(
        verification.get('account_created')
        or verification.get('account_created_seen')
        or verification.get('password_setup_ready')
        or next_step.get('recommended_route') == 'account-created'
    )

    checklist = []
    if verification.get('recovery_kit_ready'):
        checklist.append('sla de Recovery Kit bewust op op een veilige plek voordat je verder klikt')
    if verification.get('password_setup_ready'):
        checklist.append('rond het password-setup scherm handmatig af als dat nog zichtbaar is')
    if verification.get('account_created'):
        checklist.append('log daarna in op Proton met het nieuwe account en bevestig dat Pass beschikbaar is')
    if verification.get('latest_used_code'):
        checklist.append('markeer de laatst gebruikte verificatiecode als afgehandeld in je eigen notities')

    if not checklist:
        checklist.append('geen duidelijke manual-finish checklist beschikbaar; ververs eerst de Proton status')

    verification_stale = verification.get('stale')
    if manual_boundary and next_step.get('recommended_route') == 'account-created':
        verification_stale = False

    recommended_command = None
    if manual_boundary:
        recommended_command = 'python3 scripts/web-automation-dispatch.py proton-manual-finish'

    return {
        'manual_boundary': manual_boundary,
        'recommended_route': next_step.get('recommended_route'),
        'recommended_command': recommended_command,
        'reason': next_step.get('reason'),
        'verification_source': verification.get('source'),
        'verification_checked_at': verification.get('checked_at'),
        'verification_age_seconds': verification.get('age_seconds'),
        'verification_stale': verification_stale,
        'account_created': verification.get('account_created'),
        'account_created_seen': verification.get('account_created_seen'),
        'password_setup_ready': verification.get('password_setup_ready'),
        'recovery_kit_ready': verification.get('recovery_kit_ready'),
        'latest_used_code': verification.get('latest_used_code'),
        'verification_mail_matches': verification.get('verification_mail_matches'),
        'latest_code_age_seconds': verification.get('latest_code_age_seconds'),
        'latest_mail_subject': latest_code.get('subject'),
        'latest_mail_uid': latest_code.get('uid'),
        'checklist': checklist,
    }


def render_text(summary):
    lines = ['Proton manual finish']
    lines.append(
        f"- manual_boundary={summary.get('manual_boundary')}, route={summary.get('recommended_route')}, stale={summary.get('verification_stale')}"
    )
    lines.append(
        f"- evidence: source={summary.get('verification_source')}, age={summary.get('verification_age_seconds')}s, checked_at={summary.get('verification_checked_at')}"
    )
    if summary.get('recommended_command'):
        lines.append(f"- command={summary.get('recommended_command')}")
    lines.append(
        f"- account_created={summary.get('account_created')}, recovery_kit_ready={summary.get('recovery_kit_ready')}, password_setup_ready={summary.get('password_setup_ready')}, used_code={summary.get('latest_used_code')}"
    )
    if summary.get('reason'):
        lines.append(f"- why={summary.get('reason')}")
    if summary.get('latest_mail_subject'):
        lines.append(
            f"- latest_mail=#{summary.get('latest_mail_uid')} {summary.get('latest_mail_subject')} age={summary.get('latest_code_age_seconds')}s"
        )
    lines.append('- checklist:')
    for item in summary.get('checklist') or []:
        lines.append(f"  - {item}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte handoff voor de Proton manual finish boundary')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    summary = build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
