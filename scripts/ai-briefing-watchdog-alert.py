#!/usr/bin/env python3
import argparse
import json
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic

ROOT = Path('/home/clawdy/.openclaw/workspace')
WATCHDOG = ROOT / 'scripts' / 'ai-briefing-watchdog.py'
DEFAULT_REPORT_DIR = ROOT / 'tmp' / 'ai-briefing' / 'reports'


def build_consumer_presets(base_dir: Path | None = None) -> dict[str, dict]:
    report_dir = base_dir or DEFAULT_REPORT_DIR
    return {
        'board-json': {
            'path': report_dir / 'ai-briefing-watchdog-alert.json',
            'format': 'json',
            'append': False,
        },
        'board-text': {
            'path': report_dir / 'ai-briefing-watchdog-alert.txt',
            'format': 'text',
            'append': False,
        },
        'eventlog-jsonl': {
            'path': report_dir / 'ai-briefing-watchdog-alert.jsonl',
            'format': 'jsonl',
            'append': True,
        },
    }


CONSUMER_BUNDLES = {
    'board-pair': ['board-json', 'board-text'],
    'board-suite': ['board-json', 'board-text', 'eventlog-jsonl'],
}


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


def compact_reasons(reasons: list[str]) -> list[str]:
    compact: list[str] = []
    for reason in reasons:
        cleaned = ' '.join((reason or '').split())
        if not cleaned or cleaned == 'status not ok':
            continue
        compact.append(cleaned)
    return compact

def run_watchdog(timeout_seconds: int, require_qualified_runs: int, reference_ms: int | None = None) -> dict:
    cmd = [
        'python3',
        str(WATCHDOG),
        '--json',
        '--timeout',
        str(timeout_seconds),
        '--require-qualified-runs',
        str(require_qualified_runs),
    ]
    if reference_ms is not None:
        cmd.extend(['--reference-ms', str(reference_ms)])
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
    reasons = compact_reasons(data.get('reasons') or [])
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
    if data.get('proof_blocker_text'):
        bits.append(data['proof_blocker_text'])
    if data.get('proof_wait_until_text'):
        bits.append(data['proof_wait_until_text'])
    if data.get('proof_wait_until_reason_text'):
        bits.append(data['proof_wait_until_reason_text'])
    if require_qualified_runs > 0:
        proof_progress = data.get('proof_progress_text')
        if proof_progress and proof_progress not in (readiness_text or ''):
            bits.append(proof_progress)
        if data.get('proof_config_identity_text'):
            bits.append(data['proof_config_identity_text'])
        if data.get('last_run_config_relation_text'):
            bits.append(data['last_run_config_relation_text'])
        if data.get('proof_recheck_schedule_text'):
            bits.append(data['proof_recheck_schedule_text'])
        if data.get('proof_recheck_schedule_kind_text'):
            bits.append(data['proof_recheck_schedule_kind_text'])
        if data.get('proof_freshness_text'):
            bits.append(data['proof_freshness_text'])
        if data.get('proof_plan_text'):
            bits.append(data['proof_plan_text'])
        proof_runs_remaining = data.get('proof_runs_remaining')
        if proof_runs_remaining is not None and not data.get('proof_target_met'):
            bits.append(f'nog {proof_runs_remaining} kwalificerende run(s) te gaan')
    if data.get('proof_next_action_window_text') and require_qualified_runs > 0:
        bits.append(data['proof_next_action_window_text'])
    elif data.get('proof_next_action_text') and require_qualified_runs > 0:
        bits.append(data['proof_next_action_text'])
    if data.get('proof_recheck_commands_text') and require_qualified_runs > 0:
        bits.append(data['proof_recheck_commands_text'])
    if require_qualified_runs > 0 and not data.get('proof_next_action_window_text'):
        if data.get('proof_recheck_window_text') and data.get('proof_recheck_window_text') != data.get('proof_next_action_text'):
            bits.append(data['proof_recheck_window_text'])
        elif data.get('proof_recheck_after_text_compact'):
            bits.append(data['proof_recheck_after_text_compact'])
    if data.get('proof_schedule_risk_text') and require_qualified_runs > 0:
        bits.append(data['proof_schedule_risk_text'])
    if data.get('proof_countdown_text') and require_qualified_runs > 0:
        bits.append(data['proof_countdown_text'])
    if data.get('proof_target_check_gate_text') and require_qualified_runs > 0:
        bits.append(data['proof_target_check_gate_text'])
    if require_qualified_runs <= 0 and data.get('next_run_at_text'):
        bits.append(f"volgende run {data['next_run_at_text']}")
    proof_target_run_slots_text = data.get('proof_target_run_slots_context_text') or data.get('proof_target_run_slots_text')
    if proof_target_run_slots_text and mode in {'proof-check', 'proof-target-check'}:
        bits.append(f"kwalificatie-slots {proof_target_run_slots_text}")
    if data.get('last_run_timeout_text'):
        bits.append(data['last_run_timeout_text'])
    if data.get('recent_run_duration_text'):
        bits.append(data['recent_run_duration_text'])
    if reasons:
        bits.append('redenen: ' + '; '.join(reasons[:2]))
    if summary_output_examples:
        bits.append('bewijs: ' + ' | '.join(summary_output_examples[:proof_example_limit]))
    return ' | '.join(unique_bits(bits))


def resolve_consumer_settings(args, *, default_format: str, consumer_presets: dict[str, dict]):
    output_path = args.consumer_out
    output_format = args.consumer_format or default_format
    append = args.consumer_append

    if args.consumer_preset:
        preset = consumer_presets[args.consumer_preset]
        output_path = str(preset['path'])
        output_format = args.consumer_format or preset['format']
        append = args.consumer_append or preset['append']

    if output_path and output_format == 'jsonl':
        append = True

    return output_path, output_format, append


def describe_requested_outputs(
    *,
    output_path: str | None,
    output_format: str | None,
    append: bool,
    consumer_bundle: str | None,
    consumer_presets: dict[str, dict],
) -> list[dict]:
    outputs: list[dict] = []
    if output_path:
        outputs.append({
            'channel': 'consumer-out',
            'path': output_path,
            'format': output_format or 'text',
            'append': append,
        })
    if consumer_bundle:
        for preset_name in CONSUMER_BUNDLES[consumer_bundle]:
            preset = consumer_presets[preset_name]
            outputs.append({
                'channel': preset_name,
                'path': str(preset['path']),
                'format': preset['format'],
                'append': bool(preset['append']),
            })
    return outputs


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


def format_channel_summary(prefix: str, channels: list[str]) -> str:
    cleaned = [str(channel).strip() for channel in channels or [] if str(channel).strip()]
    if not cleaned:
        return f'{prefix}: geen'
    return f"{prefix}: {', '.join(cleaned)}"


def render_output(*, text: str, payload: dict, output_format: str) -> str:
    if output_format == 'json':
        return json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if output_format == 'jsonl':
        return json.dumps(payload, ensure_ascii=False) + '\n'
    return text if text.endswith('\n') else text + '\n'


def write_output(rendered: str, *, output_path: str | None = None, append: bool = False) -> None:
    if not output_path:
        return
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if append else 'w'
    with path.open(mode, encoding='utf-8') as handle:
        handle.write(rendered)


def emit_output(*, text: str, payload: dict, output_format: str, output_path: str | None = None, append: bool = False) -> None:
    rendered = render_output(text=text, payload=payload, output_format=output_format)
    write_output(rendered, output_path=output_path, append=append)
    sys.stdout.write(rendered)


def emit_output_with_bundle(*, text: str, payload: dict, stdout_format: str, stdout_output_path: str | None = None, stdout_output_format: str | None = None, stdout_append: bool = False, consumer_bundle: str | None = None, consumer_presets: dict[str, dict]) -> None:
    stdout_rendered = render_output(text=text, payload=payload, output_format=stdout_format)
    sys.stdout.write(stdout_rendered)
    if stdout_output_path:
        write_output(
            render_output(text=text, payload=payload, output_format=stdout_output_format or stdout_format),
            output_path=stdout_output_path,
            append=stdout_append,
        )
    if not consumer_bundle:
        return
    for preset_name in CONSUMER_BUNDLES[consumer_bundle]:
        preset = consumer_presets[preset_name]
        rendered = render_output(text=text, payload=payload, output_format=preset['format'])
        write_output(rendered, output_path=str(preset['path']), append=preset['append'])


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


def build_json_payload(
    data: dict,
    mode: str,
    require_qualified_runs: int,
    alert_text: str,
    *,
    no_reply: bool,
    suppressed_before_proof_deadline: bool,
    consumer_requested_outputs: list[dict],
    run_metadata: dict | None = None,
) -> dict:
    requested_channels: list[str] = []
    for item in consumer_requested_outputs:
        channel = str(item.get('channel') or '').strip()
        if channel and channel not in requested_channels:
            requested_channels.append(channel)
    return {
        'ok': bool(data.get('ok')),
        'mode': mode,
        'require_qualified_runs': require_qualified_runs,
        'watchdog_returncode': data.get('_returncode'),
        'no_reply': no_reply,
        'suppressed_before_proof_deadline': suppressed_before_proof_deadline,
        'summary': data.get('summary') or data.get('status_text'),
        'alert_text': alert_text,
        'readiness_text': data.get('readiness_text'),
        'reference_context_text': data.get('reference_context_text'),
        'proof_state': data.get('proof_state'),
        'proof_state_text': data.get('proof_state_text'),
        'proof_blocker_kind': data.get('proof_blocker_kind'),
        'proof_blocker_text': data.get('proof_blocker_text'),
        'proof_progress_text': data.get('proof_progress_text'),
        'proof_runs_remaining': data.get('proof_runs_remaining'),
        'proof_target_met': data.get('proof_target_met'),
        'proof_waiting_for_next_scheduled_run': data.get('proof_waiting_for_next_scheduled_run'),
        'proof_config_hash': data.get('proof_config_hash'),
        'proof_config_identity_text': data.get('proof_config_identity_text'),
        'last_run_config_relation': data.get('last_run_config_relation'),
        'last_run_config_relation_text': data.get('last_run_config_relation_text'),
        'proof_recheck_schedule_ok': data.get('proof_recheck_schedule_ok'),
        'proof_recheck_schedule_kind': data.get('proof_recheck_schedule_kind'),
        'proof_recheck_schedule_kind_text': data.get('proof_recheck_schedule_kind_text'),
        'proof_recheck_schedule_found': data.get('proof_recheck_schedule_found'),
        'proof_recheck_schedule_enabled': data.get('proof_recheck_schedule_enabled'),
        'proof_recheck_schedule_job_name': data.get('proof_recheck_schedule_job_name'),
        'proof_recheck_schedule_expr': data.get('proof_recheck_schedule_expr'),
        'proof_recheck_schedule_tz': data.get('proof_recheck_schedule_tz'),
        'proof_recheck_schedule_expected_gap_minutes': data.get('proof_recheck_schedule_expected_gap_minutes'),
        'proof_recheck_schedule_same_day_after_target': data.get('proof_recheck_schedule_same_day_after_target'),
        'proof_recheck_schedule_matches_grace': data.get('proof_recheck_schedule_matches_grace'),
        'proof_recheck_schedule_delta_minutes': data.get('proof_recheck_schedule_delta_minutes'),
        'proof_recheck_schedule_text': data.get('proof_recheck_schedule_text'),
        'proof_next_action_kind': data.get('proof_next_action_kind'),
        'proof_next_action_text': data.get('proof_next_action_text'),
        'proof_next_action_window_text': data.get('proof_next_action_window_text'),
        'proof_recheck_commands': data.get('proof_recheck_commands') or [],
        'proof_recheck_commands_text': data.get('proof_recheck_commands_text'),
        'proof_wait_until_at': data.get('proof_wait_until_at'),
        'proof_wait_until_text': data.get('proof_wait_until_text'),
        'proof_wait_until_reason_text': data.get('proof_wait_until_reason_text'),
        'proof_next_qualifying_slot_at': data.get('proof_next_qualifying_slot_at'),
        'proof_next_qualifying_slot_at_text': data.get('proof_next_qualifying_slot_at_text'),
        'proof_recheck_window_open': data.get('proof_recheck_window_open'),
        'proof_recheck_window_text': data.get('proof_recheck_window_text'),
        'proof_recheck_after_at': data.get('proof_recheck_after_at'),
        'proof_recheck_after_text': data.get('proof_recheck_after_text'),
        'proof_recheck_after_text_compact': data.get('proof_recheck_after_text_compact'),
        'proof_target_due_at': data.get('proof_target_due_at'),
        'proof_target_due_at_text': data.get('proof_target_due_at_text'),
        'proof_target_due_at_if_next_slot_missed': data.get('proof_target_due_at_if_next_slot_missed'),
        'proof_target_due_at_if_next_slot_missed_text': data.get('proof_target_due_at_if_next_slot_missed_text'),
        'proof_schedule_slip_ms': data.get('proof_schedule_slip_ms'),
        'proof_schedule_risk_text': data.get('proof_schedule_risk_text'),
        'proof_countdown_text': data.get('proof_countdown_text'),
        'proof_target_check_gate': data.get('proof_target_check_gate'),
        'proof_target_check_gate_text': data.get('proof_target_check_gate_text'),
        'proof_target_run_slots_context_text': data.get('proof_target_run_slots_context_text'),
        'proof_target_run_slots_text': data.get('proof_target_run_slots_text'),
        'proof_freshness_text': data.get('proof_freshness_text'),
        'proof_plan_text': data.get('proof_plan_text'),
        'last_run_timeout_text': data.get('last_run_timeout_text'),
        'recent_run_duration_text': data.get('recent_run_duration_text'),
        'consumer_requested_outputs': consumer_requested_outputs,
        'consumer_requested_output_count': len(consumer_requested_outputs),
        'consumer_requested_output_channel_count': len(requested_channels),
        'consumer_requested_output_count_text': (
            'consumer-output-aanvraag '
            f'gevraagd={len(consumer_requested_outputs)}, kanalen={len(requested_channels)}'
        ),
        'consumer_requested_output_channel_count_text': (
            'consumer-output-aanvraag-kanalen '
            f'gevraagd={len(consumer_requested_outputs)}, kanalen={len(requested_channels)}'
        ),
        'consumer_requested_output_channels_text': format_channel_summary(
            'consumer-output-aanvraag-kanalen',
            requested_channels,
        ),
        'consumer_requested_outputs_status_kind': (
            'requested' if consumer_requested_outputs else 'none-requested'
        ),
        'consumer_requested_outputs_status_text': (
            f'consumer-output-aanvraag vastgelegd voor {len(consumer_requested_outputs)} artifact(s)'
            if consumer_requested_outputs
            else 'consumer-output-aanvraag leeg (geen artifact-output gevraagd)'
        ),
        'consumer_requested_outputs_text': format_consumer_outputs(consumer_requested_outputs),
        'reasons': data.get('reasons') or [],
        'summary_output_examples': data.get('summary_output_examples') or [],
        **(run_metadata or {}),
    }


def should_suppress_before_proof_deadline(data: dict, reference_ms: int | None = None) -> bool:
    proof_target_due_at = data.get('proof_target_due_at')
    if not proof_target_due_at:
        return False

    now_ms = reference_ms if reference_ms is not None else int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    return now_ms < int(proof_target_due_at)


def main() -> int:
    parser = argparse.ArgumentParser(description='Geef alleen een korte alert terug als de AI-briefing-watchdog aandacht nodig heeft.')
    parser.add_argument('--mode', choices=sorted(MODE_REQUIREMENTS), default='preflight')
    parser.add_argument('--timeout', type=int, default=120)
    parser.add_argument('--json', action='store_true', help='Geef een machinevriendelijke alertstatus terug')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische alertchecks')
    parser.add_argument('--require-qualified-runs', type=int, help='Override voor vereiste gekwalificeerde runs')
    parser.add_argument('--consumer-out', help='Schrijf de alert-uitvoer ook naar een bestand voor cron/board-consumers')
    parser.add_argument('--consumer-root', help='Alternatieve basismap voor vaste consumer-presets/bundles (handig voor tests of gescheiden artifacts)')
    parser.add_argument('--consumer-preset', choices=['board-json', 'board-text', 'eventlog-jsonl'], help='Gebruik een vaste consumer-outputroute')
    parser.add_argument('--consumer-bundle', choices=sorted(CONSUMER_BUNDLES), help='Schrijf dezelfde alertstatus naar meerdere standaard consumerbestanden')
    parser.add_argument('--consumer-format', choices=['text', 'json', 'jsonl'], help='Outputformaat voor --consumer-out; default volgt stdout-formaat')
    parser.add_argument('--consumer-append', action='store_true', help='Append naar bestaand consumer-bestand in plaats van overschrijven')
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc)
    started_monotonic = monotonic()

    require_qualified_runs = args.require_qualified_runs
    if require_qualified_runs is None:
        require_qualified_runs = MODE_REQUIREMENTS[args.mode]

    data = run_watchdog(args.timeout, max(0, require_qualified_runs), reference_ms=args.reference_ms)
    suppressed_before_proof_deadline = (
        args.mode == 'proof-target-check'
        and should_suppress_before_proof_deadline(data, reference_ms=args.reference_ms)
    )
    alert_text = build_alert(data, args.mode, max(0, require_qualified_runs))
    no_reply = suppressed_before_proof_deadline or bool(data.get('ok'))
    stdout_format = 'json' if args.json else 'text'
    consumer_presets = build_consumer_presets(Path(args.consumer_root) if args.consumer_root else None)
    consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
        args,
        default_format=stdout_format,
        consumer_presets=consumer_presets,
    )
    consumer_requested_outputs = describe_requested_outputs(
        output_path=consumer_output_path,
        output_format=consumer_output_format,
        append=consumer_append,
        consumer_bundle=args.consumer_bundle,
        consumer_presets=consumer_presets,
    )
    finished_at = datetime.now(timezone.utc)
    duration_ms = int(round((monotonic() - started_monotonic) * 1000))
    payload = build_json_payload(
        data,
        args.mode,
        max(0, require_qualified_runs),
        'NO_REPLY' if no_reply else alert_text,
        no_reply=no_reply,
        suppressed_before_proof_deadline=suppressed_before_proof_deadline,
        consumer_requested_outputs=consumer_requested_outputs,
        run_metadata=build_run_metadata(
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=duration_ms,
        ),
    )

    if args.json:
        emit_output_with_bundle(
            text='NO_REPLY' if no_reply else alert_text,
            payload=payload,
            stdout_format=stdout_format,
            stdout_output_path=consumer_output_path,
            stdout_output_format=consumer_output_format,
            stdout_append=consumer_append,
            consumer_bundle=args.consumer_bundle,
            consumer_presets=consumer_presets,
        )
        return 0

    text_output = 'NO_REPLY' if no_reply else alert_text
    emit_output_with_bundle(
        text=text_output,
        payload=payload,
        stdout_format='text',
        stdout_output_path=consumer_output_path,
        stdout_output_format=consumer_output_format,
        stdout_append=consumer_append,
        consumer_bundle=args.consumer_bundle,
        consumer_presets=consumer_presets,
    )
    return 0


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)
