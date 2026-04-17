#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
WATCHDOG = WORKSPACE / 'scripts' / 'ai-briefing-watchdog.py'

PRODUCER_MODES = {
    'board': [
        ['--json', '--consumer-bundle', 'board-pair'],
    ],
    'eventlog': [
        ['--json', '--consumer-preset', 'eventlog-jsonl'],
    ],
    'all': [
        ['--json', '--consumer-bundle', 'board-suite'],
    ],
    'proof-board': [
        ['--json', '--require-qualified-runs', '3', '--consumer-bundle', 'board-pair'],
    ],
    'proof-eventlog': [
        ['--json', '--require-qualified-runs', '3', '--consumer-preset', 'eventlog-jsonl'],
    ],
    'proof-all': [
        ['--json', '--require-qualified-runs', '3', '--consumer-bundle', 'board-suite'],
    ],
}


def run_one(args):
    cmd = ['python3', str(WATCHDOG), *args]
    return subprocess.run(cmd, cwd=WORKSPACE, text=True, capture_output=True)


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


def build_quiet_summary(stdout: str, stderr: str, returncode: int) -> str | None:
    payload_text = (stdout or '').strip() or (stderr or '').strip()
    if not payload_text:
        return None
    try:
        payload = extract_json_document(payload_text)
    except json.JSONDecodeError:
        return None

    bits: list[str] = []
    if payload.get('summary'):
        bits.append(str(payload['summary']))
    if payload.get('proof_progress_text'):
        bits.append(str(payload['proof_progress_text']))
    if payload.get('proof_today_block_text'):
        bits.append(str(payload['proof_today_block_text']))
    if payload.get('proof_next_qualifying_slot_at_text'):
        next_run = f"volgende kwalificatierun {payload['proof_next_qualifying_slot_at_text']}"
        if payload.get('proof_next_qualifying_slot_hint'):
            next_run += f" ({payload['proof_next_qualifying_slot_hint']})"
        if payload.get('proof_next_qualifying_slot_day_label'):
            next_run += f" [{payload['proof_next_qualifying_slot_day_label']}]"
        bits.append(next_run)
    if payload.get('proof_target_due_at_text'):
        bits.append(f"bewijsdoel {payload['proof_target_due_at_text']}")
    proof_target_run_slots_text = payload.get('proof_target_run_slots_context_text') or payload.get('proof_target_run_slots_text')
    if proof_target_run_slots_text:
        bits.append(f"kwalificatie-slots {proof_target_run_slots_text}")
    if payload.get('last_run_timeout_text'):
        bits.append(str(payload['last_run_timeout_text']))
    if returncode != 0:
        reasons = [reason for reason in (payload.get('reasons') or []) if reason]
        if reasons:
            bits.append('redenen: ' + '; '.join(reasons[:2]))
    return ' | '.join(bits) if bits else None


def main():
    parser = argparse.ArgumentParser(description='Vaste producer-wrapper voor AI-briefing-watchdog consumers.')
    parser.add_argument('mode', choices=sorted(PRODUCER_MODES), help='Welke vaste consumer-producerroute je wilt draaien')
    parser.add_argument('--quiet', action='store_true', help='Toon geen volledige child-output, alleen een compacte producer-status')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]

    exit_code = 0
    summaries = []
    for base_args in PRODUCER_MODES[args.mode]:
        proc = run_one(base_args + extra)
        if proc.returncode != 0 and exit_code == 0:
            exit_code = proc.returncode
        summaries.append({
            'args': base_args,
            'returncode': proc.returncode,
            'stdout': proc.stdout,
            'stderr': proc.stderr,
        })
        if not args.quiet:
            if proc.stdout:
                sys.stdout.write(proc.stdout)
                if not proc.stdout.endswith('\n'):
                    print()
            if proc.stderr:
                sys.stderr.write(proc.stderr)

    if args.quiet:
        print(f'ai-briefing-watchdog-producer: {args.mode}')
        for item in summaries:
            label = ' '.join(item['args'])
            summary = build_quiet_summary(item['stdout'], item['stderr'], item['returncode'])
            if summary:
                print(f'- {label}: exit={item["returncode"]} | {summary}')
            else:
                print(f'- {label}: exit={item["returncode"]}')

    raise SystemExit(exit_code)


if __name__ == '__main__':
    main()
