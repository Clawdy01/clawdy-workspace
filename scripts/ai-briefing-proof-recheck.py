#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS = ROOT / 'scripts' / 'ai-briefing-status.py'
WATCHDOG = ROOT / 'scripts' / 'ai-briefing-watchdog.py'


def extract_json_document(text: str):
    text = (text or '').strip()
    if not text:
        raise json.JSONDecodeError('Expecting value', text, 0)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith(('{', '[')):
            continue
        candidate = '\n'.join(lines[index:]).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise json.JSONDecodeError('Expecting value', text, 0)


def run_json(cmd: list[str]) -> tuple[int, dict]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    output = proc.stdout.strip() or proc.stderr.strip()
    if not output:
        raise RuntimeError(f'geen output van: {" ".join(cmd)}')
    return proc.returncode, extract_json_document(output)


def build_payload(status_data: dict, watchdog_data: dict) -> dict:
    recheck_window_open = bool(status_data.get('proof_recheck_window_open'))
    proof_target_met = bool(watchdog_data.get('proof_target_met'))
    watchdog_ok = bool(watchdog_data.get('ok'))

    state = 'waiting'
    exit_code = 2
    if recheck_window_open and not watchdog_ok:
        state = 'attention'
        exit_code = 3
    if proof_target_met and watchdog_ok:
        state = 'ok'
        exit_code = 0

    summary_bits = [
        status_data.get('summary') or status_data.get('status_text'),
        watchdog_data.get('proof_progress_text'),
        status_data.get('proof_next_action_window_text') or status_data.get('proof_next_action_text'),
    ]
    summary = ' | '.join(bit for bit in summary_bits if bit)

    return {
        'ok': proof_target_met and watchdog_ok,
        'state': state,
        'exit_code': exit_code,
        'summary': summary,
        'reference_now_text': status_data.get('reference_now_text') or watchdog_data.get('reference_now_text'),
        'proof_state': status_data.get('proof_state') or watchdog_data.get('proof_state'),
        'proof_state_text': status_data.get('proof_state_text') or watchdog_data.get('proof_state_text'),
        'proof_progress_text': watchdog_data.get('proof_progress_text') or status_data.get('proof_progress_text'),
        'proof_target_met': proof_target_met,
        'proof_runs_remaining': watchdog_data.get('proof_runs_remaining'),
        'proof_recheck_window_open': recheck_window_open,
        'proof_recheck_window_text': status_data.get('proof_recheck_window_text'),
        'proof_next_action_text': status_data.get('proof_next_action_text') or watchdog_data.get('proof_next_action_text'),
        'proof_next_action_window_text': status_data.get('proof_next_action_window_text') or watchdog_data.get('proof_next_action_window_text'),
        'proof_recheck_commands': status_data.get('proof_recheck_commands') or watchdog_data.get('proof_recheck_commands') or [],
        'proof_recheck_commands_text': status_data.get('proof_recheck_commands_text') or watchdog_data.get('proof_recheck_commands_text'),
        'proof_blocker_text': status_data.get('proof_blocker_text') or watchdog_data.get('proof_blocker_text'),
        'proof_countdown_text': status_data.get('proof_countdown_text') or watchdog_data.get('proof_countdown_text'),
        'proof_schedule_risk_text': status_data.get('proof_schedule_risk_text') or watchdog_data.get('proof_schedule_risk_text'),
        'proof_target_due_at_text': status_data.get('proof_target_due_at_text') or watchdog_data.get('proof_target_due_at_text'),
        'proof_target_due_at_if_next_slot_missed_text': status_data.get('proof_target_due_at_if_next_slot_missed_text') or watchdog_data.get('proof_target_due_at_if_next_slot_missed_text'),
        'proof_config_identity_text': status_data.get('proof_config_identity_text') or watchdog_data.get('proof_config_identity_text'),
        'last_run_config_relation_text': status_data.get('last_run_config_relation_text') or watchdog_data.get('last_run_config_relation_text'),
        'watchdog_ok': watchdog_ok,
        'watchdog_returncode': watchdog_data.get('_returncode'),
    }


def build_text(payload: dict) -> str:
    bits = [
        f"AI-briefing proof-recheck: {payload.get('summary')}",
        payload.get('proof_state_text'),
        payload.get('proof_blocker_text'),
        payload.get('proof_recheck_window_text'),
        payload.get('proof_schedule_risk_text'),
        payload.get('proof_countdown_text'),
        payload.get('proof_recheck_commands_text'),
    ]
    unique_bits: list[str] = []
    for bit in bits:
        cleaned = ' '.join((bit or '').split())
        if not cleaned or cleaned in unique_bits:
            continue
        unique_bits.append(cleaned)
    return ' | '.join(unique_bits)


def main() -> int:
    parser = argparse.ArgumentParser(description='Draai de AI-briefing status + watchdog hercheck in één commando.')
    parser.add_argument('--json', action='store_true', help='geef machinevriendelijke JSON terug')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische herchecks')
    args = parser.parse_args()

    status_cmd = ['python3', str(STATUS), '--json']
    watchdog_cmd = ['python3', str(WATCHDOG), '--json', '--require-qualified-runs', '3']
    if args.reference_ms is not None:
        status_cmd.extend(['--reference-ms', str(args.reference_ms)])
        watchdog_cmd.extend(['--reference-ms', str(args.reference_ms)])

    _, status_data = run_json(status_cmd)
    watchdog_returncode, watchdog_data = run_json(watchdog_cmd)
    watchdog_data['_returncode'] = watchdog_returncode

    payload = build_payload(status_data, watchdog_data)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(build_text(payload))
    return int(payload['exit_code'])


if __name__ == '__main__':
    raise SystemExit(main())
