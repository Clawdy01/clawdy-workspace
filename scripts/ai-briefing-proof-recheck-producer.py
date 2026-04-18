#!/usr/bin/env python3
import argparse
import json
import signal
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PROOF_RECHECK = WORKSPACE / 'scripts' / 'ai-briefing-proof-recheck.py'

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


def run_one(args):
    cmd = ['python3', str(PROOF_RECHECK), *args]
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
    if payload.get('result_text'):
        bits.append(str(payload['result_text']))
    if payload.get('reference_context_text'):
        bits.append(str(payload['reference_context_text']))
    if payload.get('proof_state_text'):
        bits.append(str(payload['proof_state_text']))
    if payload.get('proof_blocker_text'):
        bits.append(str(payload['proof_blocker_text']))
    if payload.get('proof_progress_text'):
        bits.append(str(payload['proof_progress_text']))
    if payload.get('proof_freshness_text'):
        bits.append(str(payload['proof_freshness_text']))
    examples = payload.get('summary_output_examples') or []
    if examples:
        bits.append('outputvoorbeelden: ' + '; '.join(str(example) for example in examples[:2]))
    if payload.get('proof_next_action_window_text'):
        bits.append(str(payload['proof_next_action_window_text']))
    elif payload.get('proof_next_action_text'):
        bits.append(str(payload['proof_next_action_text']))
    if payload.get('proof_recheck_commands_text'):
        bits.append(str(payload['proof_recheck_commands_text']))
    if payload.get('proof_schedule_risk_text'):
        bits.append(str(payload['proof_schedule_risk_text']))
    if payload.get('proof_countdown_text'):
        bits.append(str(payload['proof_countdown_text']))
    if payload.get('proof_config_identity_text'):
        bits.append(str(payload['proof_config_identity_text']))
    if payload.get('last_run_config_relation_text'):
        bits.append(str(payload['last_run_config_relation_text']))
    proof_runs_remaining = payload.get('proof_runs_remaining')
    if proof_runs_remaining is not None and not payload.get('proof_target_met'):
        bits.append(f'nog {proof_runs_remaining} kwalificerende run(s) te gaan')
    if returncode != 0 and payload.get('result_kind'):
        bits.append(f"resultaat: {payload['result_kind']}")

    deduped_bits = unique_bits(bits)
    return ' | '.join(deduped_bits) if deduped_bits else None


def main():
    parser = argparse.ArgumentParser(description='Vaste producer-wrapper voor AI-briefing proof-recheck consumers.')
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
        print(f'ai-briefing-proof-recheck-producer: {args.mode}')
        for item in summaries:
            label = ' '.join(item['args'])
            summary = build_quiet_summary(item['stdout'], item['stderr'], item['returncode'])
            if summary:
                print(f'- {label}: exit={item["returncode"]} | {summary}')
            else:
                print(f'- {label}: exit={item["returncode"]}')

    raise SystemExit(exit_code)


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)
