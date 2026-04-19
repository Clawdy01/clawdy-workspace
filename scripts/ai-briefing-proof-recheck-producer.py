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


def format_consumer_outputs(outputs: list[dict]) -> str | None:
    bits: list[str] = []
    for item in outputs or []:
        channel = str(item.get('channel') or '').strip()
        path = str(item.get('path') or '').strip()
        if channel and path:
            bits.append(f'{channel}: {path}')
        elif path:
            bits.append(path)
    if not bits:
        return None
    return 'consumer-artifacts: ' + '; '.join(bits)


def build_quiet_summary(stdout: str, stderr: str, returncode: int) -> tuple[str | None, dict | None]:
    payload_text = (stdout or '').strip() or (stderr or '').strip()
    if not payload_text:
        return None, None
    try:
        payload = extract_json_document(payload_text)
    except json.JSONDecodeError:
        return None, None

    proof_target_due_text = payload.get('proof_target_due_at_text')
    proof_target_due_if_missed_text = payload.get('proof_target_due_at_if_next_slot_missed_text')
    richer_due_context = ' '.join(
        str(bit)
        for bit in [
            payload.get('proof_schedule_risk_text'),
            payload.get('proof_target_check_gate_text'),
            payload.get('proof_countdown_text'),
        ]
        if bit
    )

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
    if payload.get('proof_wait_until_reason_text'):
        bits.append(str(payload['proof_wait_until_reason_text']))
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
    if proof_target_due_text and proof_target_due_text not in richer_due_context:
        bits.append(str(proof_target_due_text))
    if proof_target_due_if_missed_text and proof_target_due_if_missed_text not in richer_due_context:
        bits.append(str(proof_target_due_if_missed_text))
    if payload.get('proof_target_check_gate_text'):
        bits.append(str(payload['proof_target_check_gate_text']))
    if payload.get('proof_countdown_text'):
        bits.append(str(payload['proof_countdown_text']))
    if payload.get('consumer_effective_outputs_text'):
        bits.append(str(payload['consumer_effective_outputs_text']))
    elif payload.get('consumer_effective_outputs'):
        effective_outputs_text = format_consumer_outputs(payload.get('consumer_effective_outputs') or [])
        if effective_outputs_text:
            bits.append(effective_outputs_text)
    elif payload.get('consumer_outputs_text'):
        bits.append(str(payload['consumer_outputs_text']))
    elif payload.get('consumer_outputs'):
        consumer_outputs_text = format_consumer_outputs(payload.get('consumer_outputs') or [])
        if consumer_outputs_text:
            bits.append(consumer_outputs_text)
    elif payload.get('consumer_requested_outputs_text'):
        bits.append(str(payload['consumer_requested_outputs_text']))
    elif payload.get('consumer_requested_outputs'):
        requested_outputs_text = format_consumer_outputs(payload.get('consumer_requested_outputs') or [])
        if requested_outputs_text:
            bits.append(requested_outputs_text)
    if payload.get('consumer_requested_output_count_text'):
        bits.append(str(payload['consumer_requested_output_count_text']))
    if payload.get('consumer_requested_output_channel_count_text'):
        bits.append(str(payload['consumer_requested_output_channel_count_text']))
    if payload.get('consumer_requested_output_channels_text'):
        bits.append(str(payload['consumer_requested_output_channels_text']))
    if payload.get('consumer_requested_outputs_status_text'):
        bits.append(str(payload['consumer_requested_outputs_status_text']))
    if payload.get('consumer_outputs_count_text'):
        bits.append(str(payload['consumer_outputs_count_text']))
    if payload.get('consumer_output_channel_count_text'):
        bits.append(str(payload['consumer_output_channel_count_text']))
    if payload.get('consumer_output_channels_text'):
        bits.append(str(payload['consumer_output_channels_text']))
    if payload.get('consumer_outputs_status_text'):
        bits.append(str(payload['consumer_outputs_status_text']))
    if payload.get('consumer_outputs_missing_text'):
        bits.append(str(payload['consumer_outputs_missing_text']))
    if payload.get('consumer_outputs_unexpected_text'):
        bits.append(str(payload['consumer_outputs_unexpected_text']))
    if payload.get('consumer_effective_output_source_text'):
        bits.append(str(payload['consumer_effective_output_source_text']))
    if payload.get('consumer_effective_outputs_count_text'):
        bits.append(str(payload['consumer_effective_outputs_count_text']))
    if payload.get('consumer_effective_output_channel_count_text'):
        bits.append(str(payload['consumer_effective_output_channel_count_text']))
    if payload.get('consumer_effective_output_channels_text'):
        bits.append(str(payload['consumer_effective_output_channels_text']))
    if payload.get('consumer_effective_outputs_status_text'):
        bits.append(str(payload['consumer_effective_outputs_status_text']))
    if payload.get('consumer_effective_outputs_missing_text'):
        bits.append(str(payload['consumer_effective_outputs_missing_text']))
    if payload.get('consumer_effective_outputs_unexpected_text'):
        bits.append(str(payload['consumer_effective_outputs_unexpected_text']))
    if payload.get('proof_config_identity_text'):
        bits.append(str(payload['proof_config_identity_text']))
    if payload.get('last_run_config_relation_text'):
        bits.append(str(payload['last_run_config_relation_text']))
    if payload.get('proof_recheck_schedule_text'):
        bits.append(str(payload['proof_recheck_schedule_text']))
    proof_runs_remaining = payload.get('proof_runs_remaining')
    if proof_runs_remaining is not None and not payload.get('proof_target_met'):
        bits.append(f'nog {proof_runs_remaining} kwalificerende run(s) te gaan')
    if returncode != 0 and payload.get('result_kind'):
        bits.append(f"resultaat: {payload['result_kind']}")

    deduped_bits = unique_bits(bits)
    summary = ' | '.join(deduped_bits) if deduped_bits else None
    return summary, payload


def build_overall_item(producer_items: list[dict]) -> dict:
    primary = producer_items[0] if producer_items else None
    payload = (primary or {}).get('payload') or {}
    return {
        'returncode': (primary or {}).get('returncode'),
        'exit_code': payload.get('exit_code'),
        'summary': (primary or {}).get('summary'),
        'ok': payload.get('ok'),
        'state': payload.get('state'),
        'result_kind': payload.get('result_kind'),
        'result_text': payload.get('result_text'),
        'reference_now_text': payload.get('reference_now_text'),
        'reference_context_text': payload.get('reference_context_text'),
        'proof_state': payload.get('proof_state'),
        'proof_state_text': payload.get('proof_state_text'),
        'proof_blocker_kind': payload.get('proof_blocker_kind'),
        'proof_blocker_text': payload.get('proof_blocker_text'),
        'proof_progress_text': payload.get('proof_progress_text'),
        'proof_freshness_text': payload.get('proof_freshness_text'),
        'summary_output_examples': payload.get('summary_output_examples') or [],
        'proof_recheck_window_open': payload.get('proof_recheck_window_open'),
        'proof_recheck_window_text': payload.get('proof_recheck_window_text'),
        'proof_wait_until_at': payload.get('proof_wait_until_at'),
        'proof_wait_until_text': payload.get('proof_wait_until_text'),
        'proof_wait_until_hint': payload.get('proof_wait_until_hint'),
        'proof_wait_until_reason_text': payload.get('proof_wait_until_reason_text'),
        'proof_wait_until_remaining_ms': payload.get('proof_wait_until_remaining_ms'),
        'proof_wait_until_remaining_hours': payload.get('proof_wait_until_remaining_hours'),
        'proof_recheck_grace_ms': payload.get('proof_recheck_grace_ms'),
        'proof_recheck_after_at': payload.get('proof_recheck_after_at'),
        'proof_recheck_after_text': payload.get('proof_recheck_after_text'),
        'proof_recheck_after_hint': payload.get('proof_recheck_after_hint'),
        'proof_recheck_after_remaining_ms': payload.get('proof_recheck_after_remaining_ms'),
        'proof_recheck_after_remaining_hours': payload.get('proof_recheck_after_remaining_hours'),
        'proof_next_action_kind': payload.get('proof_next_action_kind'),
        'proof_next_action_window_text': payload.get('proof_next_action_window_text'),
        'proof_next_action_text': payload.get('proof_next_action_text'),
        'proof_recheck_commands': payload.get('proof_recheck_commands') or [],
        'proof_recheck_commands_text': payload.get('proof_recheck_commands_text'),
        'proof_countdown_text': payload.get('proof_countdown_text'),
        'proof_schedule_risk_text': payload.get('proof_schedule_risk_text'),
        'proof_next_qualifying_slot_at': payload.get('proof_next_qualifying_slot_at'),
        'proof_next_qualifying_slot_at_text': payload.get('proof_next_qualifying_slot_at_text'),
        'proof_next_qualifying_slot_hint': payload.get('proof_next_qualifying_slot_hint'),
        'proof_next_qualifying_slot_remaining_ms': payload.get('proof_next_qualifying_slot_remaining_ms'),
        'proof_next_qualifying_slot_remaining_hours': payload.get('proof_next_qualifying_slot_remaining_hours'),
        'proof_target_due_at': payload.get('proof_target_due_at'),
        'proof_target_due_at_text': payload.get('proof_target_due_at_text'),
        'proof_target_due_remaining_ms': payload.get('proof_target_due_remaining_ms'),
        'proof_target_due_remaining_hours': payload.get('proof_target_due_remaining_hours'),
        'proof_target_due_at_if_next_slot_missed': payload.get('proof_target_due_at_if_next_slot_missed'),
        'proof_target_due_at_if_next_slot_missed_text': payload.get('proof_target_due_at_if_next_slot_missed_text'),
        'proof_target_due_at_if_next_slot_missed_remaining_ms': payload.get('proof_target_due_at_if_next_slot_missed_remaining_ms'),
        'proof_target_due_at_if_next_slot_missed_remaining_hours': payload.get('proof_target_due_at_if_next_slot_missed_remaining_hours'),
        'proof_schedule_slip_ms': payload.get('proof_schedule_slip_ms'),
        'proof_schedule_slip_hours': payload.get('proof_schedule_slip_hours'),
        'proof_target_check_gate': payload.get('proof_target_check_gate'),
        'proof_target_check_gate_text': payload.get('proof_target_check_gate_text'),
        'proof_config_hash': payload.get('proof_config_hash'),
        'proof_config_identity_text': payload.get('proof_config_identity_text'),
        'last_run_config_relation': payload.get('last_run_config_relation'),
        'last_run_config_relation_text': payload.get('last_run_config_relation_text'),
        'proof_recheck_schedule_audit': payload.get('proof_recheck_schedule_audit') or {},
        'proof_recheck_schedule_ok': payload.get('proof_recheck_schedule_ok'),
        'proof_recheck_schedule_found': payload.get('proof_recheck_schedule_found'),
        'proof_recheck_schedule_enabled': payload.get('proof_recheck_schedule_enabled'),
        'proof_recheck_schedule_job_name': payload.get('proof_recheck_schedule_job_name'),
        'proof_recheck_schedule_expr': payload.get('proof_recheck_schedule_expr'),
        'proof_recheck_schedule_tz': payload.get('proof_recheck_schedule_tz'),
        'proof_recheck_schedule_expected_gap_minutes': payload.get('proof_recheck_schedule_expected_gap_minutes'),
        'proof_recheck_schedule_same_day_after_target': payload.get('proof_recheck_schedule_same_day_after_target'),
        'proof_recheck_schedule_matches_grace': payload.get('proof_recheck_schedule_matches_grace'),
        'proof_recheck_schedule_delta_minutes': payload.get('proof_recheck_schedule_delta_minutes'),
        'proof_recheck_schedule_text': payload.get('proof_recheck_schedule_text'),
        'proof_runs_remaining': payload.get('proof_runs_remaining'),
        'proof_recheck_ready': payload.get('proof_recheck_ready'),
        'proof_target_met': payload.get('proof_target_met'),
        'status_ok': payload.get('status_ok'),
        'status_returncode': payload.get('status_returncode'),
        'watchdog_ok': payload.get('watchdog_ok'),
        'watchdog_returncode': payload.get('watchdog_returncode'),
        'consumer_requested_outputs': payload.get('consumer_requested_outputs') or [],
        'consumer_requested_output_paths': payload.get('consumer_requested_output_paths') or [],
        'consumer_requested_output_channels': payload.get('consumer_requested_output_channels') or [],
        'consumer_requested_output_count': payload.get('consumer_requested_output_count'),
        'consumer_requested_output_channel_count': payload.get('consumer_requested_output_channel_count'),
        'consumer_requested_output_count_text': payload.get('consumer_requested_output_count_text'),
        'consumer_requested_output_channel_count_text': payload.get('consumer_requested_output_channel_count_text'),
        'consumer_requested_output_channels_text': payload.get('consumer_requested_output_channels_text'),
        'consumer_requested_outputs_status_kind': payload.get('consumer_requested_outputs_status_kind'),
        'consumer_requested_outputs_status_text': payload.get('consumer_requested_outputs_status_text'),
        'consumer_requested_outputs_text': payload.get('consumer_requested_outputs_text') or format_consumer_outputs(payload.get('consumer_requested_outputs') or []),
        'consumer_outputs_match_requested': payload.get('consumer_outputs_match_requested'),
        'consumer_output_count': payload.get('consumer_output_count'),
        'consumer_output_channel_count': payload.get('consumer_output_channel_count'),
        'consumer_output_channel_count_text': payload.get('consumer_output_channel_count_text'),
        'consumer_outputs_count_text': payload.get('consumer_outputs_count_text'),
        'consumer_outputs_status_kind': payload.get('consumer_outputs_status_kind'),
        'consumer_outputs_status_text': payload.get('consumer_outputs_status_text'),
        'consumer_outputs_missing_count': payload.get('consumer_outputs_missing_count'),
        'consumer_outputs_missing': payload.get('consumer_outputs_missing') or [],
        'consumer_outputs_missing_paths': payload.get('consumer_outputs_missing_paths') or [],
        'consumer_outputs_missing_channels': payload.get('consumer_outputs_missing_channels') or [],
        'consumer_outputs_missing_text': payload.get('consumer_outputs_missing_text'),
        'consumer_outputs_unexpected_count': payload.get('consumer_outputs_unexpected_count'),
        'consumer_outputs_unexpected': payload.get('consumer_outputs_unexpected') or [],
        'consumer_outputs_unexpected_paths': payload.get('consumer_outputs_unexpected_paths') or [],
        'consumer_outputs_unexpected_channels': payload.get('consumer_outputs_unexpected_channels') or [],
        'consumer_outputs_unexpected_text': payload.get('consumer_outputs_unexpected_text'),
        'consumer_outputs': payload.get('consumer_outputs') or [],
        'consumer_output_paths': payload.get('consumer_output_paths') or [],
        'consumer_output_channels': payload.get('consumer_output_channels') or [],
        'consumer_output_channels_text': payload.get('consumer_output_channels_text'),
        'consumer_outputs_text': payload.get('consumer_outputs_text') or format_consumer_outputs(payload.get('consumer_outputs') or []),
        'consumer_effective_output_source': payload.get('consumer_effective_output_source'),
        'consumer_effective_output_source_text': payload.get('consumer_effective_output_source_text'),
        'consumer_effective_outputs': payload.get('consumer_effective_outputs') or [],
        'consumer_effective_output_count': payload.get('consumer_effective_output_count'),
        'consumer_effective_output_channel_count': payload.get('consumer_effective_output_channel_count'),
        'consumer_effective_output_channel_count_text': payload.get('consumer_effective_output_channel_count_text'),
        'consumer_effective_output_paths': payload.get('consumer_effective_output_paths') or [],
        'consumer_effective_output_channels': payload.get('consumer_effective_output_channels') or [],
        'consumer_effective_output_channels_text': payload.get('consumer_effective_output_channels_text'),
        'consumer_effective_outputs_text': payload.get('consumer_effective_outputs_text') or format_consumer_outputs(payload.get('consumer_effective_outputs') or []),
        'consumer_effective_outputs_match_requested': payload.get('consumer_effective_outputs_match_requested'),
        'consumer_effective_outputs_missing_count': payload.get('consumer_effective_outputs_missing_count'),
        'consumer_effective_outputs_missing': payload.get('consumer_effective_outputs_missing') or [],
        'consumer_effective_outputs_missing_paths': payload.get('consumer_effective_outputs_missing_paths') or [],
        'consumer_effective_outputs_missing_channels': payload.get('consumer_effective_outputs_missing_channels') or [],
        'consumer_effective_outputs_missing_text': payload.get('consumer_effective_outputs_missing_text'),
        'consumer_effective_outputs_unexpected_count': payload.get('consumer_effective_outputs_unexpected_count'),
        'consumer_effective_outputs_unexpected': payload.get('consumer_effective_outputs_unexpected') or [],
        'consumer_effective_outputs_unexpected_paths': payload.get('consumer_effective_outputs_unexpected_paths') or [],
        'consumer_effective_outputs_unexpected_channels': payload.get('consumer_effective_outputs_unexpected_channels') or [],
        'consumer_effective_outputs_unexpected_text': payload.get('consumer_effective_outputs_unexpected_text'),
        'consumer_effective_outputs_count_text': payload.get('consumer_effective_outputs_count_text'),
        'consumer_effective_outputs_status_kind': payload.get('consumer_effective_outputs_status_kind'),
        'consumer_effective_outputs_status_text': payload.get('consumer_effective_outputs_status_text'),
    }


def build_top_level_overall_aliases(overall: dict) -> dict:
    aliases: dict = {}
    for key, value in (overall or {}).items():
        if key == 'ok':
            continue
        aliases[key] = value
    return aliases


def main():
    parser = argparse.ArgumentParser(description='Vaste producer-wrapper voor AI-briefing proof-recheck consumers.')
    parser.add_argument('mode', choices=sorted(PRODUCER_MODES), help='Welke vaste consumer-producerroute je wilt draaien')
    parser.add_argument('--quiet', action='store_true', help='Toon geen volledige child-output, alleen een compacte producer-status')
    parser.add_argument('--json', action='store_true', help='Geef een machinevriendelijke producer-samenvatting terug')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische producerchecks')
    parser.add_argument('--consumer-root', help='Alternatieve basismap voor vaste child-consumer-artifacts')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]

    if args.reference_ms is not None:
        extra = ['--reference-ms', str(args.reference_ms), *extra]
    if args.consumer_root:
        extra = ['--consumer-root', args.consumer_root, *extra]

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
        if not args.quiet and not args.json:
            if proc.stdout:
                sys.stdout.write(proc.stdout)
                if not proc.stdout.endswith('\n'):
                    print()
            if proc.stderr:
                sys.stderr.write(proc.stderr)

    producer_items = []
    for item in summaries:
        label = ' '.join(item['args'])
        summary, payload = build_quiet_summary(item['stdout'], item['stderr'], item['returncode'])
        producer_items.append({
            'label': label,
            'args': item['args'],
            'returncode': item['returncode'],
            'summary': summary,
            'payload': payload,
        })

    overall = build_overall_item(producer_items)

    if args.json:
        output = {
            'ok': exit_code == 0,
            'mode': args.mode,
            'reference_ms': args.reference_ms,
            'consumer_root': args.consumer_root,
            'overall': overall,
            'items': producer_items,
        }
        output.update(build_top_level_overall_aliases(overall))
        sys.stdout.write(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    elif args.quiet:
        print(f'ai-briefing-proof-recheck-producer: {args.mode}')
        if overall.get('summary'):
            print(f'- overall: exit={overall.get("returncode")} | {overall["summary"]}')
        duplicate_single_item = (
            len(producer_items) == 1
            and overall.get('returncode') == producer_items[0].get('returncode')
            and overall.get('summary')
            and overall.get('summary') == producer_items[0].get('summary')
        )
        if not duplicate_single_item:
            for item in producer_items:
                if item['summary']:
                    print(f'- {item["label"]}: exit={item["returncode"]} | {item["summary"]}')
                else:
                    print(f'- {item["label"]}: exit={item["returncode"]}')

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
