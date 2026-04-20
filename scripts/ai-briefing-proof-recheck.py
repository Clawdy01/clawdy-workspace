#!/usr/bin/env python3
import argparse
import json
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS = ROOT / 'scripts' / 'ai-briefing-status.py'
WATCHDOG = ROOT / 'scripts' / 'ai-briefing-watchdog.py'
DEFAULT_REPORT_DIR = ROOT / 'tmp' / 'ai-briefing' / 'reports'
CONSUMER_PRESET_NAMES = ('board-json', 'board-text', 'eventlog-jsonl')
CONSUMER_BUNDLES = {
    'board-pair': ['board-json', 'board-text'],
    'board-suite': ['board-json', 'board-text', 'eventlog-jsonl'],
}


def build_consumer_presets(base_dir: Path | None = None) -> dict[str, dict]:
    report_dir = (base_dir or DEFAULT_REPORT_DIR).expanduser().resolve()
    return {
        'board-json': {
            'path': report_dir / 'ai-briefing-proof-recheck.json',
            'format': 'json',
            'append': False,
        },
        'board-text': {
            'path': report_dir / 'ai-briefing-proof-recheck.txt',
            'format': 'text',
            'append': False,
        },
        'eventlog-jsonl': {
            'path': report_dir / 'ai-briefing-proof-recheck.jsonl',
            'format': 'jsonl',
            'append': True,
        },
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


def run_json(cmd: list[str]) -> tuple[int, dict]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    output = proc.stdout.strip() or proc.stderr.strip()
    if not output:
        raise RuntimeError(f'geen output van: {" ".join(cmd)}')
    return proc.returncode, extract_json_document(output)


def first_non_null(*values):
    for value in values:
        if value is not None:
            return value
    return None


def build_payload(status_data: dict, watchdog_data: dict) -> dict:
    recheck_window_open = bool(status_data.get('proof_recheck_window_open'))
    proof_target_met = bool(watchdog_data.get('proof_target_met'))
    watchdog_ok = bool(watchdog_data.get('ok'))
    status_ok = bool(status_data.get('ok'))
    summary_output_examples = watchdog_data.get('summary_output_examples') or []
    schedule_audit = {
        **((watchdog_data.get('proof_recheck_schedule_audit') or {})),
        **((status_data.get('proof_recheck_schedule_audit') or {})),
    }

    state = 'waiting'
    exit_code = 2
    result_kind = 'too-early'
    result_text = 'hercheck nog te vroeg, wacht op kwalificatierun en hercheckvenster'
    if recheck_window_open and not watchdog_ok:
        state = 'attention'
        exit_code = 3
        result_kind = 'attention-needed'
        result_text = 'hercheckvenster is open, maar bewijsdoel is nog niet gehaald'
    if proof_target_met and watchdog_ok:
        state = 'ok'
        exit_code = 0
        result_kind = 'proof-target-met'
        result_text = 'hercheck bevestigt dat het bewijsdoel gehaald is'

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
        'result_kind': result_kind,
        'result_text': result_text,
        'summary': summary,
        'reference_now_text': first_non_null(status_data.get('reference_now_text'), watchdog_data.get('reference_now_text')),
        'reference_context_text': first_non_null(status_data.get('reference_context_text'), watchdog_data.get('reference_context_text')),
        'proof_state': first_non_null(status_data.get('proof_state'), watchdog_data.get('proof_state')),
        'proof_state_text': first_non_null(status_data.get('proof_state_text'), watchdog_data.get('proof_state_text')),
        'proof_progress_text': first_non_null(watchdog_data.get('proof_progress_text'), status_data.get('proof_progress_text')),
        'proof_target_met': proof_target_met,
        'proof_recheck_ready': recheck_window_open,
        'proof_waiting_for_next_scheduled_run': watchdog_data.get('proof_waiting_for_next_scheduled_run'),
        'proof_runs_remaining': watchdog_data.get('proof_runs_remaining'),
        'last_run_timeout_text': watchdog_data.get('last_run_timeout_text'),
        'recent_run_duration_text': watchdog_data.get('recent_run_duration_text'),
        'proof_recheck_window_open': recheck_window_open,
        'proof_recheck_window_text': status_data.get('proof_recheck_window_text'),
        'proof_wait_until_at': first_non_null(status_data.get('proof_wait_until_at'), watchdog_data.get('proof_wait_until_at')),
        'proof_wait_until_text': first_non_null(status_data.get('proof_wait_until_text'), watchdog_data.get('proof_wait_until_text')),
        'proof_wait_until_hint': first_non_null(status_data.get('proof_wait_until_hint'), watchdog_data.get('proof_wait_until_hint')),
        'proof_wait_until_reason_text': first_non_null(status_data.get('proof_wait_until_reason_text'), watchdog_data.get('proof_wait_until_reason_text')),
        'proof_wait_until_remaining_ms': first_non_null(status_data.get('proof_wait_until_remaining_ms'), watchdog_data.get('proof_wait_until_remaining_ms')),
        'proof_wait_until_remaining_hours': first_non_null(status_data.get('proof_wait_until_remaining_hours'), watchdog_data.get('proof_wait_until_remaining_hours')),
        'proof_recheck_grace_ms': first_non_null(status_data.get('proof_recheck_grace_ms'), watchdog_data.get('proof_recheck_grace_ms')),
        'proof_recheck_after_at': first_non_null(status_data.get('proof_recheck_after_at'), watchdog_data.get('proof_recheck_after_at')),
        'proof_recheck_after_text': first_non_null(status_data.get('proof_recheck_after_text'), watchdog_data.get('proof_recheck_after_text')),
        'proof_recheck_after_hint': first_non_null(status_data.get('proof_recheck_after_hint'), watchdog_data.get('proof_recheck_after_hint')),
        'proof_recheck_after_remaining_ms': first_non_null(status_data.get('proof_recheck_after_remaining_ms'), watchdog_data.get('proof_recheck_after_remaining_ms')),
        'proof_recheck_after_remaining_hours': first_non_null(status_data.get('proof_recheck_after_remaining_hours'), watchdog_data.get('proof_recheck_after_remaining_hours')),
        'proof_next_action_kind': first_non_null(status_data.get('proof_next_action_kind'), watchdog_data.get('proof_next_action_kind')),
        'proof_next_action_text': first_non_null(status_data.get('proof_next_action_text'), watchdog_data.get('proof_next_action_text')),
        'proof_next_action_window_text': first_non_null(status_data.get('proof_next_action_window_text'), watchdog_data.get('proof_next_action_window_text')),
        'proof_recheck_commands': status_data.get('proof_recheck_commands') or watchdog_data.get('proof_recheck_commands') or [],
        'proof_recheck_commands_text': first_non_null(status_data.get('proof_recheck_commands_text'), watchdog_data.get('proof_recheck_commands_text')),
        'proof_blocker_kind': first_non_null(status_data.get('proof_blocker_kind'), watchdog_data.get('proof_blocker_kind')),
        'proof_blocker_text': first_non_null(status_data.get('proof_blocker_text'), watchdog_data.get('proof_blocker_text')),
        'proof_freshness_text': first_non_null((status_data.get('proof_freshness') or {}).get('text'), watchdog_data.get('proof_freshness_text')),
        'summary_output_examples': summary_output_examples,
        'proof_countdown_text': first_non_null(status_data.get('proof_countdown_text'), watchdog_data.get('proof_countdown_text')),
        'proof_schedule_risk_text': first_non_null(status_data.get('proof_schedule_risk_text'), watchdog_data.get('proof_schedule_risk_text')),
        'proof_next_qualifying_slot_at': first_non_null(status_data.get('proof_next_qualifying_slot_at'), watchdog_data.get('proof_next_qualifying_slot_at')),
        'proof_next_qualifying_slot_at_text': first_non_null(status_data.get('proof_next_qualifying_slot_at_text'), watchdog_data.get('proof_next_qualifying_slot_at_text')),
        'proof_next_qualifying_slot_hint': first_non_null(status_data.get('proof_next_qualifying_slot_hint'), watchdog_data.get('proof_next_qualifying_slot_hint')),
        'proof_next_qualifying_slot_remaining_ms': first_non_null(status_data.get('proof_next_qualifying_slot_remaining_ms'), watchdog_data.get('proof_next_qualifying_slot_remaining_ms')),
        'proof_next_qualifying_slot_remaining_hours': first_non_null(status_data.get('proof_next_qualifying_slot_remaining_hours'), watchdog_data.get('proof_next_qualifying_slot_remaining_hours')),
        'proof_target_due_at': first_non_null(status_data.get('proof_target_due_at'), watchdog_data.get('proof_target_due_at')),
        'proof_target_due_at_text': first_non_null(status_data.get('proof_target_due_at_text'), watchdog_data.get('proof_target_due_at_text')),
        'proof_target_due_remaining_ms': first_non_null(status_data.get('proof_target_due_remaining_ms'), watchdog_data.get('proof_target_due_remaining_ms')),
        'proof_target_due_remaining_hours': first_non_null(status_data.get('proof_target_due_remaining_hours'), watchdog_data.get('proof_target_due_remaining_hours')),
        'proof_target_due_at_if_next_slot_missed': first_non_null(status_data.get('proof_target_due_at_if_next_slot_missed'), watchdog_data.get('proof_target_due_at_if_next_slot_missed')),
        'proof_target_due_at_if_next_slot_missed_text': first_non_null(status_data.get('proof_target_due_at_if_next_slot_missed_text'), watchdog_data.get('proof_target_due_at_if_next_slot_missed_text')),
        'proof_target_due_at_if_next_slot_missed_remaining_ms': first_non_null(status_data.get('proof_target_due_at_if_next_slot_missed_remaining_ms'), watchdog_data.get('proof_target_due_at_if_next_slot_missed_remaining_ms')),
        'proof_target_due_at_if_next_slot_missed_remaining_hours': first_non_null(status_data.get('proof_target_due_at_if_next_slot_missed_remaining_hours'), watchdog_data.get('proof_target_due_at_if_next_slot_missed_remaining_hours')),
        'proof_schedule_slip_ms': first_non_null(status_data.get('proof_schedule_slip_ms'), watchdog_data.get('proof_schedule_slip_ms')),
        'proof_schedule_slip_hours': first_non_null(status_data.get('proof_schedule_slip_hours'), watchdog_data.get('proof_schedule_slip_hours')),
        'proof_target_check_gate': first_non_null(status_data.get('proof_target_check_gate'), watchdog_data.get('proof_target_check_gate')),
        'proof_target_check_gate_text': first_non_null(status_data.get('proof_target_check_gate_text'), watchdog_data.get('proof_target_check_gate_text')),
        'proof_config_hash': first_non_null(status_data.get('proof_config_hash'), watchdog_data.get('proof_config_hash')),
        'proof_config_identity_text': first_non_null(status_data.get('proof_config_identity_text'), watchdog_data.get('proof_config_identity_text')),
        'last_run_config_relation': first_non_null(status_data.get('last_run_config_relation'), watchdog_data.get('last_run_config_relation')),
        'last_run_config_relation_text': first_non_null(status_data.get('last_run_config_relation_text'), watchdog_data.get('last_run_config_relation_text')),
        'proof_recheck_schedule_audit': schedule_audit,
        'proof_recheck_schedule_ok': first_non_null(status_data.get('proof_recheck_schedule_ok'), watchdog_data.get('proof_recheck_schedule_ok'), schedule_audit.get('ok')),
        'proof_recheck_schedule_kind': first_non_null(status_data.get('proof_recheck_schedule_kind'), watchdog_data.get('proof_recheck_schedule_kind'), schedule_audit.get('kind')),
        'proof_recheck_schedule_kind_text': first_non_null(status_data.get('proof_recheck_schedule_kind_text'), watchdog_data.get('proof_recheck_schedule_kind_text'), schedule_audit.get('kind_text')),
        'proof_recheck_schedule_found': first_non_null(status_data.get('proof_recheck_schedule_found'), watchdog_data.get('proof_recheck_schedule_found'), schedule_audit.get('found')),
        'proof_recheck_schedule_enabled': first_non_null(status_data.get('proof_recheck_schedule_enabled'), watchdog_data.get('proof_recheck_schedule_enabled'), schedule_audit.get('enabled')),
        'proof_recheck_schedule_job_name': first_non_null(status_data.get('proof_recheck_schedule_job_name'), watchdog_data.get('proof_recheck_schedule_job_name'), schedule_audit.get('job_name')),
        'proof_recheck_schedule_expr': first_non_null(status_data.get('proof_recheck_schedule_expr'), watchdog_data.get('proof_recheck_schedule_expr'), schedule_audit.get('schedule_expr')),
        'proof_recheck_schedule_tz': first_non_null(status_data.get('proof_recheck_schedule_tz'), watchdog_data.get('proof_recheck_schedule_tz'), schedule_audit.get('schedule_tz')),
        'proof_recheck_schedule_expected_gap_minutes': first_non_null(status_data.get('proof_recheck_schedule_expected_gap_minutes'), watchdog_data.get('proof_recheck_schedule_expected_gap_minutes'), schedule_audit.get('expected_gap_minutes')),
        'proof_recheck_schedule_same_day_after_target': first_non_null(status_data.get('proof_recheck_schedule_same_day_after_target'), watchdog_data.get('proof_recheck_schedule_same_day_after_target'), schedule_audit.get('same_day_after_target')),
        'proof_recheck_schedule_matches_grace': first_non_null(status_data.get('proof_recheck_schedule_matches_grace'), watchdog_data.get('proof_recheck_schedule_matches_grace'), schedule_audit.get('matches_grace')),
        'proof_recheck_schedule_delta_minutes': first_non_null(status_data.get('proof_recheck_schedule_delta_minutes'), watchdog_data.get('proof_recheck_schedule_delta_minutes'), schedule_audit.get('delta_minutes')),
        'proof_recheck_schedule_text': first_non_null(status_data.get('proof_recheck_schedule_text'), watchdog_data.get('proof_recheck_schedule_text'), schedule_audit.get('text')),
        'status_ok': status_ok,
        'status_returncode': status_data.get('_returncode'),
        'watchdog_ok': watchdog_ok,
        'watchdog_returncode': watchdog_data.get('_returncode'),
    }


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


def update_effective_consumer_outputs(payload: dict) -> None:
    written_outputs = payload.get('consumer_outputs') or []
    requested_outputs = payload.get('consumer_requested_outputs') or []
    effective_outputs = written_outputs or requested_outputs
    if written_outputs:
        source = 'written'
    elif requested_outputs:
        source = 'requested-fallback'
    else:
        source = 'none'

    payload['consumer_effective_output_source'] = source
    payload['consumer_effective_output_source_text'] = {
        'written': 'consumer-effectieve-outputbron: geschreven artifacts',
        'requested-fallback': 'consumer-effectieve-outputbron: aangevraagde artifacts als fallback',
        'none': 'consumer-effectieve-outputbron: geen artifacts',
    }.get(source, f'consumer-effectieve-outputbron: {source}')
    effective_channels = sorted({item.get('channel') for item in effective_outputs if item.get('channel')})
    payload['consumer_effective_outputs'] = effective_outputs
    payload['consumer_effective_output_count'] = len(effective_outputs)
    payload['consumer_effective_output_paths'] = [item['path'] for item in effective_outputs]
    payload['consumer_effective_output_channels'] = [item['channel'] for item in effective_outputs]
    payload['consumer_effective_output_channel_count'] = len(effective_channels)
    payload['consumer_effective_output_channel_count_text'] = (
        'consumer-effectieve-output-kanalen '
        f"effectief={payload['consumer_effective_output_count']}, "
        f"kanalen={payload['consumer_effective_output_channel_count']}"
    )
    payload['consumer_effective_output_channels_text'] = format_channel_summary(
        'consumer-effectieve-output-kanalen',
        effective_channels,
    )
    payload['consumer_effective_outputs_text'] = format_consumer_outputs(effective_outputs)

    requested_signatures = {output_signature(item) for item in requested_outputs}
    effective_signatures = {output_signature(item) for item in effective_outputs}
    missing_outputs = [item for item in requested_outputs if output_signature(item) not in effective_signatures]
    unexpected_outputs = [item for item in effective_outputs if output_signature(item) not in requested_signatures]

    payload['consumer_effective_outputs_match_requested'] = not missing_outputs and not unexpected_outputs
    payload['consumer_effective_outputs_missing_count'] = len(missing_outputs)
    payload['consumer_effective_outputs_missing'] = missing_outputs
    payload['consumer_effective_outputs_missing_paths'] = [item['path'] for item in missing_outputs]
    payload['consumer_effective_outputs_missing_channels'] = [item['channel'] for item in missing_outputs]
    payload['consumer_effective_outputs_missing_text'] = format_consumer_outputs(missing_outputs)
    payload['consumer_effective_outputs_unexpected_count'] = len(unexpected_outputs)
    payload['consumer_effective_outputs_unexpected'] = unexpected_outputs
    payload['consumer_effective_outputs_unexpected_paths'] = [item['path'] for item in unexpected_outputs]
    payload['consumer_effective_outputs_unexpected_channels'] = [item['channel'] for item in unexpected_outputs]
    payload['consumer_effective_outputs_unexpected_text'] = format_consumer_outputs(unexpected_outputs)
    payload['consumer_effective_outputs_count_text'] = (
        'consumer-effectieve-output-telling '
        f"gevraagd={len(requested_outputs)}, "
        f"effectief={len(effective_outputs)}, "
        f"ontbrekend={len(missing_outputs)}, "
        f"onverwacht={len(unexpected_outputs)}"
    )
    if payload['consumer_effective_outputs_match_requested']:
        requested_count = len(requested_outputs)
        if requested_count:
            payload['consumer_effective_outputs_status_kind'] = 'ok'
            payload['consumer_effective_outputs_status_text'] = (
                f'consumer-effectieve-output-audit ok ({requested_count}/{requested_count} gevraagde artifacts gedekt via {source})'
            )
        else:
            payload['consumer_effective_outputs_status_kind'] = 'none-requested'
            payload['consumer_effective_outputs_status_text'] = 'consumer-effectieve-output-audit ok (geen artifact-output gevraagd)'
        return

    parts: list[str] = []
    missing_text = payload.get('consumer_effective_outputs_missing_text')
    unexpected_text = payload.get('consumer_effective_outputs_unexpected_text')
    if missing_text:
        parts.append('ontbreekt: ' + missing_text.removeprefix('consumer-artifacts: '))
    if unexpected_text:
        parts.append('onverwacht: ' + unexpected_text.removeprefix('consumer-artifacts: '))
    payload['consumer_effective_outputs_status_kind'] = 'mismatch'
    payload['consumer_effective_outputs_status_text'] = (
        f'consumer-effectieve-output-audit mismatch via {source} (' + '; '.join(parts) + ')'
    )


def output_signature(item: dict) -> tuple[str, str, str, bool]:
    return (
        str(item.get('channel') or ''),
        str(item.get('path') or ''),
        str(item.get('format') or ''),
        bool(item.get('append')),
    )


def update_consumer_output_audit(payload: dict) -> None:
    requested_outputs = payload.get('consumer_requested_outputs') or []
    written_outputs = payload.get('consumer_outputs') or []
    requested_signatures = {output_signature(item) for item in requested_outputs}
    written_signatures = {output_signature(item) for item in written_outputs}

    missing_outputs = [item for item in requested_outputs if output_signature(item) not in written_signatures]
    unexpected_outputs = [item for item in written_outputs if output_signature(item) not in requested_signatures]

    requested_channels = sorted({item.get('channel') for item in requested_outputs if item.get('channel')})
    payload['consumer_requested_output_count'] = len(requested_outputs)
    payload['consumer_requested_output_channel_count'] = len(requested_channels)
    payload['consumer_requested_output_channel_count_text'] = (
        'consumer-output-aanvraag-kanalen '
        f"gevraagd={payload['consumer_requested_output_count']}, "
        f"kanalen={payload['consumer_requested_output_channel_count']}"
    )
    payload['consumer_requested_output_channels_text'] = format_channel_summary(
        'consumer-output-aanvraag-kanalen',
        requested_channels,
    )
    payload['consumer_requested_output_count_text'] = (
        'consumer-output-aanvraag '
        f"gevraagd={payload['consumer_requested_output_count']}, "
        f"kanalen={payload['consumer_requested_output_channel_count']}"
    )
    if requested_outputs:
        payload['consumer_requested_outputs_status_kind'] = 'requested'
        payload['consumer_requested_outputs_status_text'] = (
            f"consumer-output-aanvraag vastgelegd voor {payload['consumer_requested_output_count']} artifact(s)"
        )
    else:
        payload['consumer_requested_outputs_status_kind'] = 'none-requested'
        payload['consumer_requested_outputs_status_text'] = 'consumer-output-aanvraag leeg (geen artifact-output gevraagd)'
    output_channels = sorted({item.get('channel') for item in written_outputs if item.get('channel')})
    payload['consumer_output_count'] = len(written_outputs)
    payload['consumer_output_channel_count'] = len(output_channels)
    payload['consumer_output_channel_count_text'] = (
        'consumer-output-kanalen '
        f"geschreven={payload['consumer_output_count']}, "
        f"kanalen={payload['consumer_output_channel_count']}"
    )
    payload['consumer_output_channels_text'] = format_channel_summary(
        'consumer-output-kanalen',
        output_channels,
    )
    payload['consumer_outputs_missing_count'] = len(missing_outputs)
    payload['consumer_outputs_missing_text'] = format_consumer_outputs(missing_outputs)
    payload['consumer_outputs_unexpected_count'] = len(unexpected_outputs)
    payload['consumer_outputs_unexpected_text'] = format_consumer_outputs(unexpected_outputs)
    payload['consumer_outputs_count_text'] = (
        'consumer-output-telling '
        f"gevraagd={payload['consumer_requested_output_count']}, "
        f"geschreven={payload['consumer_output_count']}, "
        f"ontbrekend={payload['consumer_outputs_missing_count']}, "
        f"onverwacht={payload['consumer_outputs_unexpected_count']}"
    )
    payload['consumer_outputs_match_requested'] = not missing_outputs and not unexpected_outputs
    payload['consumer_outputs_missing'] = missing_outputs
    payload['consumer_outputs_missing_paths'] = [item['path'] for item in missing_outputs]
    payload['consumer_outputs_missing_channels'] = [item['channel'] for item in missing_outputs]
    payload['consumer_outputs_unexpected'] = unexpected_outputs
    payload['consumer_outputs_unexpected_paths'] = [item['path'] for item in unexpected_outputs]
    payload['consumer_outputs_unexpected_channels'] = [item['channel'] for item in unexpected_outputs]
    update_effective_consumer_outputs(payload)

    if payload['consumer_outputs_match_requested']:
        requested_count = len(requested_outputs)
        if requested_count:
            payload['consumer_outputs_status_kind'] = 'ok'
            payload['consumer_outputs_status_text'] = (
                f'consumer-output-audit ok ({requested_count}/{requested_count} gevraagde artifacts geschreven)'
            )
        else:
            payload['consumer_outputs_status_kind'] = 'none-requested'
            payload['consumer_outputs_status_text'] = 'consumer-output-audit ok (geen artifact-output gevraagd)'
        return

    parts: list[str] = []
    missing_text = payload.get('consumer_outputs_missing_text')
    unexpected_text = payload.get('consumer_outputs_unexpected_text')
    if missing_text:
        parts.append('ontbreekt: ' + missing_text.removeprefix('consumer-artifacts: '))
    if unexpected_text:
        parts.append('onverwacht: ' + unexpected_text.removeprefix('consumer-artifacts: '))
    payload['consumer_outputs_status_kind'] = 'mismatch'
    payload['consumer_outputs_status_text'] = 'consumer-output-audit mismatch (' + '; '.join(parts) + ')'


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


def build_text(payload: dict) -> str:
    summary_output_examples = payload.get('summary_output_examples') or []
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
    bits = [
        f"AI-briefing proof-recheck: {payload.get('summary')}",
        payload.get('result_text'),
        payload.get('reference_context_text'),
        payload.get('proof_state_text'),
        payload.get('proof_config_identity_text'),
        payload.get('last_run_config_relation_text'),
        payload.get('proof_recheck_schedule_text'),
        payload.get('proof_recheck_schedule_kind_text'),
        payload.get('proof_blocker_text'),
        payload.get('proof_wait_until_reason_text'),
        payload.get('proof_freshness_text'),
        ('outputvoorbeelden: ' + '; '.join(summary_output_examples[:2])) if summary_output_examples else None,
        payload.get('proof_recheck_window_text'),
        payload.get('proof_schedule_risk_text'),
        None if proof_target_due_text and proof_target_due_text in richer_due_context else proof_target_due_text,
        None if proof_target_due_if_missed_text and proof_target_due_if_missed_text in richer_due_context else proof_target_due_if_missed_text,
        payload.get('proof_target_check_gate_text'),
        payload.get('proof_countdown_text'),
        payload.get('proof_recheck_commands_text'),
        payload.get('consumer_requested_output_count_text'),
        payload.get('consumer_requested_output_channel_count_text'),
        payload.get('consumer_requested_output_channels_text'),
        payload.get('consumer_requested_outputs_status_text'),
        payload.get('consumer_outputs_count_text'),
        payload.get('consumer_output_channel_count_text'),
        payload.get('consumer_output_channels_text'),
        payload.get('consumer_outputs_status_text'),
        payload.get('consumer_outputs_missing_text'),
        payload.get('consumer_outputs_unexpected_text'),
        payload.get('consumer_effective_output_source_text'),
        payload.get('consumer_effective_outputs_count_text'),
        payload.get('consumer_effective_output_channel_count_text'),
        payload.get('consumer_effective_output_channels_text'),
        payload.get('consumer_effective_outputs_status_text'),
        payload.get('consumer_effective_outputs_missing_text'),
        payload.get('consumer_effective_outputs_unexpected_text'),
        payload.get('consumer_effective_outputs_text') or payload.get('consumer_outputs_text'),
    ]
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

    return output_path, output_format, append


def render_output(*, text: str, payload: dict, output_format: str) -> str:
    if output_format == 'json':
        return json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if output_format == 'jsonl':
        return json.dumps(payload, ensure_ascii=False) + '\n'
    return text if text.endswith('\n') else text + '\n'


def write_output(rendered: str, *, output_path: str | None = None, append: bool = False) -> str | None:
    if not output_path:
        return None
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if append else 'w'
    with path.open(mode, encoding='utf-8') as handle:
        handle.write(rendered)
    return str(path)


def emit_output(*, text: str, payload: dict, stdout_format: str, output_path: str | None = None, output_format: str | None = None, append: bool = False) -> str | None:
    stdout_rendered = render_output(text=text, payload=payload, output_format=stdout_format)
    file_rendered = render_output(text=text, payload=payload, output_format=output_format or stdout_format)
    written_path = write_output(file_rendered, output_path=output_path, append=append)
    sys.stdout.write(stdout_rendered)
    return written_path


def collect_output_targets(*, output_format: str, output_path: str | None = None, output_append: bool = False, consumer_bundle: str | None = None, consumer_presets: dict[str, dict]) -> list[dict]:
    output_targets: list[dict] = []
    if output_path:
        output_targets.append({
            'channel': 'stdout-output',
            'path': str(Path(output_path).expanduser().resolve()),
            'format': output_format,
            'append': bool(output_append),
        })
    if consumer_bundle:
        for preset_name in CONSUMER_BUNDLES[consumer_bundle]:
            preset = consumer_presets[preset_name]
            output_targets.append({
                'channel': preset_name,
                'path': str(Path(preset['path']).expanduser().resolve()),
                'format': preset['format'],
                'append': bool(preset['append']),
            })
    return output_targets


def emit_output_with_bundle(*, text: str, payload: dict, stdout_format: str, output_path: str | None = None, output_format: str | None = None, output_append: bool = False, consumer_bundle: str | None = None, consumer_presets: dict[str, dict]) -> list[dict]:
    written_outputs: list[dict] = []
    if output_path:
        rendered = render_output(text=text, payload=payload, output_format=output_format or stdout_format)
        written_path = write_output(rendered, output_path=output_path, append=output_append)
        if written_path:
            written_outputs.append({
                'channel': 'stdout-output',
                'path': written_path,
                'format': output_format or stdout_format,
                'append': bool(output_append),
            })
    if consumer_bundle:
        for preset_name in CONSUMER_BUNDLES[consumer_bundle]:
            preset = consumer_presets[preset_name]
            rendered = render_output(text=text, payload=payload, output_format=preset['format'])
            written_path = write_output(rendered, output_path=str(preset['path']), append=preset['append'])
            if written_path:
                written_outputs.append({
                    'channel': preset_name,
                    'path': written_path,
                    'format': preset['format'],
                    'append': bool(preset['append']),
                })
    payload['consumer_outputs'] = written_outputs
    payload['consumer_output_paths'] = [item['path'] for item in written_outputs]
    payload['consumer_output_channels'] = [item['channel'] for item in written_outputs]
    payload['consumer_outputs_text'] = format_consumer_outputs(written_outputs)
    update_consumer_output_audit(payload)
    sys.stdout.write(render_output(text=build_text(payload), payload=payload, output_format=stdout_format))
    return written_outputs


def main() -> int:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    parser = argparse.ArgumentParser(description='Draai de AI-briefing status + watchdog hercheck in één commando.')
    parser.add_argument('--json', action='store_true', help='geef machinevriendelijke JSON terug')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische herchecks')
    parser.add_argument('--consumer-out', help='Schrijf de proof-recheck-uitvoer ook naar een bestand voor cron/board-consumers')
    parser.add_argument('--consumer-root', help='Alternatieve basismap voor vaste consumer-presets/bundles (handig voor tests of gescheiden artifacts)')
    parser.add_argument('--consumer-preset', choices=sorted(CONSUMER_PRESET_NAMES), help='Gebruik een vaste consumer-outputroute')
    parser.add_argument('--consumer-bundle', choices=sorted(CONSUMER_BUNDLES), help='Schrijf dezelfde proof-recheck-status naar meerdere standaard consumerbestanden')
    parser.add_argument('--consumer-format', choices=['text', 'json', 'jsonl'], help='Outputformaat voor --consumer-out; default volgt stdout-formaat')
    parser.add_argument('--consumer-append', action='store_true', help='Append naar bestaand consumer-bestand in plaats van overschrijven')
    args = parser.parse_args()

    status_cmd = ['python3', str(STATUS), '--json']
    watchdog_cmd = ['python3', str(WATCHDOG), '--json', '--require-qualified-runs', '3']
    if args.reference_ms is not None:
        status_cmd.extend(['--reference-ms', str(args.reference_ms)])
        watchdog_cmd.extend(['--reference-ms', str(args.reference_ms)])

    status_returncode, status_data = run_json(status_cmd)
    status_data['_returncode'] = status_returncode
    watchdog_returncode, watchdog_data = run_json(watchdog_cmd)
    watchdog_data['_returncode'] = watchdog_returncode

    payload = build_payload(status_data, watchdog_data)
    text_output = build_text(payload)
    stdout_format = 'json' if args.json else 'text'
    consumer_presets = build_consumer_presets(Path(args.consumer_root) if args.consumer_root else None)
    consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
        args,
        default_format=stdout_format,
        consumer_presets=consumer_presets,
    )
    requested_outputs = collect_output_targets(
        output_format=consumer_output_format,
        output_path=consumer_output_path,
        output_append=consumer_append,
        consumer_bundle=args.consumer_bundle,
        consumer_presets=consumer_presets,
    )
    payload['consumer_requested_outputs'] = requested_outputs
    payload['consumer_requested_output_paths'] = [item['path'] for item in requested_outputs]
    payload['consumer_requested_output_channels'] = [item['channel'] for item in requested_outputs]
    payload['consumer_requested_outputs_text'] = format_consumer_outputs(requested_outputs)
    payload['consumer_outputs'] = requested_outputs
    payload['consumer_output_paths'] = [item['path'] for item in payload['consumer_outputs']]
    payload['consumer_output_channels'] = [item['channel'] for item in payload['consumer_outputs']]
    payload['consumer_outputs_text'] = format_consumer_outputs(payload['consumer_outputs'])
    update_consumer_output_audit(payload)
    text_output = build_text(payload)
    emit_output_with_bundle(
        text=text_output,
        payload=payload,
        stdout_format=stdout_format,
        output_path=consumer_output_path,
        output_format=consumer_output_format,
        output_append=consumer_append,
        consumer_bundle=args.consumer_bundle,
        consumer_presets=consumer_presets,
    )
    return int(payload['exit_code'])


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)
