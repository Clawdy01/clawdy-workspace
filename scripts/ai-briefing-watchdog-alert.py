#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
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


MODE_REQUIREMENTS = {
    'preflight': 0,
    'proof-check': 1,
    'proof-progress': 3,
    'proof-target-check': 3,
}


def unique_bits(bits: list[str]) -> list[str]:
    unique: list[str] = []
    for bit in bits:
        cleaned = ' '.join((bit or '').split())
        if not cleaned:
            continue
        skip = False
        for existing in list(unique):
            if cleaned == existing or cleaned in existing:
                skip = True
                break
            if existing in cleaned:
                unique.remove(existing)
        if skip:
            continue
        unique.append(cleaned)
    return unique

def run_watchdog(timeout_seconds: int, require_qualified_runs: int) -> dict:
    cmd = [
        'python3',
        str(WATCHDOG),
        '--json',
        '--timeout',
        str(timeout_seconds),
        '--require-qualified-runs',
        str(require_qualified_runs),
    ]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_seconds + 5,
    )
    output = proc.stdout.strip() or proc.stderr.strip()
    if not output:
        raise SystemExit('watchdog gaf geen output')
    data = extract_json_document(output)
    data['_returncode'] = proc.returncode
    return data


def build_alert(data: dict, mode: str, require_qualified_runs: int) -> str:
    summary = data.get('summary') or data.get('status_text') or 'ai-briefing heeft aandacht nodig'
    reasons = [reason for reason in (data.get('reasons') or []) if reason]
    summary_output_examples = [example for example in (data.get('summary_output_examples') or []) if example]
    proof_example_limit = 2 if mode == 'preflight' else 3
    bits = [f"AI-briefing {mode}: {summary}"]
    readiness_text = data.get('readiness_text')
    if readiness_text:
        bits.append(readiness_text)
    if data.get('proof_state_text'):
        bits.append(data['proof_state_text'])
    elif data.get('proof_waiting_for_next_scheduled_run'):
        bits.append('wacht op eerstvolgende geplande kwalificatierun')
    if require_qualified_runs > 0:
        proof_progress = data.get('proof_progress_text')
        if proof_progress:
            bits.append(proof_progress)
        proof_runs_remaining = data.get('proof_runs_remaining')
        if proof_runs_remaining is not None and not data.get('proof_target_met'):
            bits.append(f'nog {proof_runs_remaining} kwalificerende run(s) te gaan')
    if data.get('next_run_at_text'):
        bits.append(f"volgende run {data['next_run_at_text']}")
    if data.get('proof_plan_text') and require_qualified_runs > 0:
        bits.append(data['proof_plan_text'])
    if data.get('proof_next_action_text') and require_qualified_runs > 0:
        bits.append(data['proof_next_action_text'])
    if data.get('proof_today_block_text') and require_qualified_runs > 0:
        bits.append(data['proof_today_block_text'])
    if data.get('proof_schedule_risk_text') and require_qualified_runs > 0:
        bits.append(data['proof_schedule_risk_text'])
    if data.get('proof_countdown_text') and require_qualified_runs > 0:
        bits.append(data['proof_countdown_text'])
    proof_wait_until = data.get('proof_wait_until_text')
    if proof_wait_until and require_qualified_runs > 0:
        proof_wait_bit = f"bewijs wacht tot {proof_wait_until}"
        if data.get('proof_wait_until_hint'):
            proof_wait_bit += f" ({data['proof_wait_until_hint']})"
        if data.get('proof_wait_until_reason_text'):
            proof_wait_bit += f": {data['proof_wait_until_reason_text']}"
        bits.append(proof_wait_bit)
    next_qualifying = data.get('proof_next_qualifying_slot_at_text')
    if next_qualifying and require_qualified_runs > 0:
        next_qualifying_bit = f"volgende kwalificatierun {next_qualifying}"
        if data.get('proof_next_qualifying_slot_hint'):
            next_qualifying_bit += f" ({data['proof_next_qualifying_slot_hint']})"
        if data.get('proof_next_qualifying_slot_day_label'):
            next_qualifying_bit += f" [{data['proof_next_qualifying_slot_day_label']}]"
        bits.append(next_qualifying_bit)
    if data.get('proof_due_at_text'):
        bits.append(f"bewijs uiterlijk {data['proof_due_at_text']}")
    if data.get('proof_target_due_at_text') and mode in {'proof-progress', 'proof-target-check'}:
        bits.append(f"bewijsdoel {data['proof_target_due_at_text']}")
    proof_target_run_slots_text = data.get('proof_target_run_slots_context_text') or data.get('proof_target_run_slots_text')
    if proof_target_run_slots_text and mode in {'proof-check', 'proof-progress', 'proof-target-check'}:
        bits.append(f"kwalificatie-slots {proof_target_run_slots_text}")
    if data.get('last_run_timeout_text'):
        bits.append(data['last_run_timeout_text'])
    if data.get('recent_run_duration_text'):
        bits.append(data['recent_run_duration_text'])
    if reasons:
        bits.append('redenen: ' + '; '.join(reasons[:3]))
    if summary_output_examples:
        bits.append('bewijs: ' + ' | '.join(summary_output_examples[:proof_example_limit]))
    return ' | '.join(unique_bits(bits))


def should_suppress_before_proof_deadline(data: dict) -> bool:
    proof_target_due_at = data.get('proof_target_due_at')
    if not proof_target_due_at:
        return False

    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    return now_ms < int(proof_target_due_at)


def main() -> int:
    parser = argparse.ArgumentParser(description='Geef alleen een korte alert terug als de AI-briefing-watchdog aandacht nodig heeft.')
    parser.add_argument('--mode', choices=sorted(MODE_REQUIREMENTS), default='preflight')
    parser.add_argument('--timeout', type=int, default=120)
    parser.add_argument('--require-qualified-runs', type=int, help='Override voor vereiste gekwalificeerde runs')
    args = parser.parse_args()

    require_qualified_runs = args.require_qualified_runs
    if require_qualified_runs is None:
        require_qualified_runs = MODE_REQUIREMENTS[args.mode]

    data = run_watchdog(args.timeout, max(0, require_qualified_runs))
    if args.mode == 'proof-target-check' and should_suppress_before_proof_deadline(data):
        print('NO_REPLY')
        return 0
    if data.get('ok'):
        print('NO_REPLY')
        return 0

    print(build_alert(data, args.mode, max(0, require_qualified_runs)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
