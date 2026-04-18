#!/usr/bin/env python3
import argparse
import json
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'
DEFAULT_REPORT_DIR = ROOT / 'tmp' / 'ai-briefing' / 'reports'


def unique_reasons(reasons: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized_seen: set[str] = set()
    unique: list[str] = []
    for reason in reasons:
        cleaned = (reason or '').strip()
        if not cleaned:
            continue
        normalized = cleaned
        if normalized.startswith('proof freshness: '):
            normalized = normalized[len('proof freshness: '):].strip()
        if cleaned in seen or normalized in normalized_seen:
            continue
        seen.add(cleaned)
        normalized_seen.add(normalized)
        unique.append(cleaned)
    return unique


def unique_bits(bits: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for bit in bits:
        cleaned = ' '.join((bit or '').split())
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        unique.append(cleaned)
    return unique


CONSUMER_PRESETS = {
    'board-json': {
        'path': DEFAULT_REPORT_DIR / 'ai-briefing-watchdog.json',
        'format': 'json',
        'append': False,
    },
    'board-text': {
        'path': DEFAULT_REPORT_DIR / 'ai-briefing-watchdog.txt',
        'format': 'text',
        'append': False,
    },
    'eventlog-jsonl': {
        'path': DEFAULT_REPORT_DIR / 'ai-briefing-watchdog.jsonl',
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


def load_status(timeout_seconds: int, reference_ms: int | None = None) -> dict:
    command = ['python3', str(STATUS_SCRIPT), '--json']
    if reference_ms is not None:
        command.extend(['--reference-ms', str(reference_ms)])
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_seconds,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'ai-briefing-status failed: {proc.returncode}')
    return extract_json_document(proc.stdout)


def resolve_consumer_settings(args, *, default_format: str):
    output_path = args.consumer_out
    output_format = args.consumer_format or default_format
    append = args.consumer_append

    if args.consumer_preset:
        preset = CONSUMER_PRESETS[args.consumer_preset]
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


def emit_output_with_bundle(*, text: str, payload: dict, stdout_format: str, stdout_output_path: str | None = None, stdout_append: bool = False, consumer_bundle: str | None = None) -> None:
    emit_output(
        text=text,
        payload=payload,
        output_format=stdout_format,
        output_path=stdout_output_path,
        append=stdout_append,
    )
    if not consumer_bundle:
        return
    for preset_name in CONSUMER_BUNDLES[consumer_bundle]:
        preset = CONSUMER_PRESETS[preset_name]
        rendered = render_output(text=text, payload=payload, output_format=preset['format'])
        write_output(rendered, output_path=str(preset['path']), append=preset['append'])


def summarize_output_examples(status: dict) -> list[str]:
    summary_output_audit = ((status.get('last_run_summary') or {}).get('summary_output_audit') or {})
    if not summary_output_audit.get('available'):
        return []

    examples: list[str] = []

    top3_invalid_source_line_examples = summary_output_audit.get('top3_invalid_source_line_examples') or []
    if top3_invalid_source_line_examples:
        rendered = ', '.join(
            f"{example.get('title', 'onbekend')} -> {example.get('source_line', '').strip()}"
            for example in top3_invalid_source_line_examples[:2]
        )
        if rendered:
            examples.append('top3 ongeldige Bron-regel: ' + rendered)

    top3_missing_multi_domain_source_examples = summary_output_audit.get('top3_missing_multi_domain_source_examples') or []
    if top3_missing_multi_domain_source_examples:
        examples.append('top3 zonder multi-domein bronregel: ' + ', '.join(top3_missing_multi_domain_source_examples[:3]))

    top3_missing_multi_source_examples = summary_output_audit.get('top3_missing_multi_source_examples') or []
    if top3_missing_multi_source_examples:
        examples.append('top3 zonder multi-source: ' + ', '.join(top3_missing_multi_source_examples[:3]))

    top3_missing_primary_fresh_examples = summary_output_audit.get('top3_missing_primary_fresh_examples') or []
    if top3_missing_primary_fresh_examples:
        examples.append('top3 zonder primaire+verse combo: ' + ', '.join(top3_missing_primary_fresh_examples[:3]))

    top3_missing_date_line_examples = summary_output_audit.get('top3_missing_date_line_examples') or []
    if top3_missing_date_line_examples:
        examples.append('top3 zonder Datum:-regel: ' + ', '.join(top3_missing_date_line_examples[:3]))

    top3_missing_source_examples = summary_output_audit.get('top3_missing_source_examples') or []
    if top3_missing_source_examples:
        examples.append('top3 zonder bron: ' + ', '.join(top3_missing_source_examples[:3]))

    items_invalid_source_line_examples = summary_output_audit.get('items_invalid_source_line_examples') or []
    if items_invalid_source_line_examples and not top3_invalid_source_line_examples:
        rendered = ', '.join(
            f"{example.get('title', 'onbekend')} -> {example.get('source_line', '').strip()}"
            for example in items_invalid_source_line_examples[:2]
        )
        if rendered:
            examples.append('ongeldige Bron-regel: ' + rendered)

    exact_field_line_counts = summary_output_audit.get('exact_field_line_counts') or {}
    item_count = int(summary_output_audit.get('item_count') or 0)
    if item_count > 0:
        mismatched_fields = []
        for field_name in (
            'Titel:',
            'Bron:',
            'Datum:',
            'Wat is er nieuw:',
            'Waarom is dit belangrijk:',
            'Relevant voor Christian:',
        ):
            field_count = int(exact_field_line_counts.get(field_name) or 0)
            if field_count != item_count:
                mismatched_fields.append(f'{field_name} {field_count}/{item_count}')
        if mismatched_fields:
            examples.append('exacte veldlabels missen: ' + ', '.join(mismatched_fields[:4]))

    return examples[:3]


def is_expected_preflight_freshness_wait(status: dict, *, require_qualified_runs: int) -> bool:
    if require_qualified_runs > 0:
        return False
    if not status.get('found') or not status.get('enabled'):
        return False
    if not status.get('has_run_proof'):
        return False

    for key in ('payload_audit', 'runtime_audit', 'next_run_audit', 'storage_audit', 'runlog_audit', 'uniqueness_audit'):
        audit = status.get(key) or {}
        if audit and not audit.get('ok', False):
            return False

    proof_freshness = status.get('proof_freshness') or {}
    if proof_freshness.get('ok', True):
        return False
    if not proof_freshness.get('stale_finished'):
        return False

    proof_next_qualifying_slot_at = status.get('proof_next_qualifying_slot_at')
    if not proof_next_qualifying_slot_at:
        return False

    last_run_at = status.get('last_run_at')
    updated_at = status.get('updated_at')
    if not last_run_at or not updated_at or updated_at <= last_run_at:
        return False

    return True


def evaluate(status: dict, *, require_qualified_runs: int = 0) -> tuple[bool, list[str], str]:
    reasons: list[str] = []
    expected_preflight_freshness_wait = is_expected_preflight_freshness_wait(
        status,
        require_qualified_runs=require_qualified_runs,
    )

    if not status.get('ok') and not expected_preflight_freshness_wait:
        reasons.append('status not ok')
    if not status.get('found'):
        reasons.append('job niet gevonden')
    if not status.get('enabled'):
        reasons.append('job staat uit')

    for key in ('payload_audit', 'runtime_audit', 'next_run_audit', 'storage_audit', 'runlog_audit', 'uniqueness_audit', 'proof_freshness'):
        audit = status.get(key) or {}
        if not audit or audit.get('ok', False):
            continue
        if key == 'proof_freshness' and expected_preflight_freshness_wait:
            continue
        reasons.append(audit.get('text') or key)

    if status.get('attention_needed'):
        attention_text = status.get('attention_text') or 'attention nodig'
        proof_freshness_text = ((status.get('proof_freshness') or {}).get('text') or '').strip()
        if not (expected_preflight_freshness_wait and attention_text == f'proof freshness: {proof_freshness_text}'):
            reasons.append(attention_text)

    proof_qualified_runs = int(status.get('proof_qualified_runs') or 0)
    if require_qualified_runs > 0 and proof_qualified_runs < require_qualified_runs:
        reasons.append(
            f'onvoldoende gekwalificeerde runs voor huidige config ({proof_qualified_runs}/{require_qualified_runs})'
        )

    previous_run_slot_at = status.get('previous_run_slot_at')
    last_proof_qualified_run_at = status.get('last_proof_qualified_run_at')
    if require_qualified_runs > 0 and previous_run_slot_at:
        if not last_proof_qualified_run_at:
            reasons.append(
                f'geen gekwalificeerde run sinds verwacht dagslot {status.get("previous_run_slot_at_text") or previous_run_slot_at}'
            )
        elif last_proof_qualified_run_at < previous_run_slot_at:
            reasons.append(
                'laatste gekwalificeerde run is te oud voor huidige proof-check '
                f'({status.get("last_proof_qualified_run_at_text") or last_proof_qualified_run_at} < '
                f'{status.get("previous_run_slot_at_text") or previous_run_slot_at})'
            )

    readiness_phase = status.get('readiness_phase')
    if readiness_phase == 'ready-for-first-run':
        summary = status.get('text') or 'klaar voor eerste run'
    elif status.get('has_run_proof'):
        summary = status.get('text') or 'runbewijs aanwezig'
    else:
        summary = status.get('text') or 'geen runbewijs'

    reasons = unique_reasons(reasons)
    return (len(reasons) == 0, reasons, summary)


def main() -> int:
    parser = argparse.ArgumentParser(description='Controleer of de dagelijkse AI-briefing gezond en bewijsbaar is.')
    parser.add_argument('--json', action='store_true', help='print resultaat als JSON')
    parser.add_argument('--timeout', type=int, default=120, help='timeout in seconden voor ai-briefing-status.py')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische statuschecks')
    parser.add_argument('--require-qualified-runs', type=int, default=0, help='markeer de watchdog pas groen als minstens zoveel gekwalificeerde runs voor de huidige config aanwezig zijn')
    parser.add_argument('--consumer-out', help='Schrijf de watchdog-uitvoer ook naar een bestand voor cron/board-consumers')
    parser.add_argument('--consumer-preset', choices=sorted(CONSUMER_PRESETS), help='Gebruik een vaste consumer-outputroute')
    parser.add_argument('--consumer-bundle', choices=sorted(CONSUMER_BUNDLES), help='Schrijf dezelfde watchdog-status naar meerdere standaard consumerbestanden')
    parser.add_argument('--consumer-format', choices=['text', 'json', 'jsonl'], help='Outputformaat voor --consumer-out; default volgt stdout-formaat')
    parser.add_argument('--consumer-append', action='store_true', help='Append naar bestaand consumer-bestand in plaats van overschrijven')
    args = parser.parse_args()

    status = load_status(args.timeout, reference_ms=args.reference_ms)
    ok, reasons, summary = evaluate(status, require_qualified_runs=max(0, args.require_qualified_runs))
    proof_qualified_runs = int(status.get('proof_qualified_runs') or 0)
    required_qualified_runs = max(0, args.require_qualified_runs)
    proof_runs_remaining = int(status.get('proof_runs_remaining') or 0)
    last_run_timeout_audit = status.get('last_run_timeout_audit') or {}
    recent_run_duration_audit = status.get('recent_run_duration_audit') or {}
    result = {
        'ok': ok,
        'summary': summary,
        'reasons': reasons,
        'readiness_phase': status.get('readiness_phase'),
        'readiness_text': status.get('readiness_text'),
        'expected_proof_freshness_wait': status.get('expected_proof_freshness_wait'),
        'proof_waiting_for_next_scheduled_run': status.get('expected_proof_freshness_wait'),
        'proof_progress_text': status.get('proof_progress_text'),
        'proof_plan_text': status.get('proof_plan_text'),
        'proof_state': status.get('proof_state'),
        'proof_state_text': status.get('proof_state_text'),
        'proof_blocker_kind': status.get('proof_blocker_kind'),
        'proof_blocker_text': status.get('proof_blocker_text'),
        'proof_config_hash': status.get('proof_config_hash'),
        'proof_config_identity_text': status.get('proof_config_identity_text'),
        'last_run_config_relation': status.get('last_run_config_relation'),
        'last_run_config_relation_text': status.get('last_run_config_relation_text'),
        'proof_recheck_schedule_audit': status.get('proof_recheck_schedule_audit') or {},
        'proof_recheck_schedule_ok': ((status.get('proof_recheck_schedule_audit') or {}).get('ok')),
        'proof_recheck_schedule_found': ((status.get('proof_recheck_schedule_audit') or {}).get('found')),
        'proof_recheck_schedule_enabled': ((status.get('proof_recheck_schedule_audit') or {}).get('enabled')),
        'proof_recheck_schedule_job_name': ((status.get('proof_recheck_schedule_audit') or {}).get('job_name')),
        'proof_recheck_schedule_expr': ((status.get('proof_recheck_schedule_audit') or {}).get('schedule_expr')),
        'proof_recheck_schedule_tz': ((status.get('proof_recheck_schedule_audit') or {}).get('schedule_tz')),
        'proof_recheck_schedule_expected_gap_minutes': ((status.get('proof_recheck_schedule_audit') or {}).get('expected_gap_minutes')),
        'proof_recheck_schedule_same_day_after_target': ((status.get('proof_recheck_schedule_audit') or {}).get('same_day_after_target')),
        'proof_recheck_schedule_matches_grace': ((status.get('proof_recheck_schedule_audit') or {}).get('matches_grace')),
        'proof_recheck_schedule_delta_minutes': ((status.get('proof_recheck_schedule_audit') or {}).get('delta_minutes')),
        'proof_recheck_schedule_text': ((status.get('proof_recheck_schedule_audit') or {}).get('text')),
        'proof_next_action_kind': status.get('proof_next_action_kind'),
        'proof_next_action_text': status.get('proof_next_action_text'),
        'proof_next_action_window_text': status.get('proof_next_action_window_text'),
        'proof_recheck_commands': status.get('proof_recheck_commands'),
        'proof_recheck_commands_text': status.get('proof_recheck_commands_text'),
        'proof_target_runs': status.get('proof_target_runs'),
        'reference_now_ms': status.get('reference_now_ms'),
        'reference_now_text': status.get('reference_now_text'),
        'reference_mode': status.get('reference_mode'),
        'reference_context_text': status.get('reference_context_text'),
        'proof_qualified_runs': proof_qualified_runs,
        'proof_runs_remaining': proof_runs_remaining,
        'required_qualified_runs': required_qualified_runs,
        'proof_requirement_met': proof_qualified_runs >= required_qualified_runs,
        'proof_target_met': status.get('proof_target_met'),
        'proof_target_due_at': status.get('proof_target_due_at'),
        'job_name': status.get('job_name'),
        'next_run_at_text': status.get('next_run_at_text'),
        'proof_due_at_text': status.get('proof_due_at_text'),
        'proof_target_due_at_text': status.get('proof_target_due_at_text'),
        'proof_target_due_remaining_ms': status.get('proof_target_due_remaining_ms'),
        'proof_target_due_remaining_hours': status.get('proof_target_due_remaining_hours'),
        'proof_target_due_at_if_next_slot_missed_text': status.get('proof_target_due_at_if_next_slot_missed_text'),
        'proof_target_due_at_if_next_slot_missed_remaining_ms': status.get('proof_target_due_at_if_next_slot_missed_remaining_ms'),
        'proof_target_due_at_if_next_slot_missed_remaining_hours': status.get('proof_target_due_at_if_next_slot_missed_remaining_hours'),
        'proof_schedule_slip_ms': status.get('proof_schedule_slip_ms'),
        'proof_schedule_slip_hours': status.get('proof_schedule_slip_hours'),
        'proof_target_check_gate': status.get('proof_target_check_gate'),
        'proof_target_check_gate_text': status.get('proof_target_check_gate_text'),
        'proof_target_run_slots_text': status.get('proof_target_run_slots_text'),
        'proof_target_run_slots_context_text': status.get('proof_target_run_slots_context_text'),
        'proof_target_run_slot_day_labels': status.get('proof_target_run_slot_day_labels'),
        'proof_next_qualifying_slot_at_text': status.get('proof_next_qualifying_slot_at_text'),
        'proof_next_qualifying_slot_hint': status.get('proof_next_qualifying_slot_hint'),
        'proof_next_qualifying_slot_remaining_ms': status.get('proof_next_qualifying_slot_remaining_ms'),
        'proof_next_qualifying_slot_remaining_hours': status.get('proof_next_qualifying_slot_remaining_hours'),
        'proof_next_qualifying_slot_day_label': status.get('proof_next_qualifying_slot_day_label'),
        'proof_no_more_qualifying_runs_today': status.get('proof_no_more_qualifying_runs_today'),
        'proof_today_block_text': status.get('proof_today_block_text'),
        'proof_schedule_risk_text': status.get('proof_schedule_risk_text'),
        'proof_wait_until_at': status.get('proof_wait_until_at'),
        'proof_wait_until_text': status.get('proof_wait_until_text'),
        'proof_wait_until_hint': status.get('proof_wait_until_hint'),
        'proof_wait_until_remaining_ms': status.get('proof_wait_until_remaining_ms'),
        'proof_wait_until_remaining_hours': status.get('proof_wait_until_remaining_hours'),
        'proof_wait_until_reason_text': status.get('proof_wait_until_reason_text'),
        'proof_recheck_grace_ms': status.get('proof_recheck_grace_ms'),
        'proof_recheck_after_at': status.get('proof_recheck_after_at'),
        'proof_recheck_after_text': status.get('proof_recheck_after_text'),
        'proof_recheck_after_hint': status.get('proof_recheck_after_hint'),
        'proof_recheck_after_remaining_ms': status.get('proof_recheck_after_remaining_ms'),
        'proof_recheck_after_remaining_hours': status.get('proof_recheck_after_remaining_hours'),
        'proof_recheck_window_open': status.get('proof_recheck_window_open'),
        'proof_recheck_window_text': status.get('proof_recheck_window_text'),
        'proof_recheck_after_text_compact': status.get('proof_recheck_after_text_compact'),
        'proof_countdown_text': status.get('proof_countdown_text'),
        'previous_run_slot_at_text': status.get('previous_run_slot_at_text'),
        'last_proof_qualified_run_at_text': status.get('last_proof_qualified_run_at_text'),
        'has_run_proof': status.get('has_run_proof'),
        'attention_needed': status.get('attention_needed'),
        'status_text': status.get('text'),
        'last_run_timeout_text': last_run_timeout_audit.get('text'),
        'last_run_timeout_near_timeout': last_run_timeout_audit.get('near_timeout'),
        'last_run_timeout_timed_out': last_run_timeout_audit.get('timed_out'),
        'recent_run_duration_text': recent_run_duration_audit.get('text'),
        'recent_run_duration_near_timeout': recent_run_duration_audit.get('near_timeout'),
        'recent_run_duration_timed_out': recent_run_duration_audit.get('timed_out'),
        'summary_output_examples': summarize_output_examples(status),
    }

    state = 'ok' if ok else 'attention'
    lines = [f'ai briefing watchdog: {state} - {summary}']
    if result['proof_state_text']:
        lines.append(f"proof state: {result['proof_state_text']} ({result['proof_state']})")
    if result.get('proof_blocker_text'):
        lines.append(f"proof blocker: {result['proof_blocker_text']} ({result.get('proof_blocker_kind')})")
    if reasons:
        lines.append('reasons:')
        lines.extend(f'- {reason}' for reason in reasons)
    if result['readiness_text']:
        lines.append(f"readiness: {result['readiness_text']}")
    if result.get('reference_context_text'):
        lines.append(f"reference: {result['reference_context_text']}")
    if result.get('proof_config_identity_text'):
        lines.append(f"proof config: {result['proof_config_identity_text']}")
    if result.get('last_run_config_relation_text'):
        lines.append(f"last run config relation: {result['last_run_config_relation_text']}")
    if result.get('proof_recheck_schedule_text'):
        lines.append(f"proof recheck schedule: {result['proof_recheck_schedule_text']}")
    if result['proof_progress_text']:
        lines.append(f"proof progress: {result['proof_progress_text']}")
    if result['proof_waiting_for_next_scheduled_run']:
        lines.append('proof wait state: wacht op eerstvolgende geplande kwalificatierun')
    if required_qualified_runs > 0:
        lines.append(
            f"proof requirement: {proof_qualified_runs}/{required_qualified_runs} gekwalificeerde runs"
        )
        lines.append(f"proof remaining: nog {proof_runs_remaining} te gaan")
    if result['next_run_at_text']:
        lines.append(f"next run: {result['next_run_at_text']}")
    if result['proof_due_at_text']:
        lines.append(f"proof due: {result['proof_due_at_text']}")
    if result['proof_target_due_at_text']:
        lines.append(f"proof target due: {result['proof_target_due_at_text']}")
    if result['proof_plan_text']:
        lines.append(f"proof plan: {result['proof_plan_text']}")
    if result.get('proof_next_action_window_text'):
        lines.append(f"proof next action window: {result['proof_next_action_window_text']}")
    elif result['proof_next_action_text']:
        lines.append(f"proof next action: {result['proof_next_action_text']}")
    if result.get('proof_recheck_commands_text'):
        lines.append(f"proof recheck commands: {result['proof_recheck_commands_text']}")
    if not result.get('proof_next_action_window_text'):
        if result.get('proof_recheck_window_text') and result.get('proof_recheck_window_text') != result.get('proof_next_action_text'):
            lines.append(f"proof recheck window: {result['proof_recheck_window_text']}")
        elif result['proof_recheck_after_text_compact']:
            lines.append(f"proof recheck: {result['proof_recheck_after_text_compact']}")
    if result['proof_today_block_text']:
        lines.append(f"proof today block: {result['proof_today_block_text']}")
    if result['proof_schedule_risk_text']:
        lines.append(f"proof schedule risk: {result['proof_schedule_risk_text']}")
    if result['proof_wait_until_text']:
        proof_wait_line = f"proof wait until: {result['proof_wait_until_text']}"
        if result['proof_wait_until_hint']:
            proof_wait_line += f" ({result['proof_wait_until_hint']})"
        if result['proof_wait_until_remaining_hours'] is not None:
            proof_wait_line += f" [T{result['proof_wait_until_remaining_hours']:+g}u]"
        if result['proof_wait_until_reason_text']:
            proof_wait_line += f" - {result['proof_wait_until_reason_text']}"
        lines.append(proof_wait_line)
    if result['proof_next_qualifying_slot_at_text']:
        next_qualifying_line = f"next qualifying run: {result['proof_next_qualifying_slot_at_text']}"
        if result['proof_next_qualifying_slot_hint']:
            next_qualifying_line += f" ({result['proof_next_qualifying_slot_hint']})"
        if result['proof_next_qualifying_slot_remaining_hours'] is not None:
            next_qualifying_line += f" [T{result['proof_next_qualifying_slot_remaining_hours']:+g}u]"
        if result['proof_next_qualifying_slot_day_label']:
            next_qualifying_line += f" [{result['proof_next_qualifying_slot_day_label']}]"
        lines.append(next_qualifying_line)
    if result.get('proof_countdown_text'):
        lines.append(f"proof countdown: {result['proof_countdown_text']}")
    if result['proof_target_check_gate_text']:
        lines.append(
            f"proof target check gate: {result['proof_target_check_gate_text']} ({result['proof_target_check_gate']})"
        )
    if result['proof_target_run_slots_context_text']:
        lines.append(f"qualifying run slots: {result['proof_target_run_slots_context_text']}")
    elif result['proof_target_run_slots_text']:
        lines.append(f"qualifying run slots: {result['proof_target_run_slots_text']}")
    if result['last_run_timeout_text']:
        lines.append(f"last run timeout audit: {result['last_run_timeout_text']}")
    if result['recent_run_duration_text']:
        lines.append(f"recent run duration audit: {result['recent_run_duration_text']}")
    if result['last_proof_qualified_run_at_text']:
        lines.append(f"last qualified run: {result['last_proof_qualified_run_at_text']}")
    text_output = '\n'.join(unique_bits(lines)) + '\n'

    stdout_format = 'json' if args.json else 'text'
    consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
        args,
        default_format=stdout_format,
    )
    emit_output_with_bundle(
        text=text_output,
        payload=result,
        stdout_format=stdout_format,
        stdout_output_path=consumer_output_path,
        stdout_append=consumer_append,
        consumer_bundle=args.consumer_bundle,
    )

    return 0 if ok else 2


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
