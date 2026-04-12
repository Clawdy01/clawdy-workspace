#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
PROTON_STATUS = ROOT / 'scripts' / 'proton-status-summary.py'
PROTON_NEXT = ROOT / 'scripts' / 'proton-next-step.py'
PROTON_FINISH = ROOT / 'scripts' / 'proton-manual-finish-summary.py'


def run_json(cmd, label, default=None, timeout=20):
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return default, f'{label} timed out'
    if proc.returncode != 0:
        return default, (proc.stderr.strip() or proc.stdout.strip() or f'{label} failed: {proc.returncode}')
    try:
        return json.loads(proc.stdout), None
    except Exception as exc:
        return default, f'{label} returned invalid json: {exc}'


def build_board():
    status, status_error = run_json(['python3', str(PROTON_STATUS), '--json'], 'proton-status-summary', default={})
    next_step, next_error = run_json(['python3', str(PROTON_NEXT), '--json'], 'proton-next-step', default={})
    finish, finish_error = run_json(['python3', str(PROTON_FINISH), '--json'], 'proton-manual-finish-summary', default={})
    return {
        'status': status or {},
        'next_step': next_step or {},
        'finish': finish or {},
        'errors': {k: v for k, v in {'status': status_error, 'next_step': next_error, 'finish': finish_error}.items() if v},
    }


def render_text(board):
    status = board.get('status') or {}
    start = status.get('start') or {}
    route = status.get('route') or {}
    password = status.get('password_step') or {}
    next_step = board.get('next_step') or {}

    lines = ['Protonboard']
    lines.append(
        f"- start: signup={start.get('signup_visible')}, captcha={start.get('captcha_likely')}, blocked={start.get('blocked')}"
    )
    lines.append(
        f"- route: password-step={route.get('reached_password_step')}, username={route.get('username')}, propagated={route.get('propagated_value')}"
    )
    verify = next_step.get('verification') or {}
    regression_summary = status.get('regression_suspected')
    regression_next = next_step.get('regression_suspected')
    if verify.get('account_created'):
        regression_summary = False
        regression_next = False
    lines.append(f"- regressie-verdenking: {regression_summary}")
    lines.append(
        f"- password: velden={','.join(password.get('password_ids') or []) or 'geen'}, focus={password.get('active_id')}"
    )
    lines.append(
        f"- volgende stap: {next_step.get('recommended_route', 'onbekend')} ({next_step.get('reason', 'geen reden')})"
    )
    lines.append(f"- regressie vermoed: {regression_next}")
    if verify.get('account_created'):
        lines.append('- account-status: waarschijnlijk aangemaakt, recovery-afhandeling bewust nalopen')
    if verify:
        lines.append(
            f"- verify: action={verify.get('recommended_action')}, mail_matches={verify.get('verification_mail_matches')}, used_code={verify.get('latest_used_code')}, pw_ready={verify.get('password_setup_ready')}, stale={verify.get('stale')}"
        )
    if next_step.get('recommended_command'):
        lines.append(f"- command: {next_step.get('recommended_command')}")
    finish = board.get('finish') or {}
    if finish.get('manual_boundary'):
        lines.append(
            f"- handoff: recovery_kit={finish.get('recovery_kit_ready')}, account_created={finish.get('account_created')}, used_code={finish.get('latest_used_code')}, source={finish.get('verification_source')}, age={finish.get('verification_age_seconds')}s"
        )
        if finish.get('recommended_command'):
            lines.append(f"- handoff command: {finish.get('recommended_command')}")
        checklist = finish.get('checklist') or []
        if checklist:
            lines.append(f"- checklist: {checklist[0]}")
    errors = board.get('errors') or {}
    if errors:
        lines.append(f"- gedegradeerd: {', '.join(sorted(errors))}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compact Proton board uit statusprobe + notes')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    board = build_board()
    if args.json:
        print(json.dumps(board, ensure_ascii=False, indent=2))
    else:
        print(render_text(board))


if __name__ == '__main__':
    main()
