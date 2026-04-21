#!/usr/bin/env python3
import argparse
import json
import signal
import subprocess
import sys
from datetime import datetime, timezone
from time import monotonic
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
    if payload.get('proof_blocker_text'):
        bits.append(str(payload['proof_blocker_text']))
    if payload.get('proof_progress_text'):
        readiness_text = str(payload.get('readiness_text') or '')
        proof_progress_text = str(payload['proof_progress_text'])
        if proof_progress_text not in readiness_text:
            bits.append(proof_progress_text)
    if payload.get('proof_config_identity_text'):
        bits.append(str(payload['proof_config_identity_text']))
    if payload.get('last_run_config_relation_text'):
        bits.append(str(payload['last_run_config_relation_text']))
    if payload.get('proof_recheck_schedule_text'):
        bits.append(str(payload['proof_recheck_schedule_text']))
    if payload.get('proof_recheck_schedule_kind_text'):
        bits.append(str(payload['proof_recheck_schedule_kind_text']))
    if payload.get('proof_freshness_text'):
        bits.append(str(payload['proof_freshness_text']))
    proof_runs_remaining = payload.get('proof_runs_remaining')
    if proof_runs_remaining is not None and not payload.get('proof_target_met'):
        bits.append(f'nog {proof_runs_remaining} kwalificerende run(s) te gaan')
    if payload.get('proof_next_action_window_text'):
        bits.append(str(payload['proof_next_action_window_text']))
    elif payload.get('proof_next_action_text'):
        bits.append(str(payload['proof_next_action_text']))
    if payload.get('proof_recheck_commands_text'):
        bits.append(str(payload['proof_recheck_commands_text']))
    if not payload.get('proof_next_action_window_text'):
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
    summary_output_examples = [example for example in (payload.get('summary_output_examples') or []) if example]
    if summary_output_examples:
        bits.append('bewijs: ' + ' | '.join(summary_output_examples[:2]))
    if returncode != 0:
        reasons = compact_reasons(payload.get('reasons') or [])
        if reasons:
            bits.append('redenen: ' + '; '.join(reasons[:2]))
    deduped_bits = unique_bits(bits)
    return ' | '.join(deduped_bits) if deduped_bits else None


def extract_payload(stdout: str, stderr: str) -> dict:
    payload_text = (stdout or '').strip() or (stderr or '').strip()
    if not payload_text:
        return {}
    try:
        payload = extract_json_document(payload_text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def build_overall_summary(payload: dict, returncode: int) -> dict:
    if not payload:
        return {
            'ok': returncode == 0,
            'exit_code': returncode,
        }
    overall = {
        'ok': returncode == 0 and bool(payload.get('ok', True)),
        'exit_code': returncode,
        'summary': payload.get('summary'),
        'readiness_text': payload.get('readiness_text'),
        'reference_context_text': payload.get('reference_context_text'),
        'proof_state': payload.get('proof_state'),
        'proof_state_text': payload.get('proof_state_text'),
        'proof_blocker_kind': payload.get('proof_blocker_kind'),
        'proof_blocker_text': payload.get('proof_blocker_text'),
        'proof_progress_text': payload.get('proof_progress_text'),
        'proof_runs_remaining': payload.get('proof_runs_remaining'),
        'proof_target_met': payload.get('proof_target_met'),
        'proof_waiting_for_next_scheduled_run': payload.get('proof_waiting_for_next_scheduled_run'),
        'proof_config_hash': payload.get('proof_config_hash'),
        'proof_config_identity_text': payload.get('proof_config_identity_text'),
        'last_run_config_relation': payload.get('last_run_config_relation'),
        'last_run_config_relation_text': payload.get('last_run_config_relation_text'),
        'proof_recheck_schedule_ok': payload.get('proof_recheck_schedule_ok'),
        'proof_recheck_schedule_kind': payload.get('proof_recheck_schedule_kind'),
        'proof_recheck_schedule_kind_text': payload.get('proof_recheck_schedule_kind_text'),
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
        'proof_next_action_kind': payload.get('proof_next_action_kind'),
        'proof_next_action_text': payload.get('proof_next_action_text'),
        'proof_next_action_window_text': payload.get('proof_next_action_window_text'),
        'proof_recheck_commands': payload.get('proof_recheck_commands') or [],
        'proof_recheck_commands_text': payload.get('proof_recheck_commands_text'),
        'proof_wait_until_at': payload.get('proof_wait_until_at'),
        'proof_wait_until_text': payload.get('proof_wait_until_text'),
        'proof_wait_until_reason_text': payload.get('proof_wait_until_reason_text'),
        'proof_next_qualifying_slot_at': payload.get('proof_next_qualifying_slot_at'),
        'proof_next_qualifying_slot_at_text': payload.get('proof_next_qualifying_slot_at_text'),
        'proof_recheck_window_open': payload.get('proof_recheck_window_open'),
        'proof_recheck_window_text': payload.get('proof_recheck_window_text'),
        'proof_recheck_after_at': payload.get('proof_recheck_after_at'),
        'proof_recheck_after_text': payload.get('proof_recheck_after_text'),
        'proof_recheck_after_text_compact': payload.get('proof_recheck_after_text_compact'),
        'proof_target_due_at': payload.get('proof_target_due_at'),
        'proof_target_due_at_text': payload.get('proof_target_due_at_text'),
        'proof_target_due_at_if_next_slot_missed': payload.get('proof_target_due_at_if_next_slot_missed'),
        'proof_target_due_at_if_next_slot_missed_text': payload.get('proof_target_due_at_if_next_slot_missed_text'),
        'proof_schedule_slip_ms': payload.get('proof_schedule_slip_ms'),
        'proof_schedule_risk_text': payload.get('proof_schedule_risk_text'),
        'proof_countdown_text': payload.get('proof_countdown_text'),
        'proof_target_check_gate': payload.get('proof_target_check_gate'),
        'proof_target_check_gate_text': payload.get('proof_target_check_gate_text'),
        'proof_target_run_slots_context_text': payload.get('proof_target_run_slots_context_text'),
        'proof_target_run_slots_text': payload.get('proof_target_run_slots_text'),
        'proof_freshness_text': payload.get('proof_freshness_text'),
        'last_run_timeout_text': payload.get('last_run_timeout_text'),
        'recent_run_duration_text': payload.get('recent_run_duration_text'),
        'summary_output_examples': payload.get('summary_output_examples') or [],
        'consumer_requested_outputs': payload.get('consumer_requested_outputs') or [],
        'consumer_requested_output_count': payload.get('consumer_requested_output_count'),
        'consumer_requested_output_channel_count': payload.get('consumer_requested_output_channel_count'),
        'consumer_requested_output_count_text': payload.get('consumer_requested_output_count_text'),
        'consumer_requested_output_channel_count_text': payload.get('consumer_requested_output_channel_count_text'),
        'consumer_requested_output_channels_text': payload.get('consumer_requested_output_channels_text'),
        'consumer_requested_outputs_status_kind': payload.get('consumer_requested_outputs_status_kind'),
        'consumer_requested_outputs_status_text': payload.get('consumer_requested_outputs_status_text'),
        'consumer_requested_outputs_text': payload.get('consumer_requested_outputs_text'),
        'reasons': payload.get('reasons') or [],
    }
    return overall


def build_top_level_overall_aliases(overall: dict) -> dict:
    aliases: dict = {}
    for key, value in (overall or {}).items():
        if key == 'ok':
            continue
        aliases[key] = value
    return aliases


def build_run_metadata(*, started_at: datetime, finished_at: datetime, duration_ms: int) -> dict:
    duration_seconds = round(duration_ms / 1000, 3)
    return {
        'generated_at': finished_at.isoformat(),
        'generated_at_text': finished_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'started_at': started_at.isoformat(),
        'started_at_text': started_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'duration_ms': duration_ms,
        'duration_seconds': duration_seconds,
        'duration_text': f'{duration_seconds:.3f}s',
    }


def main():
    parser = argparse.ArgumentParser(description='Vaste producer-wrapper voor AI-briefing-watchdog consumers.')
    parser.add_argument('mode', choices=sorted(PRODUCER_MODES), help='Welke vaste consumer-producerroute je wilt draaien')
    parser.add_argument('--quiet', action='store_true', help='Toon geen volledige child-output, alleen een compacte producer-status')
    parser.add_argument('--json', action='store_true', help='Geef een machinevriendelijke producer-samenvatting terug')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische producerchecks')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]

    if args.reference_ms is not None:
        extra = ['--reference-ms', str(args.reference_ms), *extra]

    started_at = datetime.now(timezone.utc)
    started_monotonic = monotonic()

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
            'payload': extract_payload(proc.stdout, proc.stderr),
        })
        if not args.quiet and not args.json:
            if proc.stdout:
                sys.stdout.write(proc.stdout)
                if not proc.stdout.endswith('\n'):
                    print()
            if proc.stderr:
                sys.stderr.write(proc.stderr)

    if args.json:
        items = []
        overall = {}
        for item in summaries:
            payload = item.get('payload') or {}
            quiet_summary = build_quiet_summary(item['stdout'], item['stderr'], item['returncode'])
            item_summary = {
                'args': item['args'],
                'returncode': item['returncode'],
                'summary': quiet_summary,
                'payload': payload,
            }
            items.append(item_summary)
            if not overall:
                overall = build_overall_summary(payload, item['returncode'])
        result = {
            'mode': args.mode,
            'ok': exit_code == 0,
            'item_count': len(items),
            'items': items,
            'overall': overall,
        }
        result.update(build_top_level_overall_aliases(overall))
        result.update(
            build_run_metadata(
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
                duration_ms=int(round((monotonic() - started_monotonic) * 1000)),
            )
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

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
