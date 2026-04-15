#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'
DEFAULT_REPORT_DIR = ROOT / 'tmp' / 'ai-briefing' / 'reports'
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


def load_status(timeout_seconds: int) -> dict:
    proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--json'],
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

    return (len(reasons) == 0, reasons, summary)


def main() -> int:
    parser = argparse.ArgumentParser(description='Controleer of de dagelijkse AI-briefing gezond en bewijsbaar is.')
    parser.add_argument('--json', action='store_true', help='print resultaat als JSON')
    parser.add_argument('--timeout', type=int, default=120, help='timeout in seconden voor ai-briefing-status.py')
    parser.add_argument('--require-qualified-runs', type=int, default=0, help='markeer de watchdog pas groen als minstens zoveel gekwalificeerde runs voor de huidige config aanwezig zijn')
    parser.add_argument('--consumer-out', help='Schrijf de watchdog-uitvoer ook naar een bestand voor cron/board-consumers')
    parser.add_argument('--consumer-preset', choices=sorted(CONSUMER_PRESETS), help='Gebruik een vaste consumer-outputroute')
    parser.add_argument('--consumer-bundle', choices=sorted(CONSUMER_BUNDLES), help='Schrijf dezelfde watchdog-status naar meerdere standaard consumerbestanden')
    parser.add_argument('--consumer-format', choices=['text', 'json', 'jsonl'], help='Outputformaat voor --consumer-out; default volgt stdout-formaat')
    parser.add_argument('--consumer-append', action='store_true', help='Append naar bestaand consumer-bestand in plaats van overschrijven')
    args = parser.parse_args()

    status = load_status(args.timeout)
    ok, reasons, summary = evaluate(status, require_qualified_runs=max(0, args.require_qualified_runs))
    proof_qualified_runs = int(status.get('proof_qualified_runs') or 0)
    required_qualified_runs = max(0, args.require_qualified_runs)
    result = {
        'ok': ok,
        'summary': summary,
        'reasons': reasons,
        'readiness_phase': status.get('readiness_phase'),
        'proof_progress_text': status.get('proof_progress_text'),
        'proof_target_runs': status.get('proof_target_runs'),
        'proof_qualified_runs': proof_qualified_runs,
        'required_qualified_runs': required_qualified_runs,
        'proof_requirement_met': proof_qualified_runs >= required_qualified_runs,
        'proof_target_due_at': status.get('proof_target_due_at'),
        'job_name': status.get('job_name'),
        'next_run_at_text': status.get('next_run_at_text'),
        'proof_due_at_text': status.get('proof_due_at_text'),
        'proof_target_due_at_text': status.get('proof_target_due_at_text'),
        'proof_target_run_slots_text': status.get('proof_target_run_slots_text'),
        'previous_run_slot_at_text': status.get('previous_run_slot_at_text'),
        'last_proof_qualified_run_at_text': status.get('last_proof_qualified_run_at_text'),
        'has_run_proof': status.get('has_run_proof'),
        'attention_needed': status.get('attention_needed'),
        'status_text': status.get('text'),
        'summary_output_examples': summarize_output_examples(status),
    }

    state = 'ok' if ok else 'attention'
    lines = [f'ai briefing watchdog: {state} - {summary}']
    if reasons:
        lines.append('reasons:')
        lines.extend(f'- {reason}' for reason in reasons)
    if result['proof_progress_text']:
        lines.append(f"proof progress: {result['proof_progress_text']}")
    if required_qualified_runs > 0:
        lines.append(
            f"proof requirement: {proof_qualified_runs}/{required_qualified_runs} gekwalificeerde runs"
        )
    if result['next_run_at_text']:
        lines.append(f"next run: {result['next_run_at_text']}")
    if result['proof_due_at_text']:
        lines.append(f"proof due: {result['proof_due_at_text']}")
    if result['proof_target_due_at_text']:
        lines.append(f"proof target due: {result['proof_target_due_at_text']}")
    if result['proof_target_run_slots_text']:
        lines.append(f"qualifying run slots: {result['proof_target_run_slots_text']}")
    if result['last_proof_qualified_run_at_text']:
        lines.append(f"last qualified run: {result['last_proof_qualified_run_at_text']}")
    text_output = '\n'.join(lines) + '\n'

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
    raise SystemExit(main())
