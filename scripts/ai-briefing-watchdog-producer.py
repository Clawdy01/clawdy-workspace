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


def compact_reasons(reasons: list[str]) -> list[str]:
    compact: list[str] = []
    for reason in reasons:
        cleaned = ' '.join((reason or '').split())
        if not cleaned or cleaned == 'status not ok':
            continue
        compact.append(cleaned)
    return compact


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
    if payload.get('readiness_text'):
        bits.append(str(payload['readiness_text']))
    if payload.get('proof_state_text'):
        bits.append(str(payload['proof_state_text']))
    elif payload.get('proof_waiting_for_next_scheduled_run'):
        bits.append('wacht op eerstvolgende geplande kwalificatierun')
    if payload.get('proof_progress_text'):
        readiness_text = str(payload.get('readiness_text') or '')
        proof_progress_text = str(payload['proof_progress_text'])
        if proof_progress_text not in readiness_text:
            bits.append(proof_progress_text)
    if payload.get('proof_config_identity_text'):
        bits.append(str(payload['proof_config_identity_text']))
    if payload.get('last_run_config_relation_text'):
        bits.append(str(payload['last_run_config_relation_text']))
    proof_runs_remaining = payload.get('proof_runs_remaining')
    if proof_runs_remaining is not None and not payload.get('proof_target_met'):
        bits.append(f'nog {proof_runs_remaining} kwalificerende run(s) te gaan')
    if payload.get('proof_next_action_text'):
        bits.append(str(payload['proof_next_action_text']))
    if payload.get('proof_recheck_commands_text'):
        bits.append(str(payload['proof_recheck_commands_text']))
    if payload.get('proof_recheck_window_text') and payload.get('proof_recheck_window_text') != payload.get('proof_next_action_text'):
        bits.append(str(payload['proof_recheck_window_text']))
    elif payload.get('proof_recheck_after_text_compact'):
        bits.append(str(payload['proof_recheck_after_text_compact']))
    if payload.get('proof_schedule_risk_text'):
        bits.append(str(payload['proof_schedule_risk_text']))
    if payload.get('proof_countdown_text'):
        bits.append(str(payload['proof_countdown_text']))
    if payload.get('proof_target_check_gate_text'):
        bits.append(str(payload['proof_target_check_gate_text']))
    proof_target_run_slots_text = payload.get('proof_target_run_slots_context_text') or payload.get('proof_target_run_slots_text')
    if proof_target_run_slots_text and not payload.get('proof_countdown_text'):
        bits.append(f"kwalificatie-slots {proof_target_run_slots_text}")
    if payload.get('last_run_timeout_text'):
        bits.append(str(payload['last_run_timeout_text']))
    if payload.get('recent_run_duration_text'):
        bits.append(str(payload['recent_run_duration_text']))
    if returncode != 0:
        reasons = compact_reasons(payload.get('reasons') or [])
        if reasons:
            bits.append('redenen: ' + '; '.join(reasons[:2]))
    deduped_bits = unique_bits(bits)
    return ' | '.join(deduped_bits) if deduped_bits else None


def main():
    parser = argparse.ArgumentParser(description='Vaste producer-wrapper voor AI-briefing-watchdog consumers.')
    parser.add_argument('mode', choices=sorted(PRODUCER_MODES), help='Welke vaste consumer-producerroute je wilt draaien')
    parser.add_argument('--quiet', action='store_true', help='Toon geen volledige child-output, alleen een compacte producer-status')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische producerchecks')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]

    if args.reference_ms is not None:
        extra = ['--reference-ms', str(args.reference_ms), *extra]

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
