#!/usr/bin/env python3
import argparse
import importlib.util
import json
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from difflib import get_close_matches
from pathlib import Path
from time import monotonic

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'
PROOF_RECHECK_SCRIPT = ROOT / 'scripts' / 'ai-briefing-proof-recheck.py'
PROOF_RECHECK_PRODUCER_SCRIPT = ROOT / 'scripts' / 'ai-briefing-proof-recheck-producer.py'
WATCHDOG_SCRIPT = ROOT / 'scripts' / 'ai-briefing-watchdog.py'
WATCHDOG_ALERT_SCRIPT = ROOT / 'scripts' / 'ai-briefing-watchdog-alert.py'
WATCHDOG_PRODUCER_SCRIPT = ROOT / 'scripts' / 'ai-briefing-watchdog-producer.py'
STATUSBOARD_SCRIPT = ROOT / 'scripts' / 'statusboard.py'
CLAWDY_BRIEF_SCRIPT = ROOT / 'scripts' / 'clawdy-brief.py'
DEFAULT_REFERENCE_MS = int(datetime(2026, 4, 15, 0, 0, tzinfo=timezone.utc).timestamp() * 1000)
EXPECTED_PROOF_RECHECK_JOB_NAME = 'ai-briefing-proof-recheck-producer'
EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR = '15 9 * * *'
EXPECTED_PROOF_RECHECK_SCHEDULE_TZ = 'Europe/Amsterdam'
EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES = 15


def run_status_json(reference_ms: int | None = None) -> dict:
    cmd = ['python3', str(STATUS_SCRIPT), '--json']
    if reference_ms is not None:
        cmd.extend(['--reference-ms', str(reference_ms)])
    return json.loads(subprocess.check_output(cmd, cwd=ROOT, text=True))


LIVE_STATUS_BASELINE = run_status_json()
CURRENT_PROOF_NEXT_SLOT_AT = LIVE_STATUS_BASELINE['proof_next_qualifying_slot_at']
CURRENT_PROOF_RECHECK_AFTER_AT = LIVE_STATUS_BASELINE['proof_recheck_after_at']
CURRENT_PROOF_TARGET_DUE_AT = LIVE_STATUS_BASELINE['proof_target_due_at']
REFERENCE_MS_BEFORE_SLOT_TOMORROW = CURRENT_PROOF_NEXT_SLOT_AT - ((24 * 60 * 60 + 2 * 60) * 1000)
REFERENCE_MS_NEXT_DAY_BEFORE_SLOT = CURRENT_PROOF_NEXT_SLOT_AT - (2 * 60 * 1000)
REFERENCE_MS_CURRENT_SLOT_GRACE = CURRENT_PROOF_NEXT_SLOT_AT + (5 * 60 * 1000)
REFERENCE_MS_RECHECK_WINDOW_OPEN = CURRENT_PROOF_RECHECK_AFTER_AT
REFERENCE_MS_AFTER_PROOF_DEADLINE = CURRENT_PROOF_TARGET_DUE_AT + (60 * 1000)
STATUS_BEFORE_SLOT_TOMORROW = run_status_json(REFERENCE_MS_BEFORE_SLOT_TOMORROW)
STATUS_NEXT_DAY_BEFORE_SLOT = run_status_json(REFERENCE_MS_NEXT_DAY_BEFORE_SLOT)
STATUS_CURRENT_SLOT_GRACE = run_status_json(REFERENCE_MS_CURRENT_SLOT_GRACE)
STATUS_RECHECK_WINDOW_OPEN = run_status_json(REFERENCE_MS_RECHECK_WINDOW_OPEN)
CURRENT_PROOF_NEXT_SLOT_TEXT = STATUS_BEFORE_SLOT_TOMORROW['proof_wait_until_text']
CURRENT_PROOF_RECHECK_AFTER_TEXT = STATUS_BEFORE_SLOT_TOMORROW['proof_recheck_after_text']
CURRENT_PROOF_CONFIG_HASH = LIVE_STATUS_BASELINE.get('proof_config_hash')


def unique_case_names(case_names: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for case_name in case_names:
        if case_name in seen:
            continue
        seen.add(case_name)
        unique.append(case_name)
    return unique


def emit_unknown_case_error(
    *,
    requested_case_names: list[str],
    unknown_cases: list[str],
    available_case_names: list[str],
    available_case_count: int,
    as_json: bool,
    run_metadata: dict | None = None,
) -> None:
    unique_requested_case_names = unique_case_names(requested_case_names)
    unique_unknown_cases = unique_case_names(unknown_cases)
    selected_case_names = [
        case_name for case_name in unique_requested_case_names
        if case_name in available_case_names
    ]
    suggested_case_names_by_input = {
        case_name: get_close_matches(case_name, available_case_names, n=3, cutoff=0.45)
        for case_name in unique_unknown_cases
    }
    if as_json:
        print(json.dumps({
            'ok': False,
            'error': 'unknown-cases',
            'message': 'onbekende regressiecase opgegeven',
            'requested_case_names': unique_requested_case_names,
            'requested_case_count': len(unique_requested_case_names),
            'selected_case_names': selected_case_names,
            'selected_case_count': len(selected_case_names),
            'unknown_case_names': unique_unknown_cases,
            'unknown_case_count': len(unique_unknown_cases),
            'available_case_names': available_case_names,
            'available_case_count': available_case_count,
            'suggested_case_names_by_input': suggested_case_names_by_input,
            **(run_metadata or {}),
        }, ensure_ascii=False, indent=2))
        return
    if selected_case_names:
        print(
            'geldige regressiecases in dezelfde aanvraag: ' + ', '.join(selected_case_names),
            file=sys.stderr,
        )
    for case_name in unique_unknown_cases:
        print(f'onbekende regressiecase: {case_name}', file=sys.stderr)
        suggestions = suggested_case_names_by_input.get(case_name) or []
        if suggestions:
            print(
                '  suggesties: ' + ', '.join(suggestions),
                file=sys.stderr,
            )


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


DEFAULT_CASES = [
    {
        'name': 'real-run-2026-04-14-0902-failed-summary',
        'path': ROOT / 'tmp' / 'ai-briefing-run-2026-04-14-0902-failed-summary.txt',
        'expect_ok': False,
        'expect_item_count': 10,
        'expect_items_with_source_count': 0,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 10,
        'expect_first3_items_with_source_count': 0,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 10,
            'komma': 9,
            'puntkomma': 6,
            'haakjes': 1,
            'update_datum': 1,
            'datumtekst': 10,
            'vrije_tekst': 10,
            'extra_context': 1,
            'via_context': 1,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 0,
            'Bron:': 10,
            'Datum:': 0,
            'Wat is er nieuw:': 0,
            'Waarom is dit belangrijk:': 0,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'niet elk item heeft een zichtbare bron-URL',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'geen URL 10x',
            'te weinig top-3 items met meerdere bron-URLs',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'invalid-bron-with-urls-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-invalid-bron-with-urls-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 1,
        'expect_items_with_valid_source_line_count': 1,
        'expect_items_with_invalid_source_line_count': 2,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 1,
        'expect_first3_items_with_multiple_sources_count': 1,
        'expect_first3_evidenced_item_count': 1,
        'expect_first3_primary_source_family_count': 1,
        'expect_first3_primary_fresh_item_count': 1,
        'expect_source_url_count': 2,
        'expect_unique_source_url_count': 2,
        'expect_source_domain_count': 2,
        'expect_first3_unique_source_url_count': 2,
        'expect_first3_source_domain_count': 2,
        'expect_invalid_source_issue_counts': {
            'komma': 1,
            'url_leesteken': 1,
            'update_datum': 1,
            'datumtekst': 1,
            'vrije_tekst': 2,
            'via_context': 1,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (2)',
            'te weinig unieke bron-URLs voor aantal items (2/3)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'niet elk top-3 item heeft een geldige Bron:-regel met alleen URLs',
            'te weinig top-3 items met meerdere bron-URLs (1/3, verwacht minstens 3)',
            'vrije tekst 2x',
            'via 1x',
            'update-datum 1x',
        ],
    },
    {
        'name': 'top3-trailing-slash-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-trailing-slash-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-percent-encoding-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-percent-encoding-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'query-encoded-unreserved-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-query-encoded-unreserved-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-path-encoded-unreserved-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-path-encoded-unreserved-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-dot-segment-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-dot-segment-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-encoded-dot-segment-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-encoded-dot-segment-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-double-slash-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-double-slash-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 2,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'format-compliant-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-format-compliant-sample.txt',
        'expect_ok': True,
        'expect_item_count': 4,
        'expect_items_with_source_count': 4,
        'expect_items_with_valid_source_line_count': 4,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 4,
            'Bron:': 4,
            'Datum:': 4,
            'Wat is er nieuw:': 4,
            'Waarom is dit belangrijk:': 4,
            'Relevant voor Christian:': 4,
        },
        'expect_reason_substrings': [],
    },
    {
        'name': 'top3-alt-primary-domains-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-alt-primary-domains-sample.txt',
        'expect_ok': True,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 6,
        'expect_source_domain_count': 6,
        'expect_first3_unique_source_url_count': 6,
        'expect_first3_source_domain_count': 6,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [],
    },
    {
        'name': 'lowercase-labels-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-lowercase-labels-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 5,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 0,
            'Bron:': 0,
            'Datum:': 0,
            'Wat is er nieuw:': 0,
            'Waarom is dit belangrijk:': 0,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'verplichte exacte veldlabels per item kloppen niet',
            'niet elk item volgt de exacte labelvolgorde (0/3)',
        ],
    },
    {
        'name': 'markdown-bron-links-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-markdown-bron-links-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 3,
            'haakjes': 3,
            'vierkante_haken': 3,
            'vrije_tekst': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'haakjes 3x',
            'vrije tekst 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'angle-bracket-bron-links-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-angle-bracket-bron-links-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 3,
            'hoekhaken': 3,
            'vrije_tekst': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'hoekhaken 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'square-bracket-bron-urls-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-square-bracket-bron-urls-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 3,
            'vierkante_haken': 3,
            'vrije_tekst': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'vierkante haken 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'unicode-pipe-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-unicode-pipe-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_invalid_source_issue_counts': {
            'pipe_variant': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'pipe-variant 3x',
            'te weinig top-3 items met meerdere bron-URLs (0/3, verwacht minstens 3)',
            'te weinig top-3 items met primaire bron én verse datum (0/3 binnen 48 uur)',
        ],
    },
    {
        'name': 'bullet-separator-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-bullet-separator-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'bullet_separator': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'bullet-separator 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'semicolon-separated-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-semicolon-separated-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'puntkomma': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'puntkomma 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'quoted-bron-urls-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-quoted-bron-urls-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 3,
            'aanhalingstekens': 3,
            'vrije_tekst': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'aanhalingstekens 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'schemeless-bron-urls-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-schemeless-bron-urls-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 2,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 2,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 3,
            'vrije_tekst': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een zichtbare bron-URL (2/3)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'geen URL 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'backtick-bron-urls-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-backtick-bron-urls-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_invalid_source_issue_counts': {
            'geen_url': 3,
            'backticks': 3,
            'vrije_tekst': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'backticks 3x',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'top3-two-of-three-multi-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-two-of-three-multi-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 4,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-same-domain-multi-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-same-domain-multi-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_multiple_sources_count': 3,
        'expect_items_with_multi_domain_sources_count': 0,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_multi_domain_sources_count': 0,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 6,
        'expect_source_domain_count': 3,
        'expect_first3_unique_source_url_count': 6,
        'expect_first3_source_domain_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (0/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-reused-source-urls-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-reused-source-urls-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 2,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'top-3 items hergebruiken bron-URLs (2/3 uniek)',
        ],
    },
    {
        'name': 'duplicate-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-duplicate-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_source_domain_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_first3_source_domain_count': 0,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 0,
            'Datum:': 0,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'niet alle itemtitels zijn uniek (2/3)',
            'OpenAI brengt GPT-update uit x2',
        ],
    },
    {
        'name': 'duplicate-top3-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-duplicate-top3-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 2,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 3,
        'expect_unique_source_url_count': 2,
        'expect_source_domain_count': 2,
        'expect_first3_unique_source_url_count': 2,
        'expect_first3_source_domain_count': 2,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'te weinig unieke bron-URLs voor aantal items (2/3)',
            'top-3 items hergebruiken bron-URLs (2/3 uniek)',
        ],
    },
    {
        'name': 'future-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-future-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 1,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 1,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_source_domain_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_first3_source_domain_count': 0,
        'expect_future_dated_item_count': 1,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 0,
            'Datum:': 0,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'verdachte toekomstige datums in briefing (1 item(s), tolerantie 1 dag)',
        ],
    },
    {
        'name': 'multi-source-weak-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-multi-source-weak-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 3,
        'expect_unique_source_url_count': 3,
        'expect_source_domain_count': 3,
        'expect_first3_unique_source_url_count': 3,
        'expect_first3_source_domain_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (0/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-nonprimary-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-nonprimary-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 3,
        'expect_unique_source_url_count': 3,
        'expect_source_domain_count': 3,
        'expect_first3_unique_source_url_count': 3,
        'expect_first3_source_domain_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'geen herkenbare primaire bron tussen URLs',
            'te weinig primaire bronfamilies in top 3 (0)',
        ],
    },
    {
        'name': 'top3-same-primary-family-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-same-primary-family-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 1,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 3,
        'expect_unique_source_url_count': 3,
        'expect_source_domain_count': 3,
        'expect_first3_unique_source_url_count': 3,
        'expect_first3_source_domain_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 0,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 0,
        },
        'expect_reason_substrings': [
            'te weinig primaire bronfamilies in top 3 (1)',
        ],
    },
    {
        'name': 'top3-duplicate-url-in-item-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-duplicate-url-in-item-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 4,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'Anthropic bundelt prompt caching en docs-updates',
        ],
    },
    {
        'name': 'top3-tracking-param-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-tracking-param-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 4,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'Anthropic bundelt prompt caching en docs-updates',
        ],
    },
    {
        'name': 'top3-default-port-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-default-port-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'OpenAI publiceert GPT-4.1 API-updates',
        ],
    },
    {
        'name': 'top3-query-order-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-query-order-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 4,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'Anthropic publiceert prompt caching update met queryvolgorde-variant',
        ],
    },
    {
        'name': 'top3-www-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-www-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
            'OpenAI publiceert Responses API-update via www-variant',
        ],
    },
    {
        'name': 'top3-host-case-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-host-case-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
            'OpenAI publiceert Responses API update via host-case-variant',
        ],
    },
    {
        'name': 'top3-host-trailing-dot-duplicate-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-host-trailing-dot-duplicate-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_source_url_count': 6,
        'expect_unique_source_url_count': 5,
        'expect_source_domain_count': 5,
        'expect_first3_unique_source_url_count': 5,
        'expect_first3_source_domain_count': 5,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig top-3 items met meerdere bron-URLs (2/3, verwacht minstens 3)',
            'te weinig top-3 items met bron-URLs uit meerdere domeinen (2/3, verwacht minstens 3)',
            'OpenAI scherpt Responses API logging aan',
        ],
    },
    {
        'name': 'top3-missing-primary-source-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-missing-primary-source-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 2,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 2,
        'expect_first3_primary_fresh_item_count': 2,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'niet elk top-3 item heeft een herkenbare primaire bron (2/3)',
            'Onderzoekers bespreken nieuwe agent benchmark voor tool calling',
        ],
    },
    {
        'name': 'trailing-punctuation-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-trailing-punctuation-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 1,
        'expect_items_with_invalid_source_line_count': 2,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 1,
        'expect_first3_items_with_multiple_sources_count': 1,
        'expect_first3_items_with_primary_source_count': 1,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 1,
        'expect_first3_primary_source_family_count': 2,
        'expect_first3_primary_fresh_item_count': 1,
        'expect_source_url_count': 2,
        'expect_unique_source_url_count': 2,
        'expect_source_domain_count': 2,
        'expect_first3_unique_source_url_count': 2,
        'expect_first3_source_domain_count': 2,
        'expect_invalid_source_issue_counts': {
            'url_leesteken': 2,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (2)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs',
            'URL-leesteken 2x',
            'te weinig top-3 items met zowel bron als recente datum (1/3)',
        ],
    },
    {
        'name': 'dangling-pipe-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-dangling-pipe-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_source_domain_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_first3_source_domain_count': 0,
        'expect_invalid_source_issue_counts': {
            'lege_separator': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_items_with_exact_field_order_count': 3,
        'expect_items_with_field_order_mismatch_count': 0,
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs (0/3)',
            'patronen: lege separator 3x',
            'top3 patronen: lege separator 3x',
            'te weinig top-3 items met meerdere bron-URLs (0/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'slash-separated-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-slash-separated-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_source_domain_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_first3_source_domain_count': 0,
        'expect_invalid_source_issue_counts': {
            'slash_separator': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_items_with_exact_field_order_count': 3,
        'expect_items_with_field_order_mismatch_count': 0,
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs (0/3)',
            'patronen: slash-separator 3x',
            'top3 patronen: slash-separator 3x',
            'te weinig top-3 items met meerdere bron-URLs (0/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'ampersand-separated-bron-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-ampersand-separated-bron-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 0,
        'expect_items_with_invalid_source_line_count': 3,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_items_with_primary_source_count': 0,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_source_url_count': 0,
        'expect_unique_source_url_count': 0,
        'expect_source_domain_count': 0,
        'expect_first3_unique_source_url_count': 0,
        'expect_first3_source_domain_count': 0,
        'expect_invalid_source_issue_counts': {
            'ampersand_separator': 3,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_items_with_exact_field_order_count': 3,
        'expect_items_with_field_order_mismatch_count': 0,
        'expect_reason_substrings': [
            'te weinig geldige bron-URLs op geldige Bron:-regels (0)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs (0/3)',
            'patronen: ampersand-separator 3x',
            'top3 patronen: ampersand-separator 3x',
            'te weinig top-3 items met meerdere bron-URLs (0/3, verwacht minstens 3)',
        ],
    },
    {
        'name': 'top3-missing-date-line-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-top3-missing-date-line-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_explicit_dated_item_count': 2,
        'expect_explicit_recent_dated_first3_count': 2,
        'expect_explicit_fresh_dated_first3_count': 2,
        'expect_first3_evidenced_item_count': 2,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 2,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 2,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_reason_substrings': [
            'verplichte exacte veldlabels per item kloppen niet (Datum: 2/3)',
            'niet elk item heeft een expliciete Datum:-regel (2/3)',
            'te weinig top-3 items met zowel bron als recente datum (2/3)',
            'OpenAI verbreedt agents-SDK documentatie met nieuwe voorbeelden',
        ],
    },
    {
        'name': 'label-order-mismatch-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-label-order-mismatch-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_items_with_exact_field_order_count': 2,
        'expect_items_with_field_order_mismatch_count': 1,
        'expect_reason_substrings': [
            'niet elk item volgt de exacte labelvolgorde (2/3)',
            'OpenAI rolt nieuwe Responses API-updates uit -> Titel: > Datum: > Bron:',
        ],
    },
    {
        'name': 'bullet-labels-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-bullet-labels-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 0,
            'Waarom is dit belangrijk:': 0,
            'Relevant voor Christian:': 0,
        },
        'expect_items_with_exact_field_order_count': 0,
        'expect_items_with_field_order_mismatch_count': 3,
        'expect_reason_substrings': [
            'verplichte exacte veldlabels per item kloppen niet (Wat is er nieuw: 0/3, Waarom is dit belangrijk: 0/3, Relevant voor Christian: 0/3)',
            'niet elk item volgt de exacte labelvolgorde (0/3)',
            'OpenAI scherpt Responses API voorbeelden aan voor toolgebruik -> Titel: > Bron: > Datum:',
        ],
    },
    {
        'name': 'numbered-title-headings-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-numbered-title-headings-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 3,
        'expect_items_with_valid_source_line_count': 3,
        'expect_items_with_invalid_source_line_count': 0,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_valid_source_line_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_items_with_primary_source_count': 3,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 3,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 3,
        'expect_invalid_source_issue_counts': {},
        'expect_exact_field_line_counts': {
            'Titel:': 0,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_items_with_exact_field_order_count': 3,
        'expect_items_with_field_order_mismatch_count': 0,
        'expect_numbered_title_heading_count': 3,
        'expect_reason_substrings': [
            'verplichte exacte veldlabels per item kloppen niet (Titel: 0/3)',
            'genummerde itemkoppen gevonden (3)',
            'OpenAI verduidelijkt Responses API voor toolgebruik',
        ],
    },
    {
        'name': 'empty-bron-line-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-empty-bron-line-sample.txt',
        'expect_ok': False,
        'expect_item_count': 3,
        'expect_items_with_source_count': 2,
        'expect_items_with_valid_source_line_count': 2,
        'expect_items_with_invalid_source_line_count': 1,
        'expect_first3_items_with_source_count': 2,
        'expect_first3_items_with_valid_source_line_count': 2,
        'expect_first3_items_with_multiple_sources_count': 2,
        'expect_first3_items_with_primary_source_count': 2,
        'expect_explicit_dated_item_count': 3,
        'expect_explicit_recent_dated_first3_count': 3,
        'expect_explicit_fresh_dated_first3_count': 3,
        'expect_first3_evidenced_item_count': 2,
        'expect_first3_primary_source_family_count': 3,
        'expect_first3_primary_fresh_item_count': 2,
        'expect_invalid_source_issue_counts': {
            'leeg': 1,
        },
        'expect_exact_field_line_counts': {
            'Titel:': 3,
            'Bron:': 3,
            'Datum:': 3,
            'Wat is er nieuw:': 3,
            'Waarom is dit belangrijk:': 3,
            'Relevant voor Christian:': 3,
        },
        'expect_items_with_exact_field_order_count': 3,
        'expect_items_with_field_order_mismatch_count': 0,
        'expect_reason_substrings': [
            'niet elk item heeft een zichtbare bron-URL (2/3)',
            'niet elk item heeft een geldige Bron:-regel met alleen URLs (2/3)',
            'patronen: leeg 1x',
            'niet elk top-3 item heeft een zichtbare bron-URL (2/3)',
            'niet elk top-3 item heeft een geldige Bron:-regel met alleen URLs (2/3)',
            'top3 patronen: leeg 1x',
        ],
    },
]

STATUS_PHASE_CASES = [
    {
        'name': 'status-before-slot-waits-for-run',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_blocker_kind': 'time-gated-next-slot',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_proof_recheck_window_open': False,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            f'hercheck vanaf {CURRENT_PROOF_RECHECK_AFTER_TEXT}',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
        ],
    },
    {
        'name': 'status-next-day-before-slot-waits-for-run',
        'reference_ms': REFERENCE_MS_NEXT_DAY_BEFORE_SLOT,
        'expect_proof_state': 'waiting-next-scheduled-run',
        'expect_proof_blocker_kind': 'time-gated-next-slot',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_proof_recheck_window_open': False,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            f'hercheck vanaf {CURRENT_PROOF_RECHECK_AFTER_TEXT}',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
        ],
    },
    {
        'name': 'status-current-slot-grace-window',
        'reference_ms': REFERENCE_MS_CURRENT_SLOT_GRACE,
        'expect_proof_state': 'current-slot-grace-window',
        'expect_proof_blocker_kind': 'grace-window-before-recheck',
        'expect_proof_next_action_kind': 'wait-for-recheck-window',
        'expect_proof_recheck_window_open': False,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            f'kwalificatierun van {CURRENT_PROOF_NEXT_SLOT_TEXT} zit in grace-window',
            f'hercheck vanaf {CURRENT_PROOF_RECHECK_AFTER_TEXT}',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
        ],
    },
    {
        'name': 'status-recheck-window-open',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_blocker_kind': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_proof_recheck_window_open': True,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
        ],
    },
]

STATUS_STDOUT_CASES = [
    {
        'name': 'status-stdout-json-before-slot-has-runtime-metadata',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_last_run_config_relation_text': STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
        ],
    },
    {
        'name': 'status-stdout-json-open-window-has-runtime-metadata',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_last_run_config_relation_text': STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
        ],
    },
]

STATUS_SUMMARY_AUDIT_CASES = [
    {
        'name': 'status-summary-audit-cli-keeps-runtime-metadata',
        'path': ROOT / 'tmp' / 'ai-briefing-format-compliant-sample.txt',
    },
]

PROOF_RECHECK_CASES = [
    {
        'name': 'proof-recheck-before-slot-too-early',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_state': 'waiting',
        'expect_exit_code': 2,
        'expect_result_kind': 'too-early',
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_blocker_kind': 'time-gated-next-slot',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_proof_recheck_ready': False,
        'expect_proof_wait_until_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_at'),
        'expect_proof_wait_until_text': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_text'),
        'expect_proof_wait_until_reason_text': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_reason_text'),
        'expect_proof_recheck_after_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_recheck_after_at'),
        'expect_proof_wait_until_remaining_ms': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_remaining_ms'),
        'expect_proof_next_qualifying_slot_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_next_qualifying_slot_at'),
        'expect_proof_next_qualifying_slot_remaining_ms': STATUS_BEFORE_SLOT_TOMORROW.get('proof_next_qualifying_slot_remaining_ms'),
        'expect_proof_target_due_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_target_due_at'),
        'expect_proof_target_due_at_if_next_slot_missed': STATUS_BEFORE_SLOT_TOMORROW.get('proof_target_due_at_if_next_slot_missed'),
        'expect_proof_schedule_slip_ms': STATUS_BEFORE_SLOT_TOMORROW.get('proof_schedule_slip_ms'),
        'expect_status_ok': False,
        'expect_watchdog_ok': False,
        'expect_proof_config_hash_present': True,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            'hercheck nog te vroeg, wacht op kwalificatierun en hercheckvenster',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            f'hercheck vanaf {CURRENT_PROOF_RECHECK_AFTER_TEXT}',
            'proof-recheck-cronstatus: ok',
            f'config {CURRENT_PROOF_CONFIG_HASH}',
            'laatste run hoorde nog bij de vorige config',
        ],
        'expect_plain_not_substrings': [
            '| 2026-04-21 09:15 CEST |',
            '| 2026-04-22 09:15 CEST |',
        ],
    },
    {
        'name': 'proof-recheck-grace-window-too-early',
        'reference_ms': REFERENCE_MS_CURRENT_SLOT_GRACE,
        'expect_state': 'waiting',
        'expect_exit_code': 2,
        'expect_result_kind': 'too-early',
        'expect_proof_state': 'current-slot-grace-window',
        'expect_proof_blocker_kind': 'grace-window-before-recheck',
        'expect_proof_next_action_kind': 'wait-for-recheck-window',
        'expect_proof_recheck_ready': False,
        'expect_proof_wait_until_at': STATUS_CURRENT_SLOT_GRACE.get('proof_wait_until_at'),
        'expect_proof_wait_until_text': STATUS_CURRENT_SLOT_GRACE.get('proof_wait_until_text'),
        'expect_proof_wait_until_reason_text': STATUS_CURRENT_SLOT_GRACE.get('proof_wait_until_reason_text'),
        'expect_proof_recheck_after_at': STATUS_CURRENT_SLOT_GRACE.get('proof_recheck_after_at'),
        'expect_proof_wait_until_remaining_ms': STATUS_CURRENT_SLOT_GRACE.get('proof_wait_until_remaining_ms'),
        'expect_proof_next_qualifying_slot_at': STATUS_CURRENT_SLOT_GRACE.get('proof_next_qualifying_slot_at'),
        'expect_proof_next_qualifying_slot_remaining_ms': STATUS_CURRENT_SLOT_GRACE.get('proof_next_qualifying_slot_remaining_ms'),
        'expect_proof_target_due_at': STATUS_CURRENT_SLOT_GRACE.get('proof_target_due_at'),
        'expect_proof_target_due_at_if_next_slot_missed': STATUS_CURRENT_SLOT_GRACE.get('proof_target_due_at_if_next_slot_missed'),
        'expect_proof_schedule_slip_ms': STATUS_CURRENT_SLOT_GRACE.get('proof_schedule_slip_ms'),
        'expect_status_ok': False,
        'expect_watchdog_ok': False,
        'expect_proof_config_hash_present': True,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            'hercheck nog te vroeg, wacht op kwalificatierun en hercheckvenster',
            f'kwalificatierun van {CURRENT_PROOF_NEXT_SLOT_TEXT} zit in grace-window',
            f'hercheck vanaf {CURRENT_PROOF_RECHECK_AFTER_TEXT}',
            'proof-recheck-cronstatus: ok',
            f'config {CURRENT_PROOF_CONFIG_HASH}',
            'laatste run hoorde nog bij de vorige config',
        ],
        'expect_plain_not_substrings': [
            '| 2026-04-21 09:15 CEST |',
            '| 2026-04-22 09:15 CEST |',
        ],
    },
    {
        'name': 'proof-recheck-open-window-needs-attention',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_state': 'attention',
        'expect_exit_code': 3,
        'expect_result_kind': 'attention-needed',
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_blocker_kind': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_proof_recheck_ready': True,
        'expect_proof_wait_until_at': None,
        'expect_proof_wait_until_text': None,
        'expect_proof_wait_until_reason_text': None,
        'expect_proof_recheck_after_at': STATUS_RECHECK_WINDOW_OPEN.get('proof_recheck_after_at'),
        'expect_proof_wait_until_remaining_ms': None,
        'expect_proof_next_qualifying_slot_at': STATUS_RECHECK_WINDOW_OPEN.get('proof_next_qualifying_slot_at'),
        'expect_proof_next_qualifying_slot_remaining_ms': STATUS_RECHECK_WINDOW_OPEN.get('proof_next_qualifying_slot_remaining_ms'),
        'expect_proof_target_due_at': STATUS_RECHECK_WINDOW_OPEN.get('proof_target_due_at'),
        'expect_proof_target_due_at_if_next_slot_missed': STATUS_RECHECK_WINDOW_OPEN.get('proof_target_due_at_if_next_slot_missed'),
        'expect_proof_schedule_slip_ms': STATUS_RECHECK_WINDOW_OPEN.get('proof_schedule_slip_ms'),
        'expect_status_ok': False,
        'expect_watchdog_ok': False,
        'expect_proof_config_hash_present': True,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_substrings': [
            'hercheckvenster is open, maar bewijsdoel is nog niet gehaald',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            'daarna draai: python3 scripts/ai-briefing-status.py --json ; python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3',
            'proof-recheck-cronstatus: ok',
            f'config {CURRENT_PROOF_CONFIG_HASH}',
            'laatste run hoorde nog bij de vorige config',
        ],
        'expect_plain_not_substrings': [
            '| 2026-04-21 09:15 CEST |',
            '| 2026-04-22 09:15 CEST |',
        ],
    },
]

PROOF_RECHECK_PRODUCER_CASES = [
    {
        'name': 'proof-recheck-producer-before-slot-too-early',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_exit_code': 2,
        'expect_state': 'waiting',
        'expect_result_kind': 'too-early',
        'expect_reference_now_text': STATUS_BEFORE_SLOT_TOMORROW.get('reference_now_text'),
        'expect_status_ok': False,
        'expect_watchdog_ok': False,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_blocker_kind': 'time-gated-next-slot',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_proof_recheck_ready': False,
        'expect_proof_wait_until_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_at'),
        'expect_proof_wait_until_text': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_text'),
        'expect_proof_wait_until_reason_text': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_reason_text'),
        'expect_proof_recheck_after_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_recheck_after_at'),
        'expect_proof_wait_until_remaining_ms': STATUS_BEFORE_SLOT_TOMORROW.get('proof_wait_until_remaining_ms'),
        'expect_proof_next_qualifying_slot_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_next_qualifying_slot_at'),
        'expect_proof_next_qualifying_slot_remaining_ms': STATUS_BEFORE_SLOT_TOMORROW.get('proof_next_qualifying_slot_remaining_ms'),
        'expect_proof_target_due_at': STATUS_BEFORE_SLOT_TOMORROW.get('proof_target_due_at'),
        'expect_proof_target_due_at_if_next_slot_missed': STATUS_BEFORE_SLOT_TOMORROW.get('proof_target_due_at_if_next_slot_missed'),
        'expect_proof_schedule_slip_ms': STATUS_BEFORE_SLOT_TOMORROW.get('proof_schedule_slip_ms'),
        'expect_quiet_substrings': [
            'ai-briefing-proof-recheck-producer: all',
            'resultaat: too-early',
            'proof-recheck-cronstatus: ok',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
        ],
        'expect_quiet_absent_substrings': [
            '--json --consumer-bundle board-suite: exit=',
            '| 2026-04-21 09:15 CEST |',
            '| 2026-04-22 09:15 CEST |',
        ],
        'expect_json_substrings': [
            'hercheck nog te vroeg, wacht op kwalificatierun en hercheckvenster',
            f"referentietijd {STATUS_BEFORE_SLOT_TOMORROW.get('reference_now_text')}",
        ],
        'expect_proof_config_hash_present': True,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_artifact_substrings': [
            'hercheck nog te vroeg, wacht op kwalificatierun en hercheckvenster',
            'proof-recheck-cronstatus: ok',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
        ],
    },
    {
        'name': 'proof-recheck-producer-open-window-needs-attention',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_exit_code': 3,
        'expect_state': 'attention',
        'expect_result_kind': 'attention-needed',
        'expect_reference_now_text': STATUS_RECHECK_WINDOW_OPEN.get('reference_now_text'),
        'expect_status_ok': False,
        'expect_watchdog_ok': False,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_blocker_kind': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_proof_recheck_ready': True,
        'expect_proof_wait_until_at': None,
        'expect_proof_wait_until_text': None,
        'expect_proof_wait_until_reason_text': None,
        'expect_proof_recheck_after_at': STATUS_RECHECK_WINDOW_OPEN.get('proof_recheck_after_at'),
        'expect_proof_wait_until_remaining_ms': None,
        'expect_proof_next_qualifying_slot_at': STATUS_RECHECK_WINDOW_OPEN.get('proof_next_qualifying_slot_at'),
        'expect_proof_next_qualifying_slot_remaining_ms': STATUS_RECHECK_WINDOW_OPEN.get('proof_next_qualifying_slot_remaining_ms'),
        'expect_proof_target_due_at': STATUS_RECHECK_WINDOW_OPEN.get('proof_target_due_at'),
        'expect_proof_target_due_at_if_next_slot_missed': STATUS_RECHECK_WINDOW_OPEN.get('proof_target_due_at_if_next_slot_missed'),
        'expect_proof_schedule_slip_ms': STATUS_RECHECK_WINDOW_OPEN.get('proof_schedule_slip_ms'),
        'expect_quiet_substrings': [
            'ai-briefing-proof-recheck-producer: all',
            'resultaat: attention-needed',
            'proof-recheck-cronstatus: ok',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
        ],
        'expect_quiet_absent_substrings': [
            '--json --consumer-bundle board-suite: exit=',
            '| 2026-04-21 09:15 CEST |',
            '| 2026-04-22 09:15 CEST |',
        ],
        'expect_json_substrings': [
            'hercheckvenster is open, maar bewijsdoel is nog niet gehaald',
            f"referentietijd {STATUS_RECHECK_WINDOW_OPEN.get('reference_now_text')}",
        ],
        'expect_proof_config_hash_present': True,
        'expect_proof_recheck_schedule_audit_ok': True,
        'expect_proof_recheck_schedule_matches_grace': True,
        'expect_artifact_substrings': [
            'hercheckvenster is open, maar bewijsdoel is nog niet gehaald',
            'proof-recheck-cronstatus: ok',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
        ],
    },
]

BRIEF_CONSUMER_CASES = [
    {
        'name': 'statusboard-before-slot-keeps-proof-recheck-cronstatus',
        'script': STATUSBOARD_SCRIPT,
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_proof_plan_text': STATUS_BEFORE_SLOT_TOMORROW['proof_plan_text'],
        'expect_last_run_config_relation_text': STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            STATUS_BEFORE_SLOT_TOMORROW['proof_freshness_text'],
            STATUS_BEFORE_SLOT_TOMORROW['proof_plan_text'],
            STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
        ],
    },
    {
        'name': 'statusboard-open-window-keeps-proof-recheck-cronstatus',
        'script': STATUSBOARD_SCRIPT,
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_proof_plan_text': STATUS_RECHECK_WINDOW_OPEN['proof_plan_text'],
        'expect_last_run_config_relation_text': STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            STATUS_RECHECK_WINDOW_OPEN['proof_freshness_text'],
            STATUS_RECHECK_WINDOW_OPEN['proof_plan_text'],
            STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
        ],
    },
    {
        'name': 'clawdy-brief-before-slot-keeps-proof-recheck-cronstatus',
        'script': CLAWDY_BRIEF_SCRIPT,
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_proof_plan_text': STATUS_BEFORE_SLOT_TOMORROW['proof_plan_text'],
        'expect_last_run_config_relation_text': STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            STATUS_BEFORE_SLOT_TOMORROW['proof_freshness_text'],
            STATUS_BEFORE_SLOT_TOMORROW['proof_plan_text'],
            STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
        ],
    },
    {
        'name': 'clawdy-brief-open-window-keeps-proof-recheck-cronstatus',
        'script': CLAWDY_BRIEF_SCRIPT,
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_proof_plan_text': STATUS_RECHECK_WINDOW_OPEN['proof_plan_text'],
        'expect_last_run_config_relation_text': STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            STATUS_RECHECK_WINDOW_OPEN['proof_freshness_text'],
            STATUS_RECHECK_WINDOW_OPEN['proof_plan_text'],
            STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
        ],
    },
]

WATCHDOG_ALERT_CASES = [
    {
        'name': 'watchdog-alert-before-slot-keeps-proof-recheck-cronstatus',
        'mode': 'proof-progress',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_require_qualified_runs': 3,
        'expect_no_reply': False,
        'expect_suppressed_before_proof_deadline': False,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
        ],
    },
    {
        'name': 'watchdog-alert-open-window-keeps-proof-recheck-cronstatus',
        'mode': 'proof-progress',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_require_qualified_runs': 3,
        'expect_no_reply': False,
        'expect_suppressed_before_proof_deadline': False,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
        ],
    },
    {
        'name': 'watchdog-alert-proof-target-check-suppresses-before-deadline',
        'mode': 'proof-target-check',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_require_qualified_runs': 3,
        'expect_no_reply': True,
        'expect_suppressed_before_proof_deadline': True,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_text_output': 'NO_REPLY',
    },
    {
        'name': 'watchdog-alert-proof-target-check-board-suite-keeps-no-reply-before-deadline',
        'mode': 'proof-target-check',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_require_qualified_runs': 3,
        'expect_no_reply': True,
        'expect_suppressed_before_proof_deadline': True,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_text_output': 'NO_REPLY',
        'consumer_bundle': 'board-suite',
    },
    {
        'name': 'watchdog-alert-proof-target-check-unsuppresses-after-deadline',
        'mode': 'proof-target-check',
        'reference_ms': REFERENCE_MS_AFTER_PROOF_DEADLINE,
        'expect_require_qualified_runs': 3,
        'expect_no_reply': False,
        'expect_suppressed_before_proof_deadline': False,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'kwalificatie-slots',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
        ],
    },
    {
        'name': 'watchdog-alert-proof-target-check-board-suite-unsuppresses-after-deadline',
        'mode': 'proof-target-check',
        'reference_ms': REFERENCE_MS_AFTER_PROOF_DEADLINE,
        'expect_require_qualified_runs': 3,
        'expect_no_reply': False,
        'expect_suppressed_before_proof_deadline': False,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'kwalificatie-slots',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
        ],
        'consumer_bundle': 'board-suite',
    },
]

WATCHDOG_PRODUCER_CASES = [
    {
        'name': 'watchdog-producer-before-slot-keeps-proof-recheck-cronstatus',
        'mode': 'proof-all',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_exit_code': 2,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
            ((STATUS_BEFORE_SLOT_TOMORROW.get('proof_freshness') or {}).get('text') or ''),
        ],
    },
    {
        'name': 'watchdog-producer-proof-board-before-slot-keeps-proof-recheck-cronstatus',
        'mode': 'proof-board',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_exit_code': 2,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
            ((STATUS_BEFORE_SLOT_TOMORROW.get('proof_freshness') or {}).get('text') or ''),
        ],
    },
    {
        'name': 'watchdog-producer-proof-eventlog-before-slot-keeps-proof-recheck-cronstatus',
        'mode': 'proof-eventlog',
        'reference_ms': REFERENCE_MS_BEFORE_SLOT_TOMORROW,
        'expect_exit_code': 2,
        'expect_proof_state': 'waiting-next-scheduled-run-tomorrow',
        'expect_proof_next_action_kind': 'wait-then-recheck',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            f'wacht op geplande kwalificatierun {CURRENT_PROOF_NEXT_SLOT_TEXT}',
            STATUS_BEFORE_SLOT_TOMORROW['last_run_config_relation_text'],
            ((STATUS_BEFORE_SLOT_TOMORROW.get('proof_freshness') or {}).get('text') or ''),
        ],
    },
    {
        'name': 'watchdog-producer-open-window-keeps-proof-recheck-cronstatus',
        'mode': 'proof-all',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_exit_code': 2,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
            ((STATUS_RECHECK_WINDOW_OPEN.get('proof_freshness') or {}).get('text') or ''),
        ],
    },
    {
        'name': 'watchdog-producer-proof-board-open-window-keeps-proof-recheck-cronstatus',
        'mode': 'proof-board',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_exit_code': 2,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
            ((STATUS_RECHECK_WINDOW_OPEN.get('proof_freshness') or {}).get('text') or ''),
        ],
    },
    {
        'name': 'watchdog-producer-proof-eventlog-open-window-keeps-proof-recheck-cronstatus',
        'mode': 'proof-eventlog',
        'reference_ms': REFERENCE_MS_RECHECK_WINDOW_OPEN,
        'expect_exit_code': 2,
        'expect_proof_state': 'recheck-window-open',
        'expect_proof_next_action_kind': 'recheck-now',
        'expect_text_substrings': [
            'proof-recheck-cronstatus: ok',
            'proof-recheck-cron ok (09:15 Europe/Amsterdam, 15m na daily-ai-update en gelijk aan grace-window)',
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
            STATUS_RECHECK_WINDOW_OPEN['last_run_config_relation_text'],
            ((STATUS_RECHECK_WINDOW_OPEN.get('proof_freshness') or {}).get('text') or ''),
        ],
    },
]


def load_status_module():
    spec = importlib.util.spec_from_file_location('ai_briefing_status', STATUS_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_proof_recheck_producer_module():
    spec = importlib.util.spec_from_file_location('ai_briefing_proof_recheck_producer', PROOF_RECHECK_PRODUCER_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def evaluate_case(module, case):
    path = Path(case['path'])
    summary_text = path.read_text(encoding='utf-8')
    audit = module.audit_summary_output(summary_text, reference_ms=case.get('reference_ms', DEFAULT_REFERENCE_MS))
    failures = []
    if audit.get('ok') != case['expect_ok']:
        failures.append(f"ok verwacht {case['expect_ok']}, kreeg {audit.get('ok')}")
    if 'expect_item_count' in case and audit.get('item_count') != case['expect_item_count']:
        failures.append(f"item_count verwacht {case['expect_item_count']}, kreeg {audit.get('item_count')}")
    if 'expect_items_with_source_count' in case and audit.get('items_with_source_count') != case['expect_items_with_source_count']:
        failures.append(
            f"items_with_source_count verwacht {case['expect_items_with_source_count']}, kreeg {audit.get('items_with_source_count')}"
        )
    if (
        'expect_items_with_multiple_sources_count' in case
        and audit.get('items_with_multiple_sources_count') != case['expect_items_with_multiple_sources_count']
    ):
        failures.append(
            'items_with_multiple_sources_count verwacht '
            f"{case['expect_items_with_multiple_sources_count']}, kreeg {audit.get('items_with_multiple_sources_count')}"
        )
    if (
        'expect_items_with_multi_domain_sources_count' in case
        and audit.get('items_with_multi_domain_sources_count') != case['expect_items_with_multi_domain_sources_count']
    ):
        failures.append(
            'items_with_multi_domain_sources_count verwacht '
            f"{case['expect_items_with_multi_domain_sources_count']}, kreeg {audit.get('items_with_multi_domain_sources_count')}"
        )
    if (
        'expect_items_with_valid_source_line_count' in case
        and audit.get('items_with_valid_source_line_count') != case['expect_items_with_valid_source_line_count']
    ):
        failures.append(
            'items_with_valid_source_line_count verwacht '
            f"{case['expect_items_with_valid_source_line_count']}, kreeg {audit.get('items_with_valid_source_line_count')}"
        )
    if (
        'expect_items_with_invalid_source_line_count' in case
        and audit.get('items_with_invalid_source_line_count') != case['expect_items_with_invalid_source_line_count']
    ):
        failures.append(
            'items_with_invalid_source_line_count verwacht '
            f"{case['expect_items_with_invalid_source_line_count']}, kreeg {audit.get('items_with_invalid_source_line_count')}"
        )
    if 'expect_first3_items_with_source_count' in case and audit.get('first3_items_with_source_count') != case['expect_first3_items_with_source_count']:
        failures.append(
            'first3_items_with_source_count verwacht '
            f"{case['expect_first3_items_with_source_count']}, kreeg {audit.get('first3_items_with_source_count')}"
        )
    if (
        'expect_first3_items_with_valid_source_line_count' in case
        and audit.get('first3_items_with_valid_source_line_count') != case['expect_first3_items_with_valid_source_line_count']
    ):
        failures.append(
            'first3_items_with_valid_source_line_count verwacht '
            f"{case['expect_first3_items_with_valid_source_line_count']}, kreeg {audit.get('first3_items_with_valid_source_line_count')}"
        )
    if (
        'expect_first3_items_with_multiple_sources_count' in case
        and audit.get('first3_items_with_multiple_sources_count') != case['expect_first3_items_with_multiple_sources_count']
    ):
        failures.append(
            'first3_items_with_multiple_sources_count verwacht '
            f"{case['expect_first3_items_with_multiple_sources_count']}, kreeg {audit.get('first3_items_with_multiple_sources_count')}"
        )
    if (
        'expect_first3_items_with_multi_domain_sources_count' in case
        and audit.get('first3_items_with_multi_domain_sources_count') != case['expect_first3_items_with_multi_domain_sources_count']
    ):
        failures.append(
            'first3_items_with_multi_domain_sources_count verwacht '
            f"{case['expect_first3_items_with_multi_domain_sources_count']}, kreeg {audit.get('first3_items_with_multi_domain_sources_count')}"
        )
    if (
        'expect_first3_items_with_primary_source_count' in case
        and audit.get('first3_items_with_primary_source_count') != case['expect_first3_items_with_primary_source_count']
    ):
        failures.append(
            'first3_items_with_primary_source_count verwacht '
            f"{case['expect_first3_items_with_primary_source_count']}, kreeg {audit.get('first3_items_with_primary_source_count')}"
        )
    if (
        'expect_first3_evidenced_item_count' in case
        and audit.get('first3_evidenced_item_count') != case['expect_first3_evidenced_item_count']
    ):
        failures.append(
            'first3_evidenced_item_count verwacht '
            f"{case['expect_first3_evidenced_item_count']}, kreeg {audit.get('first3_evidenced_item_count')}"
        )
    if (
        'expect_first3_primary_source_family_count' in case
        and audit.get('first3_primary_source_family_count') != case['expect_first3_primary_source_family_count']
    ):
        failures.append(
            'first3_primary_source_family_count verwacht '
            f"{case['expect_first3_primary_source_family_count']}, kreeg {audit.get('first3_primary_source_family_count')}"
        )
    if (
        'expect_first3_primary_fresh_item_count' in case
        and audit.get('first3_primary_fresh_item_count') != case['expect_first3_primary_fresh_item_count']
    ):
        failures.append(
            'first3_primary_fresh_item_count verwacht '
            f"{case['expect_first3_primary_fresh_item_count']}, kreeg {audit.get('first3_primary_fresh_item_count')}"
        )
    if 'expect_source_url_count' in case and audit.get('source_url_count') != case['expect_source_url_count']:
        failures.append(
            f"source_url_count verwacht {case['expect_source_url_count']}, kreeg {audit.get('source_url_count')}"
        )
    if 'expect_unique_source_url_count' in case and audit.get('unique_source_url_count') != case['expect_unique_source_url_count']:
        failures.append(
            'unique_source_url_count verwacht '
            f"{case['expect_unique_source_url_count']}, kreeg {audit.get('unique_source_url_count')}"
        )
    if 'expect_source_domain_count' in case and audit.get('source_domain_count') != case['expect_source_domain_count']:
        failures.append(
            f"source_domain_count verwacht {case['expect_source_domain_count']}, kreeg {audit.get('source_domain_count')}"
        )
    if (
        'expect_first3_unique_source_url_count' in case
        and audit.get('first3_unique_source_url_count') != case['expect_first3_unique_source_url_count']
    ):
        failures.append(
            'first3_unique_source_url_count verwacht '
            f"{case['expect_first3_unique_source_url_count']}, kreeg {audit.get('first3_unique_source_url_count')}"
        )
    if (
        'expect_first3_source_domain_count' in case
        and audit.get('first3_source_domain_count') != case['expect_first3_source_domain_count']
    ):
        failures.append(
            'first3_source_domain_count verwacht '
            f"{case['expect_first3_source_domain_count']}, kreeg {audit.get('first3_source_domain_count')}"
        )
    if (
        'expect_explicit_dated_item_count' in case
        and audit.get('explicit_dated_item_count') != case['expect_explicit_dated_item_count']
    ):
        failures.append(
            'explicit_dated_item_count verwacht '
            f"{case['expect_explicit_dated_item_count']}, kreeg {audit.get('explicit_dated_item_count')}"
        )
    if (
        'expect_explicit_recent_dated_first3_count' in case
        and audit.get('explicit_recent_dated_first3_count') != case['expect_explicit_recent_dated_first3_count']
    ):
        failures.append(
            'explicit_recent_dated_first3_count verwacht '
            f"{case['expect_explicit_recent_dated_first3_count']}, kreeg {audit.get('explicit_recent_dated_first3_count')}"
        )
    if (
        'expect_explicit_fresh_dated_first3_count' in case
        and audit.get('explicit_fresh_dated_first3_count') != case['expect_explicit_fresh_dated_first3_count']
    ):
        failures.append(
            'explicit_fresh_dated_first3_count verwacht '
            f"{case['expect_explicit_fresh_dated_first3_count']}, kreeg {audit.get('explicit_fresh_dated_first3_count')}"
        )
    if (
        'expect_future_dated_item_count' in case
        and audit.get('future_dated_item_count') != case['expect_future_dated_item_count']
    ):
        failures.append(
            'future_dated_item_count verwacht '
            f"{case['expect_future_dated_item_count']}, kreeg {audit.get('future_dated_item_count')}"
        )
    if (
        'expect_invalid_source_issue_counts' in case
        and audit.get('invalid_source_line_issue_counts') != case['expect_invalid_source_issue_counts']
    ):
        failures.append(
            'invalid_source_line_issue_counts verwacht '
            f"{case['expect_invalid_source_issue_counts']}, kreeg {audit.get('invalid_source_line_issue_counts')}"
        )
    if (
        'expect_exact_field_line_counts' in case
        and audit.get('exact_field_line_counts') != case['expect_exact_field_line_counts']
    ):
        failures.append(
            'exact_field_line_counts verwacht '
            f"{case['expect_exact_field_line_counts']}, kreeg {audit.get('exact_field_line_counts')}"
        )
    if (
        'expect_items_with_exact_field_order_count' in case
        and audit.get('items_with_exact_field_order_count') != case['expect_items_with_exact_field_order_count']
    ):
        failures.append(
            'items_with_exact_field_order_count verwacht '
            f"{case['expect_items_with_exact_field_order_count']}, kreeg {audit.get('items_with_exact_field_order_count')}"
        )
    if (
        'expect_items_with_field_order_mismatch_count' in case
        and audit.get('items_with_field_order_mismatch_count') != case['expect_items_with_field_order_mismatch_count']
    ):
        failures.append(
            'items_with_field_order_mismatch_count verwacht '
            f"{case['expect_items_with_field_order_mismatch_count']}, kreeg {audit.get('items_with_field_order_mismatch_count')}"
        )
    if (
        'expect_numbered_title_heading_count' in case
        and audit.get('numbered_title_heading_count') != case['expect_numbered_title_heading_count']
    ):
        failures.append(
            'numbered_title_heading_count verwacht '
            f"{case['expect_numbered_title_heading_count']}, kreeg {audit.get('numbered_title_heading_count')}"
        )
    audit_text = audit.get('text') or ''
    for snippet in case.get('expect_reason_substrings', []):
        if snippet not in audit_text:
            failures.append(f"verwachte audittekst ontbreekt: {snippet}")
    return {
        'name': case['name'],
        'path': str(path),
        'ok': not failures,
        'failures': failures,
        'audit_ok': audit.get('ok'),
        'audit_text': audit.get('text'),
        'item_count': audit.get('item_count'),
        'items_with_source_count': audit.get('items_with_source_count'),
        'items_with_valid_source_line_count': audit.get('items_with_valid_source_line_count'),
        'items_with_invalid_source_line_count': audit.get('items_with_invalid_source_line_count'),
        'first3_items_with_source_count': audit.get('first3_items_with_source_count'),
        'first3_items_with_valid_source_line_count': audit.get('first3_items_with_valid_source_line_count'),
        'first3_items_with_multiple_sources_count': audit.get('first3_items_with_multiple_sources_count'),
        'first3_items_with_primary_source_count': audit.get('first3_items_with_primary_source_count'),
        'first3_primary_source_family_count': audit.get('first3_primary_source_family_count'),
        'first3_primary_fresh_item_count': audit.get('first3_primary_fresh_item_count'),
        'explicit_dated_item_count': audit.get('explicit_dated_item_count'),
        'explicit_recent_dated_first3_count': audit.get('explicit_recent_dated_first3_count'),
        'explicit_fresh_dated_first3_count': audit.get('explicit_fresh_dated_first3_count'),
        'future_dated_item_count': audit.get('future_dated_item_count'),
        'invalid_source_line_issue_counts': audit.get('invalid_source_line_issue_counts'),
        'exact_field_line_counts': audit.get('exact_field_line_counts'),
        'items_with_exact_field_order_count': audit.get('items_with_exact_field_order_count'),
        'items_with_field_order_mismatch_count': audit.get('items_with_field_order_mismatch_count'),
        'numbered_title_heading_count': audit.get('numbered_title_heading_count'),
    }


def evaluate_status_phase_case(module, case):
    status = module.build_status(reference_ms=case['reference_ms'])
    failures = []

    if status.get('proof_state') != case['expect_proof_state']:
        failures.append(
            f"proof_state verwacht {case['expect_proof_state']}, kreeg {status.get('proof_state')}"
        )
    if status.get('proof_blocker_kind') != case['expect_proof_blocker_kind']:
        failures.append(
            f"proof_blocker_kind verwacht {case['expect_proof_blocker_kind']}, kreeg {status.get('proof_blocker_kind')}"
        )
    if status.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
        failures.append(
            f"proof_next_action_kind verwacht {case['expect_proof_next_action_kind']}, kreeg {status.get('proof_next_action_kind')}"
        )
    if status.get('proof_recheck_window_open') != case['expect_proof_recheck_window_open']:
        failures.append(
            'proof_recheck_window_open verwacht '
            f"{case['expect_proof_recheck_window_open']}, kreeg {status.get('proof_recheck_window_open')}"
        )
    if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
        audit_ok = ((status.get('proof_recheck_schedule_audit') or {}).get('ok'))
        if audit_ok != case.get('expect_proof_recheck_schedule_audit_ok'):
            failures.append(
                'status proof_recheck_schedule_audit.ok verwacht '
                f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {audit_ok}"
            )
        if status.get('proof_recheck_schedule_ok') != case.get('expect_proof_recheck_schedule_audit_ok'):
            failures.append(
                'status proof_recheck_schedule_ok verwacht '
                f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {status.get('proof_recheck_schedule_ok')}"
            )
        expected_schedule_kind = 'ok' if case.get('expect_proof_recheck_schedule_audit_ok') else None
        audit_kind = ((status.get('proof_recheck_schedule_audit') or {}).get('kind'))
        if expected_schedule_kind is not None and audit_kind != expected_schedule_kind:
            failures.append(
                f"status proof_recheck_schedule_audit.kind verwacht {expected_schedule_kind}, kreeg {audit_kind}"
            )
        if expected_schedule_kind is not None and status.get('proof_recheck_schedule_kind') != expected_schedule_kind:
            failures.append(
                f"status proof_recheck_schedule_kind verwacht {expected_schedule_kind}, kreeg {status.get('proof_recheck_schedule_kind')}"
            )
        if expected_schedule_kind is not None and status.get('proof_recheck_schedule_kind_text') != f'proof-recheck-cronstatus: {expected_schedule_kind}':
            failures.append(
                'status proof_recheck_schedule_kind_text verwacht '
                f"proof-recheck-cronstatus: {expected_schedule_kind}, kreeg {status.get('proof_recheck_schedule_kind_text')}"
            )
        if status.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
            failures.append(
                'status proof_recheck_schedule_job_name verwacht '
                f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {status.get('proof_recheck_schedule_job_name')}"
            )
        if status.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
            failures.append(
                'status proof_recheck_schedule_expr verwacht '
                f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {status.get('proof_recheck_schedule_expr')}"
            )
        if status.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
            failures.append(
                'status proof_recheck_schedule_tz verwacht '
                f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {status.get('proof_recheck_schedule_tz')}"
            )
        if status.get('proof_recheck_schedule_expected_gap_minutes') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES:
            failures.append(
                'status proof_recheck_schedule_expected_gap_minutes verwacht '
                f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES}, kreeg {status.get('proof_recheck_schedule_expected_gap_minutes')}"
            )
        if status.get('proof_recheck_schedule_same_day_after_target') is not True:
            failures.append(
                'status proof_recheck_schedule_same_day_after_target verwacht True, kreeg '
                f"{status.get('proof_recheck_schedule_same_day_after_target')}"
            )
    if case.get('expect_proof_recheck_schedule_matches_grace') is not None:
        if status.get('proof_recheck_schedule_matches_grace') != case.get('expect_proof_recheck_schedule_matches_grace'):
            failures.append(
                'status proof_recheck_schedule_matches_grace verwacht '
                f"{case.get('expect_proof_recheck_schedule_matches_grace')}, kreeg {status.get('proof_recheck_schedule_matches_grace')}"
            )

    combined_text = ' || '.join(
        str(bit) for bit in [
            status.get('proof_state_text'),
            status.get('proof_blocker_text'),
            status.get('proof_next_action_text'),
            status.get('proof_next_action_window_text'),
            status.get('proof_recheck_window_text'),
            status.get('proof_recheck_schedule_text'),
        ] if bit
    )
    for snippet in case.get('expect_substrings', []):
        if snippet not in combined_text:
            failures.append(f"verwachte status-tekst ontbreekt: {snippet}")

    return {
        'name': case['name'],
        'path': None,
        'ok': not failures,
        'failures': failures,
        'audit_ok': status.get('ok'),
        'audit_text': combined_text,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_status_stdout_case(case):
    expected_status = run_status_json(case['reference_ms'])
    json_proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--json', '--reference-ms', str(case['reference_ms'])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    text_proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--reference-ms', str(case['reference_ms'])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    failures = []
    json_output = json_proc.stdout.strip() or json_proc.stderr.strip()
    text_output = text_proc.stdout.strip() or text_proc.stderr.strip()

    if json_proc.returncode != 0:
        failures.append(f"json-exitcode verwacht 0, kreeg {json_proc.returncode}")
        payload = {}
    elif not json_output:
        failures.append('geen JSON-output van ai-briefing-status.py')
        payload = {}
    else:
        try:
            payload = json.loads(json_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-status.py: {exc}')
            payload = {}

    if text_proc.returncode != 0:
        failures.append(f"tekst-exitcode verwacht 0, kreeg {text_proc.returncode}")
    if not text_output:
        failures.append('geen tekstoutput van ai-briefing-status.py')

    assert_runtime_metadata(payload, 'ai-briefing-status stdout-json', failures)

    if payload.get('proof_state') != case['expect_proof_state']:
        failures.append(
            f"proof_state verwacht {case['expect_proof_state']}, kreeg {payload.get('proof_state')}"
        )
    if payload.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
        failures.append(
            'proof_next_action_kind verwacht '
            f"{case['expect_proof_next_action_kind']}, kreeg {payload.get('proof_next_action_kind')}"
        )
    if payload.get('proof_recheck_schedule_kind') != 'ok':
        failures.append(
            f"proof_recheck_schedule_kind verwacht ok, kreeg {payload.get('proof_recheck_schedule_kind')}"
        )
    if payload.get('proof_recheck_schedule_kind_text') != 'proof-recheck-cronstatus: ok':
        failures.append(
            'proof_recheck_schedule_kind_text verwacht proof-recheck-cronstatus: ok, kreeg '
            f"{payload.get('proof_recheck_schedule_kind_text')}"
        )
    if payload.get('proof_freshness_text') != expected_status.get('proof_freshness_text'):
        failures.append(
            'proof_freshness_text verwacht '
            f"{expected_status.get('proof_freshness_text')}, kreeg {payload.get('proof_freshness_text')}"
        )
    if payload.get('proof_plan_text') != expected_status.get('proof_plan_text'):
        failures.append(
            'proof_plan_text verwacht '
            f"{expected_status.get('proof_plan_text')}, kreeg {payload.get('proof_plan_text')}"
        )
    expected_last_run_config_relation_text = case.get('expect_last_run_config_relation_text')
    if (
        expected_last_run_config_relation_text is not None
        and payload.get('last_run_config_relation_text') != expected_last_run_config_relation_text
    ):
        failures.append(
            'last_run_config_relation_text verwacht '
            f"{expected_last_run_config_relation_text}, kreeg {payload.get('last_run_config_relation_text')}"
        )
    if payload.get('last_run_config_relation_text') and not payload.get('last_run_config_relation'):
        failures.append(
            'last_run_config_relation ontbreekt in status-stdout-json terwijl '
            'last_run_config_relation_text wel gezet is'
        )
    if payload.get('proof_freshness_text') != ((payload.get('proof_freshness') or {}).get('text')):
        failures.append(
            'proof_freshness_text verwacht alias-pariteit met proof_freshness.text, kreeg '
            f"{payload.get('proof_freshness_text')} versus {((payload.get('proof_freshness') or {}).get('text'))}"
        )
    if payload.get('summary_output_examples') != expected_status.get('summary_output_examples'):
        failures.append(
            'summary_output_examples verwacht '
            f"{expected_status.get('summary_output_examples')}, kreeg {payload.get('summary_output_examples')}"
        )
    if not isinstance(payload.get('summary_output_examples'), list):
        failures.append(
            'summary_output_examples verwacht list, kreeg '
            f"{type(payload.get('summary_output_examples')).__name__}"
        )

    if payload.get('proof_freshness_text') and payload['proof_freshness_text'] not in text_output:
        failures.append(
            'status-stdout-tekst mist proof_freshness_text uit stdout-json: '
            f"{payload.get('proof_freshness_text')}"
        )
    if payload.get('proof_plan_text') and payload['proof_plan_text'] not in text_output:
        failures.append(
            'status-stdout-tekst mist proof_plan_text uit stdout-json: '
            f"{payload.get('proof_plan_text')}"
        )
    if payload.get('last_run_config_relation_text') and payload['last_run_config_relation_text'] not in text_output:
        failures.append(
            'status-stdout-tekst mist last_run_config_relation_text uit stdout-json: '
            f"{payload.get('last_run_config_relation_text')}"
        )
    summary_examples_text = (
        'outputvoorbeelden: ' + '; '.join((payload.get('summary_output_examples') or [])[:2])
        if payload.get('summary_output_examples') else None
    )
    if summary_examples_text and summary_examples_text not in text_output:
        failures.append(
            'status-stdout-tekst mist summary_output_examples uit stdout-json: '
            f"{summary_examples_text}"
        )

    combined_text = ' || '.join(
        bit for bit in [
            payload.get('proof_recheck_schedule_text'),
            payload.get('proof_recheck_schedule_kind_text'),
            payload.get('proof_freshness_text'),
            payload.get('proof_plan_text'),
            payload.get('last_run_config_relation_text'),
            summary_examples_text,
            payload.get('proof_next_action_window_text'),
            payload.get('proof_next_action_text'),
            text_output,
        ] if bit
    )
    for snippet in case.get('expect_text_substrings', []):
        if snippet not in combined_text:
            failures.append(f"verwachte ai-briefing-status-tekst ontbreekt: {snippet}")

    return {
        'name': case['name'],
        'path': str(STATUS_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': combined_text,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_status_summary_audit_case(module, case):
    summary_path = Path(case['path'])
    summary_text = summary_path.read_text(encoding='utf-8')
    expected_payload = module.audit_summary_output(summary_text)
    expected_text = module.render_summary_audit_text(expected_payload)
    runtime_keys = {
        'generated_at',
        'generated_at_text',
        'started_at',
        'started_at_text',
        'duration_ms',
        'duration_seconds',
        'duration_text',
    }
    failures = []

    json_file_proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--json', '--summary-file', str(summary_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    json_file_output = json_file_proc.stdout.strip() or json_file_proc.stderr.strip()
    if json_file_proc.returncode != 0:
        failures.append(f'status summary-file --json exitcode verwacht 0, kreeg {json_file_proc.returncode}')
        json_file_payload = {}
    elif not json_file_output:
        failures.append('geen JSON-output van ai-briefing-status.py --json --summary-file')
        json_file_payload = {}
    else:
        try:
            json_file_payload = json.loads(json_file_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-status.py --json --summary-file: {exc}')
            json_file_payload = {}

    json_stdin_proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--json', '--summary-stdin'],
        cwd=ROOT,
        input=summary_text,
        capture_output=True,
        text=True,
        check=False,
    )
    json_stdin_output = json_stdin_proc.stdout.strip() or json_stdin_proc.stderr.strip()
    if json_stdin_proc.returncode != 0:
        failures.append(f'status summary-stdin --json exitcode verwacht 0, kreeg {json_stdin_proc.returncode}')
        json_stdin_payload = {}
    elif not json_stdin_output:
        failures.append('geen JSON-output van ai-briefing-status.py --json --summary-stdin')
        json_stdin_payload = {}
    else:
        try:
            json_stdin_payload = json.loads(json_stdin_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-status.py --json --summary-stdin: {exc}')
            json_stdin_payload = {}

    text_file_proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--summary-file', str(summary_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    text_file_output = text_file_proc.stdout.strip() or text_file_proc.stderr.strip()
    if text_file_proc.returncode != 0:
        failures.append(f'status summary-file tekst-exitcode verwacht 0, kreeg {text_file_proc.returncode}')
    elif text_file_output != expected_text:
        failures.append(
            'status summary-file tekstoutput verwacht exacte render_summary_audit_text-pariteit, kreeg '
            f"{text_file_output!r} versus {expected_text!r}"
        )

    text_stdin_proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--summary-stdin'],
        cwd=ROOT,
        input=summary_text,
        capture_output=True,
        text=True,
        check=False,
    )
    text_stdin_output = text_stdin_proc.stdout.strip() or text_stdin_proc.stderr.strip()
    if text_stdin_proc.returncode != 0:
        failures.append(f'status summary-stdin tekst-exitcode verwacht 0, kreeg {text_stdin_proc.returncode}')
    elif text_stdin_output != expected_text:
        failures.append(
            'status summary-stdin tekstoutput verwacht exacte render_summary_audit_text-pariteit, kreeg '
            f"{text_stdin_output!r} versus {expected_text!r}"
        )

    comparable_json_file_payload = None
    if json_file_payload:
        assert_runtime_metadata(json_file_payload, 'status summary-file --json', failures)
        comparable_json_file_payload = {
            key: value for key, value in json_file_payload.items() if key not in runtime_keys
        }
        if comparable_json_file_payload != expected_payload:
            failures.append(
                'status summary-file --json verwacht audit_summary_output-pariteit buiten runtime-metadata, kreeg '
                f"{comparable_json_file_payload} versus {expected_payload}"
            )

    comparable_json_stdin_payload = None
    if json_stdin_payload:
        assert_runtime_metadata(json_stdin_payload, 'status summary-stdin --json', failures)
        comparable_json_stdin_payload = {
            key: value for key, value in json_stdin_payload.items() if key not in runtime_keys
        }
        if comparable_json_stdin_payload != expected_payload:
            failures.append(
                'status summary-stdin --json verwacht audit_summary_output-pariteit buiten runtime-metadata, kreeg '
                f"{comparable_json_stdin_payload} versus {expected_payload}"
            )

    if comparable_json_file_payload is not None and comparable_json_stdin_payload is not None:
        if comparable_json_file_payload != comparable_json_stdin_payload:
            failures.append(
                'status summary-file/stdin --json verwachten onderlinge pariteit buiten runtime-metadata, kregen '
                f"{comparable_json_file_payload} versus {comparable_json_stdin_payload}"
            )

    return {
        'name': case['name'],
        'path': str(summary_path),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': ' || '.join(bit for bit in [expected_text, text_file_output, text_stdin_output] if bit),
        'item_count': expected_payload.get('item_count'),
        'items_with_source_count': expected_payload.get('items_with_source_count'),
        'items_with_valid_source_line_count': expected_payload.get('items_with_valid_source_line_count'),
        'items_with_invalid_source_line_count': expected_payload.get('items_with_invalid_source_line_count'),
        'first3_items_with_source_count': expected_payload.get('first3_items_with_source_count'),
        'first3_items_with_valid_source_line_count': expected_payload.get('first3_items_with_valid_source_line_count'),
        'first3_items_with_multiple_sources_count': expected_payload.get('first3_items_with_multiple_sources_count'),
        'first3_items_with_primary_source_count': expected_payload.get('first3_items_with_primary_source_count'),
        'first3_primary_source_family_count': expected_payload.get('first3_primary_source_family_count'),
        'first3_primary_fresh_item_count': expected_payload.get('first3_primary_fresh_item_count'),
        'explicit_dated_item_count': expected_payload.get('explicit_dated_item_count'),
        'explicit_recent_dated_first3_count': expected_payload.get('explicit_recent_dated_first3_count'),
        'explicit_fresh_dated_first3_count': expected_payload.get('explicit_fresh_dated_first3_count'),
        'future_dated_item_count': expected_payload.get('future_dated_item_count'),
        'invalid_source_line_issue_counts': expected_payload.get('invalid_source_line_issue_counts'),
        'exact_field_line_counts': expected_payload.get('exact_field_line_counts'),
        'items_with_exact_field_order_count': expected_payload.get('items_with_exact_field_order_count'),
        'items_with_field_order_mismatch_count': expected_payload.get('items_with_field_order_mismatch_count'),
        'numbered_title_heading_count': expected_payload.get('numbered_title_heading_count'),
    }


def evaluate_proof_recheck_case(case):
    proc = subprocess.run(
        ['python3', str(PROOF_RECHECK_SCRIPT), '--json', '--reference-ms', str(case['reference_ms'])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = proc.stdout.strip() or proc.stderr.strip()
    failures = []

    if not output:
        failures.append('geen output van ai-briefing-proof-recheck.py')
        payload = {}
    else:
        try:
            payload = json.loads(output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-proof-recheck.py: {exc}')
            payload = {}

    text_proc = subprocess.run(
        ['python3', str(PROOF_RECHECK_SCRIPT), '--reference-ms', str(case['reference_ms'])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    text_output = text_proc.stdout.strip() or text_proc.stderr.strip()
    if text_proc.returncode != case['expect_exit_code']:
        failures.append(
            f"tekst-exitcode verwacht {case['expect_exit_code']}, kreeg {text_proc.returncode}"
        )
    if not text_output:
        failures.append('geen tekstoutput van ai-briefing-proof-recheck.py')

    if proc.returncode != case['expect_exit_code']:
        failures.append(f"proces-exitcode verwacht {case['expect_exit_code']}, kreeg {proc.returncode}")
    if payload.get('exit_code') != case['expect_exit_code']:
        failures.append(f"payload exit_code verwacht {case['expect_exit_code']}, kreeg {payload.get('exit_code')}")
    if payload.get('state') != case['expect_state']:
        failures.append(f"state verwacht {case['expect_state']}, kreeg {payload.get('state')}")
    if payload.get('result_kind') != case['expect_result_kind']:
        failures.append(f"result_kind verwacht {case['expect_result_kind']}, kreeg {payload.get('result_kind')}")
    if payload.get('proof_state') != case['expect_proof_state']:
        failures.append(f"proof_state verwacht {case['expect_proof_state']}, kreeg {payload.get('proof_state')}")
    if payload.get('proof_blocker_kind') != case['expect_proof_blocker_kind']:
        failures.append(
            f"proof_blocker_kind verwacht {case['expect_proof_blocker_kind']}, kreeg {payload.get('proof_blocker_kind')}"
        )
    if payload.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
        failures.append(
            f"proof_next_action_kind verwacht {case['expect_proof_next_action_kind']}, kreeg {payload.get('proof_next_action_kind')}"
        )
    if payload.get('proof_recheck_ready') != case['expect_proof_recheck_ready']:
        failures.append(
            f"proof_recheck_ready verwacht {case['expect_proof_recheck_ready']}, kreeg {payload.get('proof_recheck_ready')}"
        )
    if payload.get('proof_wait_until_at') != case.get('expect_proof_wait_until_at'):
        failures.append(
            f"proof_wait_until_at verwacht {case.get('expect_proof_wait_until_at')}, kreeg {payload.get('proof_wait_until_at')}"
        )
    if payload.get('proof_wait_until_text') != case.get('expect_proof_wait_until_text'):
        failures.append(
            f"proof_wait_until_text verwacht {case.get('expect_proof_wait_until_text')}, kreeg {payload.get('proof_wait_until_text')}"
        )
    if payload.get('proof_wait_until_reason_text') != case.get('expect_proof_wait_until_reason_text'):
        failures.append(
            'proof_wait_until_reason_text verwacht '
            f"{case.get('expect_proof_wait_until_reason_text')}, kreeg {payload.get('proof_wait_until_reason_text')}"
        )
    if payload.get('proof_recheck_after_at') != case.get('expect_proof_recheck_after_at'):
        failures.append(
            f"proof_recheck_after_at verwacht {case.get('expect_proof_recheck_after_at')}, kreeg {payload.get('proof_recheck_after_at')}"
        )
    if payload.get('proof_wait_until_remaining_ms') != case.get('expect_proof_wait_until_remaining_ms'):
        failures.append(
            'proof_wait_until_remaining_ms verwacht '
            f"{case.get('expect_proof_wait_until_remaining_ms')}, kreeg {payload.get('proof_wait_until_remaining_ms')}"
        )
    if payload.get('proof_next_qualifying_slot_at') != case.get('expect_proof_next_qualifying_slot_at'):
        failures.append(
            'proof_next_qualifying_slot_at verwacht '
            f"{case.get('expect_proof_next_qualifying_slot_at')}, kreeg {payload.get('proof_next_qualifying_slot_at')}"
        )
    if payload.get('proof_next_qualifying_slot_remaining_ms') != case.get('expect_proof_next_qualifying_slot_remaining_ms'):
        failures.append(
            'proof_next_qualifying_slot_remaining_ms verwacht '
            f"{case.get('expect_proof_next_qualifying_slot_remaining_ms')}, kreeg {payload.get('proof_next_qualifying_slot_remaining_ms')}"
        )
    if payload.get('proof_target_due_at') != case.get('expect_proof_target_due_at'):
        failures.append(
            f"proof_target_due_at verwacht {case.get('expect_proof_target_due_at')}, kreeg {payload.get('proof_target_due_at')}"
        )
    if payload.get('proof_target_due_at_if_next_slot_missed') != case.get('expect_proof_target_due_at_if_next_slot_missed'):
        failures.append(
            'proof_target_due_at_if_next_slot_missed verwacht '
            f"{case.get('expect_proof_target_due_at_if_next_slot_missed')}, kreeg {payload.get('proof_target_due_at_if_next_slot_missed')}"
        )
    if payload.get('proof_schedule_slip_ms') != case.get('expect_proof_schedule_slip_ms'):
        failures.append(
            f"proof_schedule_slip_ms verwacht {case.get('expect_proof_schedule_slip_ms')}, kreeg {payload.get('proof_schedule_slip_ms')}"
        )
    if payload.get('status_ok') != case['expect_status_ok']:
        failures.append(f"status_ok verwacht {case['expect_status_ok']}, kreeg {payload.get('status_ok')}")
    if payload.get('watchdog_ok') != case['expect_watchdog_ok']:
        failures.append(f"watchdog_ok verwacht {case['expect_watchdog_ok']}, kreeg {payload.get('watchdog_ok')}")
    if case.get('expect_proof_config_hash_present') and not payload.get('proof_config_hash'):
        failures.append('proof_config_hash ontbreekt in proof-recheck-payload')
    if payload.get('proof_progress_text') and not payload.get('last_run_timeout_text'):
        failures.append('last_run_timeout_text ontbreekt in proof-recheck-payload')
    if payload.get('proof_progress_text') and not payload.get('recent_run_duration_text'):
        failures.append('recent_run_duration_text ontbreekt in proof-recheck-payload')
    if payload.get('proof_progress_text') and payload.get('proof_waiting_for_next_scheduled_run') is None:
        failures.append('proof_waiting_for_next_scheduled_run ontbreekt in proof-recheck-payload')
    if payload.get('last_run_config_relation_text') and not payload.get('last_run_config_relation'):
        failures.append('last_run_config_relation ontbreekt in proof-recheck-payload terwijl last_run_config_relation_text wel gezet is')
    if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
        audit_ok = ((payload.get('proof_recheck_schedule_audit') or {}).get('ok'))
        if audit_ok != case.get('expect_proof_recheck_schedule_audit_ok'):
            failures.append(
                'proof_recheck_schedule_audit.ok verwacht '
                f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {audit_ok}"
            )
        if payload.get('proof_recheck_schedule_ok') != case.get('expect_proof_recheck_schedule_audit_ok'):
            failures.append(
                'proof_recheck_schedule_ok verwacht '
                f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {payload.get('proof_recheck_schedule_ok')}"
            )
        expected_schedule_kind = 'ok' if case.get('expect_proof_recheck_schedule_audit_ok') else None
        audit_kind = ((payload.get('proof_recheck_schedule_audit') or {}).get('kind'))
        if expected_schedule_kind is not None and audit_kind != expected_schedule_kind:
            failures.append(
                f"proof_recheck_schedule_audit.kind verwacht {expected_schedule_kind}, kreeg {audit_kind}"
            )
        if expected_schedule_kind is not None and payload.get('proof_recheck_schedule_kind') != expected_schedule_kind:
            failures.append(
                f"proof_recheck_schedule_kind verwacht {expected_schedule_kind}, kreeg {payload.get('proof_recheck_schedule_kind')}"
            )
        if expected_schedule_kind is not None and payload.get('proof_recheck_schedule_kind_text') != f'proof-recheck-cronstatus: {expected_schedule_kind}':
            failures.append(
                'proof_recheck_schedule_kind_text verwacht '
                f"proof-recheck-cronstatus: {expected_schedule_kind}, kreeg {payload.get('proof_recheck_schedule_kind_text')}"
            )
    if case.get('expect_proof_recheck_schedule_matches_grace') is not None:
        if payload.get('proof_recheck_schedule_matches_grace') != case.get('expect_proof_recheck_schedule_matches_grace'):
            failures.append(
                'proof_recheck_schedule_matches_grace verwacht '
                f"{case.get('expect_proof_recheck_schedule_matches_grace')}, kreeg {payload.get('proof_recheck_schedule_matches_grace')}"
            )
    if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
        if payload.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
            failures.append(
                'proof_recheck_schedule_job_name verwacht '
                f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {payload.get('proof_recheck_schedule_job_name')}"
            )
        if payload.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
            failures.append(
                'proof_recheck_schedule_expr verwacht '
                f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {payload.get('proof_recheck_schedule_expr')}"
            )
        if payload.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
            failures.append(
                'proof_recheck_schedule_tz verwacht '
                f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {payload.get('proof_recheck_schedule_tz')}"
            )
        if payload.get('proof_recheck_schedule_expected_gap_minutes') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES:
            failures.append(
                'proof_recheck_schedule_expected_gap_minutes verwacht '
                f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES}, kreeg {payload.get('proof_recheck_schedule_expected_gap_minutes')}"
            )
        if payload.get('proof_recheck_schedule_same_day_after_target') is not True:
            failures.append(
                'proof_recheck_schedule_same_day_after_target verwacht True, kreeg '
                f"{payload.get('proof_recheck_schedule_same_day_after_target')}"
            )

    expected_requested_status_kind = 'requested' if payload.get('consumer_requested_output_count') else 'none-requested'
    if payload.get('consumer_requested_outputs_status_kind') != expected_requested_status_kind:
        failures.append(
            'consumer_requested_outputs_status_kind verwacht '
            f"{expected_requested_status_kind}, kreeg {payload.get('consumer_requested_outputs_status_kind')}"
        )
    expected_outputs_status_kind = (
        'ok'
        if payload.get('consumer_outputs_match_requested') and payload.get('consumer_requested_output_count')
        else 'none-requested'
        if payload.get('consumer_outputs_match_requested')
        else 'mismatch'
    )
    if payload.get('consumer_outputs_status_kind') != expected_outputs_status_kind:
        failures.append(
            'consumer_outputs_status_kind verwacht '
            f"{expected_outputs_status_kind}, kreeg {payload.get('consumer_outputs_status_kind')}"
        )
    expected_effective_status_kind = (
        'ok'
        if payload.get('consumer_effective_outputs_match_requested') and payload.get('consumer_requested_output_count')
        else 'none-requested'
        if payload.get('consumer_effective_outputs_match_requested')
        else 'mismatch'
    )
    if payload.get('consumer_effective_outputs_status_kind') != expected_effective_status_kind:
        failures.append(
            'consumer_effective_outputs_status_kind verwacht '
            f"{expected_effective_status_kind}, kreeg {payload.get('consumer_effective_outputs_status_kind')}"
        )

    combined_text = ' || '.join(
        str(bit)
        for bit in [
            payload.get('result_text'),
            payload.get('summary'),
            payload.get('proof_state_text'),
            payload.get('proof_config_identity_text'),
            payload.get('last_run_config_relation_text'),
            payload.get('proof_blocker_text'),
            payload.get('proof_next_action_text'),
            payload.get('proof_next_action_window_text'),
            payload.get('proof_recheck_window_text'),
            payload.get('proof_recheck_schedule_kind_text'),
            payload.get('proof_recheck_schedule_text'),
            payload.get('proof_recheck_commands_text'),
        ]
        if bit
    )
    for snippet in case.get('expect_substrings', []):
        if snippet not in combined_text:
            failures.append(f"verwachte proof-recheck-tekst ontbreekt: {snippet}")
        if text_output and snippet not in text_output:
            failures.append(f"verwachte proof-recheck-plain-tekst ontbreekt: {snippet}")

    for snippet in case.get('expect_plain_not_substrings', []):
        if snippet and snippet in text_output:
            failures.append(f"ongewenste proof-recheck-plain-tekst aanwezig: {snippet}")

    return {
        'name': case['name'],
        'path': str(PROOF_RECHECK_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': payload.get('ok'),
        'audit_text': combined_text,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_proof_recheck_producer_case(case):
    with tempfile.TemporaryDirectory(prefix='ai-briefing-proof-recheck-producer-') as temp_dir:
        json_proc = subprocess.run(
            [
                'python3', str(PROOF_RECHECK_PRODUCER_SCRIPT), 'all', '--json',
                '--reference-ms', str(case['reference_ms']),
                '--consumer-root', temp_dir,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        quiet_proc = subprocess.run(
            [
                'python3', str(PROOF_RECHECK_PRODUCER_SCRIPT), 'all', '--quiet',
                '--reference-ms', str(case['reference_ms']),
                '--consumer-root', temp_dir,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        failures = []
        json_output = json_proc.stdout.strip() or json_proc.stderr.strip()
        if not json_output:
            failures.append('geen JSON-output van ai-briefing-proof-recheck-producer.py')
            payload = {}
        else:
            try:
                payload = json.loads(json_output)
            except json.JSONDecodeError as exc:
                failures.append(f'ongeldige JSON van ai-briefing-proof-recheck-producer.py: {exc}')
                payload = {}

        if payload:
            assert_runtime_metadata(payload, 'proof-recheck-producer stdout-json', failures)

        overall = payload.get('overall') or {}
        items = payload.get('items') or []
        child_payload = {}
        top_level_overall_alias_keys = [key for key in overall.keys() if key != 'ok']
        if payload.get('consumer_root') != temp_dir:
            failures.append(f"consumer_root verwacht {temp_dir}, kreeg {payload.get('consumer_root')}")
        if payload.get('item_count') != 1:
            failures.append(f"item_count verwacht 1, kreeg {payload.get('item_count')}")
        if len(items) != 1:
            failures.append(f"items verwacht 1 item, kreeg {len(items)}")
        else:
            child_payload = items[0].get('payload') or {}
            if items[0].get('returncode') != case['expect_exit_code']:
                failures.append(
                    f"items[0].returncode verwacht {case['expect_exit_code']}, kreeg {items[0].get('returncode')}"
                )
            if child_payload:
                assert_runtime_metadata(child_payload, 'proof-recheck-producer child payload', failures)
        if json_proc.returncode != case['expect_exit_code']:
            failures.append(f"json-exitcode verwacht {case['expect_exit_code']}, kreeg {json_proc.returncode}")
        if quiet_proc.returncode != case['expect_exit_code']:
            failures.append(f"quiet-exitcode verwacht {case['expect_exit_code']}, kreeg {quiet_proc.returncode}")
        for alias_key in top_level_overall_alias_keys:
            if payload.get(alias_key) != overall.get(alias_key):
                failures.append(
                    f"top-level alias {alias_key} verwacht {overall.get(alias_key)!r}, kreeg {payload.get(alias_key)!r}"
                )
        if overall.get('returncode') != case['expect_exit_code']:
            failures.append(f"overall.returncode verwacht {case['expect_exit_code']}, kreeg {overall.get('returncode')}")
        if overall.get('exit_code') != case['expect_exit_code']:
            failures.append(f"overall.exit_code verwacht {case['expect_exit_code']}, kreeg {overall.get('exit_code')}")
        if overall.get('state') != case['expect_state']:
            failures.append(f"overall.state verwacht {case['expect_state']}, kreeg {overall.get('state')}")
        if overall.get('result_kind') != case['expect_result_kind']:
            failures.append(f"overall.result_kind verwacht {case['expect_result_kind']}, kreeg {overall.get('result_kind')}")
        if overall.get('reference_now_text') != case['expect_reference_now_text']:
            failures.append(
                f"overall.reference_now_text verwacht {case['expect_reference_now_text']}, kreeg {overall.get('reference_now_text')}"
            )
        if overall.get('status_ok') != case['expect_status_ok']:
            failures.append(f"overall.status_ok verwacht {case['expect_status_ok']}, kreeg {overall.get('status_ok')}")
        if overall.get('watchdog_ok') != case['expect_watchdog_ok']:
            failures.append(f"overall.watchdog_ok verwacht {case['expect_watchdog_ok']}, kreeg {overall.get('watchdog_ok')}")
        expected_proof_plan_text = case.get('expect_proof_plan_text')
        if expected_proof_plan_text is not None and overall.get('proof_plan_text') != expected_proof_plan_text:
            failures.append(
                'overall.proof_plan_text verwacht '
                f"{expected_proof_plan_text}, kreeg {overall.get('proof_plan_text')}"
            )
        if case.get('expect_proof_config_hash_present') and not overall.get('proof_config_hash'):
            failures.append('overall.proof_config_hash ontbreekt in producer-json')
        if overall.get('last_run_config_relation_text') and not overall.get('last_run_config_relation'):
            failures.append('overall.last_run_config_relation ontbreekt in producer-json terwijl last_run_config_relation_text wel gezet is')
        if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
            overall_audit_ok = ((overall.get('proof_recheck_schedule_audit') or {}).get('ok'))
            if overall_audit_ok != case.get('expect_proof_recheck_schedule_audit_ok'):
                failures.append(
                    'overall.proof_recheck_schedule_audit.ok verwacht '
                    f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {overall_audit_ok}"
                )
            if overall.get('proof_recheck_schedule_ok') != case.get('expect_proof_recheck_schedule_audit_ok'):
                failures.append(
                    'overall.proof_recheck_schedule_ok verwacht '
                    f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {overall.get('proof_recheck_schedule_ok')}"
                )
        if case.get('expect_proof_recheck_schedule_matches_grace') is not None:
            if overall.get('proof_recheck_schedule_matches_grace') != case.get('expect_proof_recheck_schedule_matches_grace'):
                failures.append(
                    'overall.proof_recheck_schedule_matches_grace verwacht '
                    f"{case.get('expect_proof_recheck_schedule_matches_grace')}, kreeg {overall.get('proof_recheck_schedule_matches_grace')}"
                )
        if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
            if overall.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
                failures.append(
                    'overall.proof_recheck_schedule_job_name verwacht '
                    f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {overall.get('proof_recheck_schedule_job_name')}"
                )
            if overall.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
                failures.append(
                    'overall.proof_recheck_schedule_expr verwacht '
                    f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {overall.get('proof_recheck_schedule_expr')}"
                )
            if overall.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
                failures.append(
                    'overall.proof_recheck_schedule_tz verwacht '
                    f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {overall.get('proof_recheck_schedule_tz')}"
                )
            if overall.get('proof_recheck_schedule_expected_gap_minutes') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES:
                failures.append(
                    'overall.proof_recheck_schedule_expected_gap_minutes verwacht '
                    f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES}, kreeg {overall.get('proof_recheck_schedule_expected_gap_minutes')}"
                )
            if overall.get('proof_recheck_schedule_same_day_after_target') is not True:
                failures.append(
                    'overall.proof_recheck_schedule_same_day_after_target verwacht True, kreeg '
                    f"{overall.get('proof_recheck_schedule_same_day_after_target')}"
                )
        if overall.get('proof_state') != case['expect_proof_state']:
            failures.append(f"overall.proof_state verwacht {case['expect_proof_state']}, kreeg {overall.get('proof_state')}")
        if overall.get('proof_blocker_kind') != case['expect_proof_blocker_kind']:
            failures.append(
                'overall.proof_blocker_kind verwacht '
                f"{case['expect_proof_blocker_kind']}, kreeg {overall.get('proof_blocker_kind')}"
            )
        if overall.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
            failures.append(
                'overall.proof_next_action_kind verwacht '
                f"{case['expect_proof_next_action_kind']}, kreeg {overall.get('proof_next_action_kind')}"
            )
        for child_payload_key in [
            'proof_freshness_text',
            'proof_plan_text',
            'last_run_timeout_text',
            'recent_run_duration_text',
            'summary_output_examples',
        ]:
            if overall.get(child_payload_key) != child_payload.get(child_payload_key):
                failures.append(
                    f'overall.{child_payload_key} verwacht passthrough {child_payload.get(child_payload_key)}, kreeg '
                    f"{overall.get(child_payload_key)}"
                )
        if overall.get('proof_recheck_ready') != case['expect_proof_recheck_ready']:
            failures.append(
                'overall.proof_recheck_ready verwacht '
                f"{case['expect_proof_recheck_ready']}, kreeg {overall.get('proof_recheck_ready')}"
            )
        if overall.get('proof_wait_until_at') != case.get('expect_proof_wait_until_at'):
            failures.append(
                f"overall.proof_wait_until_at verwacht {case.get('expect_proof_wait_until_at')}, kreeg {overall.get('proof_wait_until_at')}"
            )
        if overall.get('proof_wait_until_text') != case.get('expect_proof_wait_until_text'):
            failures.append(
                'overall.proof_wait_until_text verwacht '
                f"{case.get('expect_proof_wait_until_text')}, kreeg {overall.get('proof_wait_until_text')}"
            )
        if overall.get('proof_wait_until_reason_text') != case.get('expect_proof_wait_until_reason_text'):
            failures.append(
                'overall.proof_wait_until_reason_text verwacht '
                f"{case.get('expect_proof_wait_until_reason_text')}, kreeg {overall.get('proof_wait_until_reason_text')}"
            )
        if overall.get('proof_recheck_after_at') != case.get('expect_proof_recheck_after_at'):
            failures.append(
                'overall.proof_recheck_after_at verwacht '
                f"{case.get('expect_proof_recheck_after_at')}, kreeg {overall.get('proof_recheck_after_at')}"
            )
        if overall.get('proof_wait_until_remaining_ms') != case.get('expect_proof_wait_until_remaining_ms'):
            failures.append(
                'overall.proof_wait_until_remaining_ms verwacht '
                f"{case.get('expect_proof_wait_until_remaining_ms')}, kreeg {overall.get('proof_wait_until_remaining_ms')}"
            )
        if overall.get('proof_next_qualifying_slot_at') != case.get('expect_proof_next_qualifying_slot_at'):
            failures.append(
                'overall.proof_next_qualifying_slot_at verwacht '
                f"{case.get('expect_proof_next_qualifying_slot_at')}, kreeg {overall.get('proof_next_qualifying_slot_at')}"
            )
        if overall.get('proof_next_qualifying_slot_remaining_ms') != case.get('expect_proof_next_qualifying_slot_remaining_ms'):
            failures.append(
                'overall.proof_next_qualifying_slot_remaining_ms verwacht '
                f"{case.get('expect_proof_next_qualifying_slot_remaining_ms')}, kreeg {overall.get('proof_next_qualifying_slot_remaining_ms')}"
            )
        if overall.get('proof_target_due_at') != case.get('expect_proof_target_due_at'):
            failures.append(
                'overall.proof_target_due_at verwacht '
                f"{case.get('expect_proof_target_due_at')}, kreeg {overall.get('proof_target_due_at')}"
            )
        if overall.get('proof_target_due_at_if_next_slot_missed') != case.get('expect_proof_target_due_at_if_next_slot_missed'):
            failures.append(
                'overall.proof_target_due_at_if_next_slot_missed verwacht '
                f"{case.get('expect_proof_target_due_at_if_next_slot_missed')}, kreeg {overall.get('proof_target_due_at_if_next_slot_missed')}"
            )
        if overall.get('proof_schedule_slip_ms') != case.get('expect_proof_schedule_slip_ms'):
            failures.append(
                'overall.proof_schedule_slip_ms verwacht '
                f"{case.get('expect_proof_schedule_slip_ms')}, kreeg {overall.get('proof_schedule_slip_ms')}"
            )

        quiet_text = ' || '.join(
            bit for bit in [quiet_proc.stdout.strip(), quiet_proc.stderr.strip()] if bit
        )
        for snippet in case.get('expect_quiet_substrings', []):
            if snippet not in quiet_text:
                failures.append(f"verwachte producer-quiet-tekst ontbreekt: {snippet}")
        for snippet in case.get('expect_quiet_absent_substrings', []):
            if snippet in quiet_text:
                failures.append(f"producer-quiet-tekst had juist moeten ontbreken: {snippet}")
        if overall.get('proof_freshness_text') and overall['proof_freshness_text'] not in quiet_text:
            failures.append(
                'producer-quiet-tekst mist proof_freshness_text uit overall/stdout-json: '
                f"{overall.get('proof_freshness_text')}"
            )
        if overall.get('proof_plan_text') and overall['proof_plan_text'] not in quiet_text:
            failures.append(
                'producer-quiet-tekst mist proof_plan_text uit overall/stdout-json: '
                f"{overall.get('proof_plan_text')}"
            )
        quiet_examples_text = (
            'outputvoorbeelden: ' + '; '.join((overall.get('summary_output_examples') or [])[:2])
            if overall.get('summary_output_examples') else None
        )
        if quiet_examples_text and quiet_examples_text not in quiet_text:
            failures.append(
                'producer-quiet-tekst mist outputvoorbeelden uit overall/stdout-json: '
                f'{quiet_examples_text}'
            )

        json_text = ' || '.join(
            str(bit)
            for bit in [
                overall.get('summary'),
                overall.get('result_text'),
                overall.get('reference_context_text'),
                overall.get('proof_blocker_text'),
                overall.get('proof_next_action_window_text'),
                overall.get('proof_recheck_commands_text'),
            ]
            if bit
        )
        for snippet in case.get('expect_json_substrings', []):
            if snippet not in json_text:
                failures.append(f"verwachte producer-json-tekst ontbreekt: {snippet}")

        artifact_base = Path(temp_dir)
        json_artifact = artifact_base / 'ai-briefing-proof-recheck.json'
        text_artifact = artifact_base / 'ai-briefing-proof-recheck.txt'
        jsonl_artifact = artifact_base / 'ai-briefing-proof-recheck.jsonl'
        expected_artifacts = [json_artifact, text_artifact, jsonl_artifact]
        overall_consumer_output_paths = overall.get('consumer_output_paths') or []
        expected_artifact_paths = [str(path.resolve()) for path in expected_artifacts]
        if sorted(overall_consumer_output_paths) != sorted(expected_artifact_paths):
            failures.append(
                'overall.consumer_output_paths verwacht '
                f"{expected_artifact_paths}, kreeg {overall_consumer_output_paths}"
            )
        overall_consumer_output_channels = overall.get('consumer_output_channels') or []
        expected_channels = ['board-json', 'board-text', 'eventlog-jsonl']
        if sorted(overall_consumer_output_channels) != sorted(expected_channels):
            failures.append(
                f"overall.consumer_output_channels verwacht {expected_channels}, kreeg {overall_consumer_output_channels}"
            )
        overall_consumer_outputs_text = overall.get('consumer_outputs_text') or ''
        for expected_channel, expected_path in zip(expected_channels, expected_artifact_paths):
            expected_fragment = f'{expected_channel}: {expected_path}'
            if expected_fragment not in overall_consumer_outputs_text:
                failures.append(
                    'overall.consumer_outputs_text mist verwacht fragment: '
                    f'{expected_fragment}'
                )
        overall_consumer_outputs = overall.get('consumer_outputs') or []
        if len(overall_consumer_outputs) != len(expected_artifacts):
            failures.append(
                f"overall.consumer_outputs verwacht {len(expected_artifacts)} items, kreeg {len(overall_consumer_outputs)}"
            )
        if overall.get('consumer_effective_output_source') != 'written':
            failures.append(
                'overall.consumer_effective_output_source verwacht written, kreeg '
                f"{overall.get('consumer_effective_output_source')}"
            )
        overall_effective_output_paths = overall.get('consumer_effective_output_paths') or []
        if sorted(overall_effective_output_paths) != sorted(expected_artifact_paths):
            failures.append(
                'overall.consumer_effective_output_paths verwacht '
                f"{expected_artifact_paths}, kreeg {overall_effective_output_paths}"
            )
        overall_effective_output_channels = overall.get('consumer_effective_output_channels') or []
        if sorted(overall_effective_output_channels) != sorted(expected_channels):
            failures.append(
                f"overall.consumer_effective_output_channels verwacht {expected_channels}, kreeg {overall_effective_output_channels}"
            )
        overall_effective_outputs_text = overall.get('consumer_effective_outputs_text') or ''
        for expected_channel, expected_path in zip(expected_channels, expected_artifact_paths):
            expected_fragment = f'{expected_channel}: {expected_path}'
            if expected_fragment not in overall_effective_outputs_text:
                failures.append(
                    'overall.consumer_effective_outputs_text mist verwacht fragment: '
                    f'{expected_fragment}'
                )
        if overall.get('consumer_effective_outputs_match_requested') is not True:
            failures.append(
                'overall.consumer_effective_outputs_match_requested verwacht True, kreeg '
                f"{overall.get('consumer_effective_outputs_match_requested')}"
            )
        if overall.get('consumer_effective_outputs_count_text') != 'consumer-effectieve-output-telling gevraagd=3, effectief=3, ontbrekend=0, onverwacht=0':
            failures.append(
                'overall.consumer_effective_outputs_count_text verwacht consumer-effectieve-output-telling gevraagd=3, effectief=3, ontbrekend=0, onverwacht=0, kreeg '
                f"{overall.get('consumer_effective_outputs_count_text')}"
            )
        if overall.get('consumer_effective_output_channel_count') != len(expected_channels):
            failures.append(
                'overall.consumer_effective_output_channel_count verwacht '
                f"{len(expected_channels)}, kreeg {overall.get('consumer_effective_output_channel_count')}"
            )
        overall_effective_output_channel_count_text = overall.get('consumer_effective_output_channel_count_text') or ''
        if overall_effective_output_channel_count_text != 'consumer-effectieve-output-kanalen effectief=3, kanalen=3':
            failures.append(
                'overall.consumer_effective_output_channel_count_text verwacht consumer-effectieve-output-kanalen effectief=3, kanalen=3, kreeg '
                f'{overall_effective_output_channel_count_text}'
            )
        overall_effective_output_source_text = overall.get('consumer_effective_output_source_text') or ''
        if overall_effective_output_source_text != 'consumer-effectieve-outputbron: geschreven artifacts':
            failures.append(
                'overall.consumer_effective_output_source_text verwacht consumer-effectieve-outputbron: geschreven artifacts, kreeg '
                f'{overall_effective_output_source_text}'
            )
        overall_effective_output_channels_text = overall.get('consumer_effective_output_channels_text') or ''
        if overall_effective_output_channels_text != 'consumer-effectieve-output-kanalen: board-json, board-text, eventlog-jsonl':
            failures.append(
                'overall.consumer_effective_output_channels_text verwacht consumer-effectieve-output-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                f'{overall_effective_output_channels_text}'
            )
        overall_effective_outputs_status_text = overall.get('consumer_effective_outputs_status_text') or ''
        if 'consumer-effectieve-output-audit ok' not in overall_effective_outputs_status_text:
            failures.append(
                'overall.consumer_effective_outputs_status_text mist consumer-effectieve-output-audit ok: '
                f'{overall_effective_outputs_status_text}'
            )
        if overall.get('consumer_effective_outputs_status_kind') != 'ok':
            failures.append(
                'overall.consumer_effective_outputs_status_kind verwacht ok, kreeg '
                f"{overall.get('consumer_effective_outputs_status_kind')}"
            )
        if overall.get('consumer_requested_output_count') != len(expected_artifacts):
            failures.append(
                'overall.consumer_requested_output_count verwacht '
                f"{len(expected_artifacts)}, kreeg {overall.get('consumer_requested_output_count')}"
            )
        if overall.get('consumer_requested_output_channel_count') != len(expected_channels):
            failures.append(
                'overall.consumer_requested_output_channel_count verwacht '
                f"{len(expected_channels)}, kreeg {overall.get('consumer_requested_output_channel_count')}"
            )
        overall_consumer_requested_output_count_text = overall.get('consumer_requested_output_count_text') or ''
        if overall_consumer_requested_output_count_text != 'consumer-output-aanvraag gevraagd=3, kanalen=3':
            failures.append(
                'overall.consumer_requested_output_count_text verwacht consumer-output-aanvraag gevraagd=3, kanalen=3, kreeg '
                f'{overall_consumer_requested_output_count_text}'
            )
        overall_consumer_requested_output_channel_count_text = overall.get('consumer_requested_output_channel_count_text') or ''
        if overall_consumer_requested_output_channel_count_text != 'consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3':
            failures.append(
                'overall.consumer_requested_output_channel_count_text verwacht consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3, kreeg '
                f'{overall_consumer_requested_output_channel_count_text}'
            )
        overall_consumer_requested_output_channels_text = overall.get('consumer_requested_output_channels_text') or ''
        if overall_consumer_requested_output_channels_text != 'consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl':
            failures.append(
                'overall.consumer_requested_output_channels_text verwacht consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                f'{overall_consumer_requested_output_channels_text}'
            )
        overall_consumer_requested_outputs_status_text = overall.get('consumer_requested_outputs_status_text') or ''
        if overall_consumer_requested_outputs_status_text != 'consumer-output-aanvraag vastgelegd voor 3 artifact(s)':
            failures.append(
                'overall.consumer_requested_outputs_status_text verwacht consumer-output-aanvraag vastgelegd voor 3 artifact(s), kreeg '
                f'{overall_consumer_requested_outputs_status_text}'
            )
        if overall.get('consumer_requested_outputs_status_kind') != 'requested':
            failures.append(
                'overall.consumer_requested_outputs_status_kind verwacht requested, kreeg '
                f"{overall.get('consumer_requested_outputs_status_kind')}"
            )
        if overall.get('consumer_output_count') != len(expected_artifacts):
            failures.append(
                'overall.consumer_output_count verwacht '
                f"{len(expected_artifacts)}, kreeg {overall.get('consumer_output_count')}"
            )
        if overall.get('consumer_output_channel_count') != len(expected_channels):
            failures.append(
                'overall.consumer_output_channel_count verwacht '
                f"{len(expected_channels)}, kreeg {overall.get('consumer_output_channel_count')}"
            )
        if overall.get('consumer_outputs_match_requested') is not True:
            failures.append(
                'overall.consumer_outputs_match_requested verwacht True, kreeg '
                f"{overall.get('consumer_outputs_match_requested')}"
            )
        overall_consumer_outputs_count_text = overall.get('consumer_outputs_count_text') or ''
        if overall_consumer_outputs_count_text != 'consumer-output-telling gevraagd=3, geschreven=3, ontbrekend=0, onverwacht=0':
            failures.append(
                'overall.consumer_outputs_count_text verwacht consumer-output-telling gevraagd=3, geschreven=3, ontbrekend=0, onverwacht=0, kreeg '
                f'{overall_consumer_outputs_count_text}'
            )
        overall_consumer_output_channel_count_text = overall.get('consumer_output_channel_count_text') or ''
        if overall_consumer_output_channel_count_text != 'consumer-output-kanalen geschreven=3, kanalen=3':
            failures.append(
                'overall.consumer_output_channel_count_text verwacht consumer-output-kanalen geschreven=3, kanalen=3, kreeg '
                f'{overall_consumer_output_channel_count_text}'
            )
        overall_consumer_output_channels_text = overall.get('consumer_output_channels_text') or ''
        if overall_consumer_output_channels_text != 'consumer-output-kanalen: board-json, board-text, eventlog-jsonl':
            failures.append(
                'overall.consumer_output_channels_text verwacht consumer-output-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                f'{overall_consumer_output_channels_text}'
            )
        overall_consumer_outputs_status_text = overall.get('consumer_outputs_status_text') or ''
        if 'consumer-output-audit ok' not in overall_consumer_outputs_status_text:
            failures.append(
                'overall.consumer_outputs_status_text mist consumer-output-audit ok: '
                f'{overall_consumer_outputs_status_text}'
            )
        if overall.get('consumer_outputs_status_kind') != 'ok':
            failures.append(
                'overall.consumer_outputs_status_kind verwacht ok, kreeg '
                f"{overall.get('consumer_outputs_status_kind')}"
            )
        if overall.get('consumer_outputs_missing_count') not in (0, None):
            failures.append(
                'overall.consumer_outputs_missing_count verwacht 0, kreeg '
                f"{overall.get('consumer_outputs_missing_count')}"
            )
        if overall.get('consumer_outputs_missing') not in ([], None):
            failures.append(
                f"overall.consumer_outputs_missing verwacht [], kreeg {overall.get('consumer_outputs_missing')}"
            )
        if overall.get('consumer_outputs_unexpected_count') not in (0, None):
            failures.append(
                'overall.consumer_outputs_unexpected_count verwacht 0, kreeg '
                f"{overall.get('consumer_outputs_unexpected_count')}"
            )
        if overall.get('consumer_outputs_unexpected') not in ([], None):
            failures.append(
                f"overall.consumer_outputs_unexpected verwacht [], kreeg {overall.get('consumer_outputs_unexpected')}"
            )
        for artifact in expected_artifacts:
            if not artifact.exists():
                failures.append(f'artifact ontbreekt: {artifact}')

        artifact_json_payload = {}
        artifact_text = ''
        artifact_jsonl_payload = {}
        if json_artifact.exists():
            try:
                artifact_json_payload = json.loads(json_artifact.read_text(encoding='utf-8'))
            except json.JSONDecodeError as exc:
                failures.append(f'ongeldige JSON-artifact {json_artifact}: {exc}')
        if text_artifact.exists():
            artifact_text = text_artifact.read_text(encoding='utf-8')
        if jsonl_artifact.exists():
            jsonl_lines = [line for line in jsonl_artifact.read_text(encoding='utf-8').splitlines() if line.strip()]
            if not jsonl_lines:
                failures.append(f'lege JSONL-artifact {jsonl_artifact}')
            else:
                try:
                    artifact_jsonl_payload = json.loads(jsonl_lines[-1])
                except json.JSONDecodeError as exc:
                    failures.append(f'ongeldige JSONL-artifact {jsonl_artifact}: {exc}')

        for artifact_payload, label in ((artifact_json_payload, 'json-artifact'), (artifact_jsonl_payload, 'jsonl-artifact')):
            if artifact_payload:
                if case.get('expect_proof_config_hash_present') and not artifact_payload.get('proof_config_hash'):
                    failures.append(f'{label} mist proof_config_hash')
                if artifact_payload.get('last_run_config_relation_text') and not artifact_payload.get('last_run_config_relation'):
                    failures.append(f'{label} mist last_run_config_relation terwijl last_run_config_relation_text wel gezet is')
                if artifact_payload.get('consumer_requested_output_count') != len(expected_artifacts):
                    failures.append(
                        f'{label} consumer_requested_output_count verwacht {len(expected_artifacts)}, kreeg '
                        f"{artifact_payload.get('consumer_requested_output_count')}"
                    )
                if artifact_payload.get('consumer_requested_output_channel_count') != len(expected_channels):
                    failures.append(
                        f'{label} consumer_requested_output_channel_count verwacht {len(expected_channels)}, kreeg '
                        f"{artifact_payload.get('consumer_requested_output_channel_count')}"
                    )
                artifact_consumer_requested_output_count_text = artifact_payload.get('consumer_requested_output_count_text') or ''
                if artifact_consumer_requested_output_count_text != 'consumer-output-aanvraag gevraagd=3, kanalen=3':
                    failures.append(
                        f'{label} consumer_requested_output_count_text verwacht consumer-output-aanvraag gevraagd=3, kanalen=3, kreeg '
                        f'{artifact_consumer_requested_output_count_text}'
                    )
                artifact_consumer_requested_output_channel_count_text = artifact_payload.get('consumer_requested_output_channel_count_text') or ''
                if artifact_consumer_requested_output_channel_count_text != 'consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3':
                    failures.append(
                        f'{label} consumer_requested_output_channel_count_text verwacht consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3, kreeg '
                        f'{artifact_consumer_requested_output_channel_count_text}'
                    )
                artifact_consumer_requested_output_channels_text = artifact_payload.get('consumer_requested_output_channels_text') or ''
                if artifact_consumer_requested_output_channels_text != 'consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl':
                    failures.append(
                        f'{label} consumer_requested_output_channels_text verwacht consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                        f'{artifact_consumer_requested_output_channels_text}'
                    )
                artifact_consumer_requested_outputs_status_text = artifact_payload.get('consumer_requested_outputs_status_text') or ''
                if artifact_consumer_requested_outputs_status_text != 'consumer-output-aanvraag vastgelegd voor 3 artifact(s)':
                    failures.append(
                        f'{label} consumer_requested_outputs_status_text verwacht consumer-output-aanvraag vastgelegd voor 3 artifact(s), kreeg '
                        f'{artifact_consumer_requested_outputs_status_text}'
                    )
                if artifact_payload.get('consumer_output_count') != len(expected_artifacts):
                    failures.append(
                        f'{label} consumer_output_count verwacht {len(expected_artifacts)}, kreeg '
                        f"{artifact_payload.get('consumer_output_count')}"
                    )
                if artifact_payload.get('consumer_output_channel_count') != len(expected_channels):
                    failures.append(
                        f'{label} consumer_output_channel_count verwacht {len(expected_channels)}, kreeg '
                        f"{artifact_payload.get('consumer_output_channel_count')}"
                    )
                if artifact_payload.get('consumer_outputs_match_requested') is not True:
                    failures.append(
                        f'{label} consumer_outputs_match_requested verwacht True, kreeg '
                        f"{artifact_payload.get('consumer_outputs_match_requested')}"
                    )
                artifact_consumer_outputs_count_text = artifact_payload.get('consumer_outputs_count_text') or ''
                if artifact_consumer_outputs_count_text != 'consumer-output-telling gevraagd=3, geschreven=3, ontbrekend=0, onverwacht=0':
                    failures.append(
                        f'{label} consumer_outputs_count_text verwacht consumer-output-telling gevraagd=3, geschreven=3, ontbrekend=0, onverwacht=0, kreeg '
                        f'{artifact_consumer_outputs_count_text}'
                    )
                artifact_consumer_output_channel_count_text = artifact_payload.get('consumer_output_channel_count_text') or ''
                if artifact_consumer_output_channel_count_text != 'consumer-output-kanalen geschreven=3, kanalen=3':
                    failures.append(
                        f'{label} consumer_output_channel_count_text verwacht consumer-output-kanalen geschreven=3, kanalen=3, kreeg '
                        f'{artifact_consumer_output_channel_count_text}'
                    )
                artifact_consumer_output_channels_text = artifact_payload.get('consumer_output_channels_text') or ''
                if artifact_consumer_output_channels_text != 'consumer-output-kanalen: board-json, board-text, eventlog-jsonl':
                    failures.append(
                        f'{label} consumer_output_channels_text verwacht consumer-output-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                        f'{artifact_consumer_output_channels_text}'
                    )
                artifact_consumer_outputs_status_text = artifact_payload.get('consumer_outputs_status_text') or ''
                if 'consumer-output-audit ok' not in artifact_consumer_outputs_status_text:
                    failures.append(
                        f'{label} consumer_outputs_status_text mist consumer-output-audit ok: '
                        f'{artifact_consumer_outputs_status_text}'
                    )
                if artifact_payload.get('consumer_effective_outputs_match_requested') is not True:
                    failures.append(
                        f'{label} consumer_effective_outputs_match_requested verwacht True, kreeg '
                        f"{artifact_payload.get('consumer_effective_outputs_match_requested')}"
                    )
                artifact_effective_outputs_count_text = artifact_payload.get('consumer_effective_outputs_count_text') or ''
                if artifact_effective_outputs_count_text != 'consumer-effectieve-output-telling gevraagd=3, effectief=3, ontbrekend=0, onverwacht=0':
                    failures.append(
                        f'{label} consumer_effective_outputs_count_text verwacht consumer-effectieve-output-telling gevraagd=3, effectief=3, ontbrekend=0, onverwacht=0, kreeg '
                        f'{artifact_effective_outputs_count_text}'
                    )
                if artifact_payload.get('consumer_effective_output_channel_count') != len(expected_channels):
                    failures.append(
                        f'{label} consumer_effective_output_channel_count verwacht {len(expected_channels)}, kreeg '
                        f"{artifact_payload.get('consumer_effective_output_channel_count')}"
                    )
                artifact_effective_output_channel_count_text = artifact_payload.get('consumer_effective_output_channel_count_text') or ''
                if artifact_effective_output_channel_count_text != 'consumer-effectieve-output-kanalen effectief=3, kanalen=3':
                    failures.append(
                        f'{label} consumer_effective_output_channel_count_text verwacht consumer-effectieve-output-kanalen effectief=3, kanalen=3, kreeg '
                        f'{artifact_effective_output_channel_count_text}'
                    )
                artifact_effective_output_source_text = artifact_payload.get('consumer_effective_output_source_text') or ''
                if artifact_effective_output_source_text != 'consumer-effectieve-outputbron: geschreven artifacts':
                    failures.append(
                        f'{label} consumer_effective_output_source_text verwacht consumer-effectieve-outputbron: geschreven artifacts, kreeg '
                        f'{artifact_effective_output_source_text}'
                    )
                artifact_effective_output_channels_text = artifact_payload.get('consumer_effective_output_channels_text') or ''
                if artifact_effective_output_channels_text != 'consumer-effectieve-output-kanalen: board-json, board-text, eventlog-jsonl':
                    failures.append(
                        f'{label} consumer_effective_output_channels_text verwacht consumer-effectieve-output-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                        f'{artifact_effective_output_channels_text}'
                    )
                artifact_effective_outputs_status_text = artifact_payload.get('consumer_effective_outputs_status_text') or ''
                if 'consumer-effectieve-output-audit ok' not in artifact_effective_outputs_status_text:
                    failures.append(
                        f'{label} consumer_effective_outputs_status_text mist consumer-effectieve-output-audit ok: '
                        f'{artifact_effective_outputs_status_text}'
                    )
                if artifact_payload.get('consumer_outputs_missing_count') not in (0, None):
                    failures.append(
                        f'{label} consumer_outputs_missing_count verwacht 0, kreeg '
                        f"{artifact_payload.get('consumer_outputs_missing_count')}"
                    )
                if artifact_payload.get('consumer_outputs_unexpected_count') not in (0, None):
                    failures.append(
                        f'{label} consumer_outputs_unexpected_count verwacht 0, kreeg '
                        f"{artifact_payload.get('consumer_outputs_unexpected_count')}"
                    )
                if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
                    artifact_audit_ok = ((artifact_payload.get('proof_recheck_schedule_audit') or {}).get('ok'))
                    if artifact_audit_ok != case.get('expect_proof_recheck_schedule_audit_ok'):
                        failures.append(
                            f'{label} proof_recheck_schedule_audit.ok verwacht '
                            f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {artifact_audit_ok}"
                        )
                    if artifact_payload.get('proof_recheck_schedule_ok') != case.get('expect_proof_recheck_schedule_audit_ok'):
                        failures.append(
                            f'{label} proof_recheck_schedule_ok verwacht '
                            f"{case.get('expect_proof_recheck_schedule_audit_ok')}, kreeg {artifact_payload.get('proof_recheck_schedule_ok')}"
                        )
                if case.get('expect_proof_recheck_schedule_matches_grace') is not None:
                    if artifact_payload.get('proof_recheck_schedule_matches_grace') != case.get('expect_proof_recheck_schedule_matches_grace'):
                        failures.append(
                            f'{label} proof_recheck_schedule_matches_grace verwacht '
                            f"{case.get('expect_proof_recheck_schedule_matches_grace')}, kreeg {artifact_payload.get('proof_recheck_schedule_matches_grace')}"
                        )
                if case.get('expect_proof_recheck_schedule_audit_ok') is not None:
                    if artifact_payload.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
                        failures.append(
                            f'{label} proof_recheck_schedule_job_name verwacht '
                            f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {artifact_payload.get('proof_recheck_schedule_job_name')}"
                        )
                    if artifact_payload.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
                        failures.append(
                            f'{label} proof_recheck_schedule_expr verwacht '
                            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {artifact_payload.get('proof_recheck_schedule_expr')}"
                        )
                    if artifact_payload.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
                        failures.append(
                            f'{label} proof_recheck_schedule_tz verwacht '
                            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {artifact_payload.get('proof_recheck_schedule_tz')}"
                        )
                    if artifact_payload.get('proof_recheck_schedule_expected_gap_minutes') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES:
                        failures.append(
                            f'{label} proof_recheck_schedule_expected_gap_minutes verwacht '
                            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES}, kreeg {artifact_payload.get('proof_recheck_schedule_expected_gap_minutes')}"
                        )
                    if artifact_payload.get('proof_recheck_schedule_same_day_after_target') is not True:
                        failures.append(
                            f'{label} proof_recheck_schedule_same_day_after_target verwacht True, kreeg '
                            f"{artifact_payload.get('proof_recheck_schedule_same_day_after_target')}"
                        )
                if artifact_payload.get('result_kind') != case['expect_result_kind']:
                    failures.append(
                        f"{label} result_kind verwacht {case['expect_result_kind']}, kreeg {artifact_payload.get('result_kind')}"
                    )
                if artifact_payload.get('proof_state') != case['expect_proof_state']:
                    failures.append(
                        f"{label} proof_state verwacht {case['expect_proof_state']}, kreeg {artifact_payload.get('proof_state')}"
                    )
                if artifact_payload.get('proof_freshness_text') != overall.get('proof_freshness_text'):
                    failures.append(
                        f'{label} proof_freshness_text verwacht pariteit met overall/stdout-json {overall.get("proof_freshness_text")}, kreeg '
                        f"{artifact_payload.get('proof_freshness_text')}"
                    )
                if artifact_payload.get('proof_plan_text') != overall.get('proof_plan_text'):
                    failures.append(
                        f'{label} proof_plan_text verwacht pariteit met overall/stdout-json {overall.get("proof_plan_text")}, kreeg '
                        f"{artifact_payload.get('proof_plan_text')}"
                    )
                if artifact_payload.get('summary_output_examples') != overall.get('summary_output_examples'):
                    failures.append(
                        f'{label} summary_output_examples verwacht pariteit met overall/stdout-json {overall.get("summary_output_examples")}, kreeg '
                        f"{artifact_payload.get('summary_output_examples')}"
                    )

        text_artifact_examples_text = (
            'outputvoorbeelden: ' + '; '.join((overall.get('summary_output_examples') or [])[:2])
            if overall.get('summary_output_examples') else None
        )
        if overall.get('proof_freshness_text') and overall['proof_freshness_text'] not in artifact_text:
            failures.append(
                'board-text-artifact mist proof_freshness_text uit overall/stdout-json: '
                f"{overall.get('proof_freshness_text')}"
            )
        if overall.get('proof_plan_text') and overall['proof_plan_text'] not in artifact_text:
            failures.append(
                'board-text-artifact mist proof_plan_text uit overall/stdout-json: '
                f"{overall.get('proof_plan_text')}"
            )
        if text_artifact_examples_text and text_artifact_examples_text not in artifact_text:
            failures.append(
                'board-text-artifact mist outputvoorbeelden uit overall/stdout-json: '
                f'{text_artifact_examples_text}'
            )

        artifact_text_combined = ' || '.join(
            bit
            for bit in [
                artifact_text,
                json.dumps(artifact_json_payload, ensure_ascii=False) if artifact_json_payload else '',
                json.dumps(artifact_jsonl_payload, ensure_ascii=False) if artifact_jsonl_payload else '',
                overall.get('proof_freshness_text') or '',
                overall.get('proof_plan_text') or '',
                text_artifact_examples_text or '',
                quiet_text,
                json_text,
            ]
            if bit
        )
        for snippet in case.get('expect_artifact_substrings', []):
            if snippet not in artifact_text_combined:
                failures.append(f"verwachte artifact-tekst ontbreekt: {snippet}")

        return {
            'name': case['name'],
            'path': str(PROOF_RECHECK_PRODUCER_SCRIPT),
            'ok': not failures,
            'failures': failures,
            'audit_ok': payload.get('ok'),
            'audit_text': json_text or quiet_text or artifact_text_combined,
            'item_count': None,
            'items_with_source_count': None,
            'items_with_valid_source_line_count': None,
            'items_with_invalid_source_line_count': None,
            'first3_items_with_source_count': None,
            'first3_items_with_valid_source_line_count': None,
            'first3_items_with_multiple_sources_count': None,
            'first3_items_with_primary_source_count': None,
            'first3_primary_source_family_count': None,
            'first3_primary_fresh_item_count': None,
            'explicit_dated_item_count': None,
            'explicit_recent_dated_first3_count': None,
            'explicit_fresh_dated_first3_count': None,
            'future_dated_item_count': None,
            'invalid_source_line_issue_counts': None,
            'exact_field_line_counts': None,
            'items_with_exact_field_order_count': None,
            'items_with_field_order_mismatch_count': None,
            'numbered_title_heading_count': None,
        }



def evaluate_producer_quiet_requested_outputs_fallback_case(producer_module):
    failures = []
    payload = {
        'summary': 'synthetische producer-mismatch',
        'result_text': 'consumer-write mismatch gedetecteerd',
        'consumer_requested_outputs_text': 'consumer-artifacts: board-json: /tmp/expected.json; board-text: /tmp/expected.txt',
        'consumer_requested_output_channels_text': 'consumer-output-aanvraag-kanalen: board-json, board-text',
        'consumer_requested_outputs': [
            {'channel': 'board-json', 'path': '/tmp/expected.json', 'format': 'json', 'append': False},
            {'channel': 'board-text', 'path': '/tmp/expected.txt', 'format': 'text', 'append': False},
        ],
        'consumer_outputs': [],
        'consumer_outputs_text': None,
        'consumer_output_channels_text': 'consumer-output-kanalen: geen',
        'consumer_effective_output_source': 'requested-fallback',
        'consumer_effective_output_source_text': 'consumer-effectieve-outputbron: aangevraagde artifacts als fallback',
        'consumer_effective_outputs': [
            {'channel': 'board-json', 'path': '/tmp/expected.json', 'format': 'json', 'append': False},
            {'channel': 'board-text', 'path': '/tmp/expected.txt', 'format': 'text', 'append': False},
        ],
        'consumer_effective_outputs_text': 'consumer-artifacts: board-json: /tmp/expected.json; board-text: /tmp/expected.txt',
        'consumer_effective_output_channels_text': 'consumer-effectieve-output-kanalen: board-json, board-text',
        'consumer_effective_outputs_match_requested': True,
        'consumer_effective_outputs_count_text': 'consumer-effectieve-output-telling gevraagd=2, effectief=2, ontbrekend=0, onverwacht=0',
        'consumer_effective_outputs_status_text': 'consumer-effectieve-output-audit ok (2/2 gevraagde artifacts gedekt via requested-fallback)',
        'consumer_outputs_count_text': 'consumer-output-telling gevraagd=2, geschreven=0, ontbrekend=2, onverwacht=0',
        'consumer_outputs_missing_text': 'consumer-artifacts: board-json: /tmp/expected.json; board-text: /tmp/expected.txt',
        'consumer_outputs_unexpected_text': None,
        'consumer_outputs_status_text': 'consumer-output-audit mismatch (ontbreekt: board-json: /tmp/expected.json; board-text: /tmp/expected.txt)',
        'consumer_effective_outputs_missing_text': None,
        'consumer_effective_outputs_unexpected_text': None,
        'result_kind': 'attention-needed',
    }


    quiet_summary, extracted_payload = producer_module.build_quiet_summary(
        json.dumps(payload, ensure_ascii=False),
        '',
        3,
    )
    if extracted_payload != payload:
        failures.append('build_quiet_summary gaf niet dezelfde payload terug voor synthetische JSON-input')
    if not quiet_summary:
        failures.append('build_quiet_summary gaf geen quiet-summary terug voor synthetische mismatchpayload')
        quiet_summary = ''
    expected_snippets = [
        'consumer-artifacts: board-json: /tmp/expected.json; board-text: /tmp/expected.txt',
        'consumer-output-aanvraag-kanalen: board-json, board-text',
        'consumer-output-kanalen: geen',
        'consumer-output-telling gevraagd=2, geschreven=0, ontbrekend=2, onverwacht=0',
        'consumer-output-audit mismatch',
        'consumer-artifacts: board-json: /tmp/expected.json; board-text: /tmp/expected.txt',
        'consumer-effectieve-outputbron: aangevraagde artifacts als fallback',
        'consumer-effectieve-output-kanalen: board-json, board-text',
        'consumer-effectieve-output-telling gevraagd=2, effectief=2, ontbrekend=0, onverwacht=0',
        'consumer-effectieve-output-audit ok (2/2 gevraagde artifacts gedekt via requested-fallback)',
        'resultaat: attention-needed',
    ]
    if extracted_payload and extracted_payload.get('consumer_effective_output_source') != 'requested-fallback':
        failures.append(
            'build_quiet_summary payload consumer_effective_output_source verwacht requested-fallback, kreeg '
            f"{extracted_payload.get('consumer_effective_output_source')}"
        )
    for snippet in expected_snippets:
        if snippet not in quiet_summary:
            failures.append(f'producer quiet-summary mist fallback-fragment: {snippet}')

    return {
        'name': 'proof-recheck-producer-quiet-falls-back-to-requested-outputs',
        'path': str(PROOF_RECHECK_PRODUCER_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': quiet_summary,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_brief_consumer_case(case):
    script = Path(case['script'])
    expected_status = run_status_json(case['reference_ms'])
    json_proc = subprocess.run(
        ['python3', str(script), '--json', '--reference-ms', str(case['reference_ms'])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    text_proc = subprocess.run(
        ['python3', str(script), '--reference-ms', str(case['reference_ms'])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    failures = []
    json_output = json_proc.stdout.strip() or json_proc.stderr.strip()
    text_output = text_proc.stdout.strip() or text_proc.stderr.strip()

    if json_proc.returncode != 0:
        failures.append(f"json-exitcode verwacht 0, kreeg {json_proc.returncode}")
        payload = {}
    elif not json_output:
        failures.append(f'geen JSON-output van {script.name}')
        payload = {}
    else:
        try:
            payload = json.loads(json_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van {script.name}: {exc}')
            payload = {}

    if text_proc.returncode != 0:
        failures.append(f"tekst-exitcode verwacht 0, kreeg {text_proc.returncode}")
    if not text_output:
        failures.append(f'geen tekstoutput van {script.name}')

    assert_runtime_metadata(payload, f'{script.name} stdout-json', failures)

    ai_briefing_status = payload.get('ai_briefing_status') or {}
    if ai_briefing_status:
        assert_runtime_metadata(ai_briefing_status, f'{script.name} nested ai_briefing_status', failures)
    if ai_briefing_status.get('proof_recheck_schedule_kind') != 'ok':
        failures.append(
            'ai_briefing_status.proof_recheck_schedule_kind verwacht ok, kreeg '
            f"{ai_briefing_status.get('proof_recheck_schedule_kind')}"
        )
    if ai_briefing_status.get('proof_recheck_schedule_kind_text') != 'proof-recheck-cronstatus: ok':
        failures.append(
            'ai_briefing_status.proof_recheck_schedule_kind_text verwacht '
            f"proof-recheck-cronstatus: ok, kreeg {ai_briefing_status.get('proof_recheck_schedule_kind_text')}"
        )
    if ai_briefing_status.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
        failures.append(
            'ai_briefing_status.proof_recheck_schedule_job_name verwacht '
            f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {ai_briefing_status.get('proof_recheck_schedule_job_name')}"
        )
    if ai_briefing_status.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
        failures.append(
            'ai_briefing_status.proof_recheck_schedule_expr verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {ai_briefing_status.get('proof_recheck_schedule_expr')}"
        )
    if ai_briefing_status.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
        failures.append(
            'ai_briefing_status.proof_recheck_schedule_tz verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {ai_briefing_status.get('proof_recheck_schedule_tz')}"
        )
    if ai_briefing_status.get('proof_state') != case['expect_proof_state']:
        failures.append(
            f"ai_briefing_status.proof_state verwacht {case['expect_proof_state']}, kreeg {ai_briefing_status.get('proof_state')}"
        )
    if ai_briefing_status.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
        failures.append(
            'ai_briefing_status.proof_next_action_kind verwacht '
            f"{case['expect_proof_next_action_kind']}, kreeg {ai_briefing_status.get('proof_next_action_kind')}"
        )
    expected_proof_plan_text = case.get('expect_proof_plan_text')
    if expected_proof_plan_text is not None and ai_briefing_status.get('proof_plan_text') != expected_proof_plan_text:
        failures.append(
            'ai_briefing_status.proof_plan_text verwacht '
            f"{expected_proof_plan_text}, kreeg {ai_briefing_status.get('proof_plan_text')}"
        )
    expected_last_run_config_relation_text = case.get('expect_last_run_config_relation_text')
    if (
        expected_last_run_config_relation_text is not None
        and ai_briefing_status.get('last_run_config_relation_text') != expected_last_run_config_relation_text
    ):
        failures.append(
            'ai_briefing_status.last_run_config_relation_text verwacht '
            f"{expected_last_run_config_relation_text}, kreeg {ai_briefing_status.get('last_run_config_relation_text')}"
        )
    if ai_briefing_status.get('last_run_config_relation_text') and not ai_briefing_status.get('last_run_config_relation'):
        failures.append(
            'ai_briefing_status.last_run_config_relation ontbreekt terwijl '
            'ai_briefing_status.last_run_config_relation_text wel gezet is'
        )
    if ai_briefing_status.get('proof_freshness_text') != expected_status.get('proof_freshness_text'):
        failures.append(
            'ai_briefing_status.proof_freshness_text verwacht '
            f"{expected_status.get('proof_freshness_text')}, kreeg {ai_briefing_status.get('proof_freshness_text')}"
        )
    if ai_briefing_status.get('proof_freshness_text') != ((ai_briefing_status.get('proof_freshness') or {}).get('text')):
        failures.append(
            'ai_briefing_status.proof_freshness_text verwacht alias-pariteit met '
            'ai_briefing_status.proof_freshness.text, kreeg '
            f"{ai_briefing_status.get('proof_freshness_text')} versus {((ai_briefing_status.get('proof_freshness') or {}).get('text'))}"
        )
    if ai_briefing_status.get('summary_output_examples') != expected_status.get('summary_output_examples'):
        failures.append(
            'ai_briefing_status.summary_output_examples verwacht '
            f"{expected_status.get('summary_output_examples')}, kreeg {ai_briefing_status.get('summary_output_examples')}"
        )
    if not isinstance(ai_briefing_status.get('summary_output_examples'), list):
        failures.append(
            'ai_briefing_status.summary_output_examples verwacht list, kreeg '
            f"{type(ai_briefing_status.get('summary_output_examples')).__name__}"
        )

    combined_text = ' || '.join(
        bit for bit in [
            ai_briefing_status.get('proof_recheck_schedule_text'),
            ai_briefing_status.get('proof_recheck_schedule_kind_text'),
            ai_briefing_status.get('proof_freshness_text'),
            ('outputvoorbeelden: ' + '; '.join((ai_briefing_status.get('summary_output_examples') or [])[:2]))
            if ai_briefing_status.get('summary_output_examples') else None,
            ai_briefing_status.get('proof_plan_text'),
            ai_briefing_status.get('last_run_config_relation_text'),
            ai_briefing_status.get('proof_next_action_window_text'),
            ai_briefing_status.get('proof_next_action_text'),
            text_output,
        ] if bit
    )
    for snippet in case.get('expect_text_substrings', []):
        if snippet not in combined_text:
            failures.append(f"verwachte brief-consumer-tekst ontbreekt: {snippet}")

    if ai_briefing_status.get('proof_freshness_text') and ai_briefing_status['proof_freshness_text'] not in text_output:
        failures.append(
            'brief-consumer-tekst mist proof_freshness_text uit ai_briefing_status: '
            f"{ai_briefing_status.get('proof_freshness_text')}"
        )
    if ai_briefing_status.get('proof_plan_text') and ai_briefing_status['proof_plan_text'] not in text_output:
        failures.append(
            'brief-consumer-tekst mist proof_plan_text uit ai_briefing_status: '
            f"{ai_briefing_status.get('proof_plan_text')}"
        )
    brief_example_text = (
        'outputvoorbeelden: ' + '; '.join((ai_briefing_status.get('summary_output_examples') or [])[:2])
        if ai_briefing_status.get('summary_output_examples') else None
    )
    if brief_example_text and brief_example_text not in text_output:
        failures.append(
            'brief-consumer-tekst mist summary_output_examples uit ai_briefing_status: '
            f'{brief_example_text}'
        )

    return {
        'name': case['name'],
        'path': str(script),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': combined_text,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def assert_runtime_metadata(payload: dict, label: str, failures: list[str]) -> None:
    generated_at = payload.get('generated_at')
    started_at = payload.get('started_at')
    generated_at_text = payload.get('generated_at_text')
    started_at_text = payload.get('started_at_text')
    duration_ms = payload.get('duration_ms')
    duration_seconds = payload.get('duration_seconds')
    duration_text = payload.get('duration_text')

    if not isinstance(generated_at, str) or not generated_at:
        failures.append(f'{label} generated_at hoort een niet-lege ISO-tijdstring te zijn')
    else:
        try:
            datetime.fromisoformat(generated_at)
        except ValueError as exc:
            failures.append(f'{label} generated_at hoort parsebare ISO-tijd te zijn, kreeg {exc}')

    if not isinstance(started_at, str) or not started_at:
        failures.append(f'{label} started_at hoort een niet-lege ISO-tijdstring te zijn')
    else:
        try:
            started_dt = datetime.fromisoformat(started_at)
            finished_dt = datetime.fromisoformat(generated_at) if isinstance(generated_at, str) and generated_at else None
            if finished_dt is not None and started_dt > finished_dt:
                failures.append(f'{label} started_at hoort niet ná generated_at te liggen')
        except ValueError as exc:
            failures.append(f'{label} started_at hoort parsebare ISO-tijd te zijn, kreeg {exc}')

    if not isinstance(generated_at_text, str) or not generated_at_text.strip():
        failures.append(f'{label} generated_at_text hoort een niet-lege teksttimestamp te zijn')
    if not isinstance(started_at_text, str) or not started_at_text.strip():
        failures.append(f'{label} started_at_text hoort een niet-lege teksttimestamp te zijn')
    if not isinstance(duration_ms, int) or duration_ms < 0:
        failures.append(f'{label} duration_ms hoort een niet-negatieve int te zijn')
    if not isinstance(duration_seconds, (int, float)) or duration_seconds < 0:
        failures.append(f'{label} duration_seconds hoort een niet-negatief getal te zijn')
    elif isinstance(duration_ms, int):
        expected_duration_seconds = round(duration_ms / 1000, 3)
        if abs(float(duration_seconds) - expected_duration_seconds) > 0.0005:
            failures.append(
                f'{label} duration_seconds hoort duration_ms/1000 af te ronden op 3 decimalen'
            )
    if not isinstance(duration_text, str) or not duration_text.endswith('s'):
        failures.append(f'{label} duration_text hoort een secondenlabel te zijn')
    elif isinstance(duration_seconds, (int, float)):
        expected_duration_text = f'{float(duration_seconds):.3f}s'
        if duration_text != expected_duration_text:
            failures.append(
                f'{label} duration_text hoort exact {expected_duration_text} te spiegelen, kreeg {duration_text}'
            )


def evaluate_watchdog_alert_case(case):
    mode = case.get('mode', 'proof-progress')
    expect_require_qualified_runs = case.get('expect_require_qualified_runs', 3)
    expected_status = run_status_json(case['reference_ms'])
    watchdog_json_cmd = [
        'python3',
        str(WATCHDOG_SCRIPT),
        '--json',
        '--require-qualified-runs',
        str(expect_require_qualified_runs),
        '--reference-ms',
        str(case['reference_ms']),
    ]
    json_cmd = [
        'python3',
        str(WATCHDOG_ALERT_SCRIPT),
        '--mode',
        mode,
        '--json',
        '--reference-ms',
        str(case['reference_ms']),
    ]
    text_cmd = [
        'python3',
        str(WATCHDOG_ALERT_SCRIPT),
        '--mode',
        mode,
        '--reference-ms',
        str(case['reference_ms']),
    ]
    consumer_bundle = case.get('consumer_bundle')
    consumer_root = None
    if consumer_bundle:
        consumer_root = Path(tempfile.mkdtemp(prefix='watchdog-alert-consumer-', dir=str(ROOT / 'tmp')))
        text_cmd.extend(['--consumer-root', str(consumer_root), '--consumer-bundle', consumer_bundle])

    json_proc = subprocess.run(
        json_cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    watchdog_json_proc = subprocess.run(
        watchdog_json_cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    proc = subprocess.run(
        text_cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    failures = []
    json_output = json_proc.stdout.strip() or json_proc.stderr.strip()
    watchdog_json_output = watchdog_json_proc.stdout.strip() or watchdog_json_proc.stderr.strip()
    text_output = proc.stdout.strip() or proc.stderr.strip()
    if json_proc.returncode != 0:
        failures.append(f"json-exitcode verwacht 0, kreeg {json_proc.returncode}")
        payload = {}
    elif not json_output:
        failures.append('geen JSON-output van ai-briefing-watchdog-alert.py')
        payload = {}
    else:
        try:
            payload = json.loads(json_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-watchdog-alert.py: {exc}')
            payload = {}

    if watchdog_json_proc.returncode not in (0, 2):
        failures.append(f"watchdog-json-exitcode verwacht 0 of 2, kreeg {watchdog_json_proc.returncode}")
        watchdog_payload = {}
    elif not watchdog_json_output:
        failures.append('geen JSON-output van ai-briefing-watchdog.py voor alert-pariteit')
        watchdog_payload = {}
    else:
        try:
            watchdog_payload = json.loads(watchdog_json_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-watchdog.py voor alert-pariteit: {exc}')
            watchdog_payload = {}

    if proc.returncode != 0:
        failures.append(f"tekst-exitcode verwacht 0, kreeg {proc.returncode}")
    if not text_output:
        failures.append('geen tekstoutput van ai-briefing-watchdog-alert.py')

    assert_runtime_metadata(payload, 'watchdog-alert stdout-json', failures)

    if payload.get('mode') != mode:
        failures.append(f"mode verwacht {mode}, kreeg {payload.get('mode')}")
    if payload.get('require_qualified_runs') != expect_require_qualified_runs:
        failures.append(
            f'require_qualified_runs verwacht {expect_require_qualified_runs}, kreeg '
            f"{payload.get('require_qualified_runs')}"
        )
    if payload.get('no_reply') is not case.get('expect_no_reply', False):
        failures.append(
            f"no_reply verwacht {case.get('expect_no_reply', False)}, kreeg {payload.get('no_reply')}"
        )
    if payload.get('suppressed_before_proof_deadline') is not case.get('expect_suppressed_before_proof_deadline', False):
        failures.append(
            'suppressed_before_proof_deadline verwacht '
            f"{case.get('expect_suppressed_before_proof_deadline', False)}, kreeg "
            f"{payload.get('suppressed_before_proof_deadline')}"
        )
    if payload.get('proof_recheck_schedule_kind') != 'ok':
        failures.append(
            'proof_recheck_schedule_kind verwacht ok, kreeg '
            f"{payload.get('proof_recheck_schedule_kind')}"
        )
    if payload.get('proof_recheck_schedule_kind_text') != 'proof-recheck-cronstatus: ok':
        failures.append(
            'proof_recheck_schedule_kind_text verwacht proof-recheck-cronstatus: ok, kreeg '
            f"{payload.get('proof_recheck_schedule_kind_text')}"
        )
    if payload.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
        failures.append(
            'proof_recheck_schedule_job_name verwacht '
            f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {payload.get('proof_recheck_schedule_job_name')}"
        )
    if payload.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
        failures.append(
            'proof_recheck_schedule_expr verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {payload.get('proof_recheck_schedule_expr')}"
        )
    if payload.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
        failures.append(
            'proof_recheck_schedule_tz verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {payload.get('proof_recheck_schedule_tz')}"
        )
    if payload.get('proof_state') != case['expect_proof_state']:
        failures.append(
            f"proof_state verwacht {case['expect_proof_state']}, kreeg {payload.get('proof_state')}"
        )
    if payload.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
        failures.append(
            'proof_next_action_kind verwacht '
            f"{case['expect_proof_next_action_kind']}, kreeg {payload.get('proof_next_action_kind')}"
        )
    if payload.get('proof_config_hash') != expected_status.get('proof_config_hash'):
        failures.append(
            'proof_config_hash verwacht '
            f"{expected_status.get('proof_config_hash')}, kreeg {payload.get('proof_config_hash')}"
        )
    if payload.get('proof_next_qualifying_slot_at') != expected_status.get('proof_next_qualifying_slot_at'):
        failures.append(
            'proof_next_qualifying_slot_at verwacht '
            f"{expected_status.get('proof_next_qualifying_slot_at')}, kreeg {payload.get('proof_next_qualifying_slot_at')}"
        )
    if payload.get('proof_recheck_after_at') != expected_status.get('proof_recheck_after_at'):
        failures.append(
            'proof_recheck_after_at verwacht '
            f"{expected_status.get('proof_recheck_after_at')}, kreeg {payload.get('proof_recheck_after_at')}"
        )
    if not payload.get('last_run_timeout_text'):
        failures.append('last_run_timeout_text verwacht niet-leeg runtime-headroomveld')
    if not payload.get('recent_run_duration_text'):
        failures.append('recent_run_duration_text verwacht niet-lege duurtrend')
    if payload.get('proof_freshness_text') != watchdog_payload.get('proof_freshness_text'):
        failures.append(
            'proof_freshness_text verwacht passthrough uit watchdog-json, kreeg '
            f"{payload.get('proof_freshness_text')} versus {watchdog_payload.get('proof_freshness_text')}"
        )
    if payload.get('proof_plan_text') != watchdog_payload.get('proof_plan_text'):
        failures.append(
            'proof_plan_text verwacht passthrough uit watchdog-json, kreeg '
            f"{payload.get('proof_plan_text')} versus {watchdog_payload.get('proof_plan_text')}"
        )
    if payload.get('summary_output_examples') != watchdog_payload.get('summary_output_examples'):
        failures.append(
            'summary_output_examples verwacht passthrough uit watchdog-json, kreeg '
            f"{payload.get('summary_output_examples')} versus {watchdog_payload.get('summary_output_examples')}"
        )
    if payload.get('consumer_requested_output_count_text') != 'consumer-output-aanvraag gevraagd=0, kanalen=0':
        failures.append(
            'consumer_requested_output_count_text verwacht consumer-output-aanvraag gevraagd=0, kanalen=0, kreeg '
            f"{payload.get('consumer_requested_output_count_text')}"
        )
    if payload.get('consumer_requested_outputs_status_text') != 'consumer-output-aanvraag leeg (geen artifact-output gevraagd)':
        failures.append(
            'consumer_requested_outputs_status_text verwacht consumer-output-aanvraag leeg (geen artifact-output gevraagd), kreeg '
            f"{payload.get('consumer_requested_outputs_status_text')}"
        )
    if payload.get('consumer_requested_outputs_status_kind') != 'none-requested':
        failures.append(
            'consumer_requested_outputs_status_kind verwacht none-requested, kreeg '
            f"{payload.get('consumer_requested_outputs_status_kind')}"
        )
    if payload.get('alert_text') != text_output:
        failures.append(
            'alert_text verwacht pariteit met tekstoutput, kreeg '
            f"{payload.get('alert_text')} versus {text_output}"
        )
    expected_text_output = case.get('expect_text_output')
    if expected_text_output is not None and text_output != expected_text_output:
        failures.append(
            f'tekstoutput verwacht {expected_text_output}, kreeg {text_output}'
        )
    for snippet in case.get('expect_text_substrings', []):
        if snippet not in text_output:
            failures.append(f"verwachte watchdog-alert-tekst ontbreekt: {snippet}")
        if snippet not in (payload.get('alert_text') or ''):
            failures.append(f"verwachte watchdog-alert-jsontekst ontbreekt: {snippet}")
    if not case.get('expect_no_reply', False):
        if payload.get('proof_freshness_text'):
            if payload['proof_freshness_text'] not in text_output:
                failures.append(
                    'watchdog-alert-tekst mist proof_freshness_text uit stdout-json: '
                    f"{payload.get('proof_freshness_text')}"
                )
            if payload['proof_freshness_text'] not in (payload.get('alert_text') or ''):
                failures.append(
                    'watchdog-alert alert_text mist proof_freshness_text uit stdout-json: '
                    f"{payload.get('proof_freshness_text')}"
                )
        if payload.get('proof_plan_text'):
            if payload['proof_plan_text'] not in text_output:
                failures.append(
                    'watchdog-alert-tekst mist proof_plan_text uit stdout-json: '
                    f"{payload.get('proof_plan_text')}"
                )
            if payload['proof_plan_text'] not in (payload.get('alert_text') or ''):
                failures.append(
                    'watchdog-alert alert_text mist proof_plan_text uit stdout-json: '
                    f"{payload.get('proof_plan_text')}"
                )

    if consumer_bundle and consumer_root is not None:
        board_json_path = consumer_root / 'ai-briefing-watchdog-alert.json'
        board_text_path = consumer_root / 'ai-briefing-watchdog-alert.txt'
        eventlog_path = consumer_root / 'ai-briefing-watchdog-alert.jsonl'
        if not board_json_path.exists():
            failures.append(f'consumer board-json ontbreekt: {board_json_path}')
        else:
            try:
                board_payload = json.loads(board_json_path.read_text(encoding='utf-8'))
            except json.JSONDecodeError as exc:
                failures.append(f'consumer board-json is geen geldige JSON: {exc}')
                board_payload = {}
            assert_runtime_metadata(board_payload, 'watchdog-alert consumer board-json', failures)
            if board_payload.get('no_reply') is not case.get('expect_no_reply', False):
                failures.append(
                    'consumer board-json no_reply verwacht '
                    f"{case.get('expect_no_reply', False)}, kreeg {board_payload.get('no_reply')}"
                )
            if board_payload.get('suppressed_before_proof_deadline') is not case.get('expect_suppressed_before_proof_deadline', False):
                failures.append(
                    'consumer board-json suppressed_before_proof_deadline verwacht '
                    f"{case.get('expect_suppressed_before_proof_deadline', False)}, kreeg {board_payload.get('suppressed_before_proof_deadline')}"
                )
            if board_payload.get('alert_text') != payload.get('alert_text'):
                failures.append(
                    'consumer board-json alert_text verwacht pariteit met stdout-json, kreeg '
                    f"{board_payload.get('alert_text')} versus {payload.get('alert_text')}"
                )
            if board_payload.get('last_run_timeout_text') != payload.get('last_run_timeout_text'):
                failures.append(
                    'consumer board-json last_run_timeout_text verwacht pariteit met stdout-json, kreeg '
                    f"{board_payload.get('last_run_timeout_text')} versus {payload.get('last_run_timeout_text')}"
                )
            if board_payload.get('recent_run_duration_text') != payload.get('recent_run_duration_text'):
                failures.append(
                    'consumer board-json recent_run_duration_text verwacht pariteit met stdout-json, kreeg '
                    f"{board_payload.get('recent_run_duration_text')} versus {payload.get('recent_run_duration_text')}"
                )
            if board_payload.get('proof_freshness_text') != payload.get('proof_freshness_text'):
                failures.append(
                    'consumer board-json proof_freshness_text verwacht pariteit met stdout-json, kreeg '
                    f"{board_payload.get('proof_freshness_text')} versus {payload.get('proof_freshness_text')}"
                )
            if board_payload.get('proof_plan_text') != payload.get('proof_plan_text'):
                failures.append(
                    'consumer board-json proof_plan_text verwacht pariteit met stdout-json, kreeg '
                    f"{board_payload.get('proof_plan_text')} versus {payload.get('proof_plan_text')}"
                )
            if board_payload.get('summary_output_examples') != payload.get('summary_output_examples'):
                failures.append(
                    'consumer board-json summary_output_examples verwacht pariteit met stdout-json, kreeg '
                    f"{board_payload.get('summary_output_examples')} versus {payload.get('summary_output_examples')}"
                )
            requested_outputs = board_payload.get('consumer_requested_outputs') or []
            requested_channels = [item.get('channel') for item in requested_outputs]
            if requested_channels != ['board-json', 'board-text', 'eventlog-jsonl']:
                failures.append(
                    'consumer board-json consumer_requested_outputs verwacht board-json/board-text/eventlog-jsonl, kreeg '
                    f'{requested_channels}'
                )
            expected_requested_outputs = [
                {
                    'channel': 'board-json',
                    'path': str(board_json_path),
                    'format': 'json',
                    'append': False,
                },
                {
                    'channel': 'board-text',
                    'path': str(board_text_path),
                    'format': 'text',
                    'append': False,
                },
                {
                    'channel': 'eventlog-jsonl',
                    'path': str(eventlog_path),
                    'format': 'jsonl',
                    'append': True,
                },
            ]
            if requested_outputs != expected_requested_outputs:
                failures.append(
                    'consumer board-json consumer_requested_outputs verwacht exacte board-suite metadata, kreeg '
                    f'{requested_outputs} versus {expected_requested_outputs}'
                )
            expected_requested_outputs_text = (
                f'consumer-artifacts: board-json: {board_json_path}; '
                f'board-text: {board_text_path}; '
                f'eventlog-jsonl: {eventlog_path}'
            )
            if board_payload.get('consumer_requested_output_count') != 3:
                failures.append(
                    'consumer board-json consumer_requested_output_count verwacht 3, kreeg '
                    f"{board_payload.get('consumer_requested_output_count')}"
                )
            if board_payload.get('consumer_requested_output_channel_count') != 3:
                failures.append(
                    'consumer board-json consumer_requested_output_channel_count verwacht 3, kreeg '
                    f"{board_payload.get('consumer_requested_output_channel_count')}"
                )
            if board_payload.get('consumer_requested_output_count_text') != 'consumer-output-aanvraag gevraagd=3, kanalen=3':
                failures.append(
                    'consumer board-json consumer_requested_output_count_text verwacht consumer-output-aanvraag gevraagd=3, kanalen=3, kreeg '
                    f"{board_payload.get('consumer_requested_output_count_text')}"
                )
            if board_payload.get('consumer_requested_output_channel_count_text') != 'consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3':
                failures.append(
                    'consumer board-json consumer_requested_output_channel_count_text verwacht consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3, kreeg '
                    f"{board_payload.get('consumer_requested_output_channel_count_text')}"
                )
            if board_payload.get('consumer_requested_output_channels_text') != 'consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl':
                failures.append(
                    'consumer board-json consumer_requested_output_channels_text verwacht consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                    f"{board_payload.get('consumer_requested_output_channels_text')}"
                )
            if board_payload.get('consumer_requested_outputs_status_kind') != 'requested':
                failures.append(
                    'consumer board-json consumer_requested_outputs_status_kind verwacht requested, kreeg '
                    f"{board_payload.get('consumer_requested_outputs_status_kind')}"
                )
            if board_payload.get('consumer_requested_outputs_status_text') != 'consumer-output-aanvraag vastgelegd voor 3 artifact(s)':
                failures.append(
                    'consumer board-json consumer_requested_outputs_status_text verwacht consumer-output-aanvraag vastgelegd voor 3 artifact(s), kreeg '
                    f"{board_payload.get('consumer_requested_outputs_status_text')}"
                )
            if board_payload.get('consumer_requested_outputs_text') != expected_requested_outputs_text:
                failures.append(
                    'consumer board-json consumer_requested_outputs_text verwacht '
                    f'{expected_requested_outputs_text}, kreeg {board_payload.get("consumer_requested_outputs_text")}'
                )
        if not board_text_path.exists():
            failures.append(f'consumer board-text ontbreekt: {board_text_path}')
        else:
            board_text_output = board_text_path.read_text(encoding='utf-8').strip()
            if board_text_output != text_output:
                failures.append(
                    f'consumer board-text verwacht {text_output}, kreeg {board_text_output}'
                )
        if not eventlog_path.exists():
            failures.append(f'consumer eventlog-jsonl ontbreekt: {eventlog_path}')
        else:
            eventlog_lines = [line for line in eventlog_path.read_text(encoding='utf-8').splitlines() if line.strip()]
            if not eventlog_lines:
                failures.append('consumer eventlog-jsonl is leeg')
            else:
                try:
                    eventlog_payload = json.loads(eventlog_lines[-1])
                except json.JSONDecodeError as exc:
                    failures.append(f'consumer eventlog-jsonl laatste regel is geen geldige JSON: {exc}')
                else:
                    assert_runtime_metadata(eventlog_payload, 'watchdog-alert consumer eventlog-jsonl', failures)
                    if eventlog_payload.get('alert_text') != payload.get('alert_text'):
                        failures.append(
                            'consumer eventlog-jsonl alert_text verwacht pariteit met stdout-json, kreeg '
                            f"{eventlog_payload.get('alert_text')} versus {payload.get('alert_text')}"
                        )
                    if eventlog_payload.get('last_run_timeout_text') != payload.get('last_run_timeout_text'):
                        failures.append(
                            'consumer eventlog-jsonl last_run_timeout_text verwacht pariteit met stdout-json, kreeg '
                            f"{eventlog_payload.get('last_run_timeout_text')} versus {payload.get('last_run_timeout_text')}"
                        )
                    if eventlog_payload.get('recent_run_duration_text') != payload.get('recent_run_duration_text'):
                        failures.append(
                            'consumer eventlog-jsonl recent_run_duration_text verwacht pariteit met stdout-json, kreeg '
                            f"{eventlog_payload.get('recent_run_duration_text')} versus {payload.get('recent_run_duration_text')}"
                        )
                    if eventlog_payload.get('proof_freshness_text') != payload.get('proof_freshness_text'):
                        failures.append(
                            'consumer eventlog-jsonl proof_freshness_text verwacht pariteit met stdout-json, kreeg '
                            f"{eventlog_payload.get('proof_freshness_text')} versus {payload.get('proof_freshness_text')}"
                        )
                    if eventlog_payload.get('proof_plan_text') != payload.get('proof_plan_text'):
                        failures.append(
                            'consumer eventlog-jsonl proof_plan_text verwacht pariteit met stdout-json, kreeg '
                            f"{eventlog_payload.get('proof_plan_text')} versus {payload.get('proof_plan_text')}"
                        )
                    if eventlog_payload.get('summary_output_examples') != payload.get('summary_output_examples'):
                        failures.append(
                            'consumer eventlog-jsonl summary_output_examples verwacht pariteit met stdout-json, kreeg '
                            f"{eventlog_payload.get('summary_output_examples')} versus {payload.get('summary_output_examples')}"
                        )
                    if eventlog_payload.get('no_reply') is not case.get('expect_no_reply', False):
                        failures.append(
                            'consumer eventlog-jsonl no_reply verwacht '
                            f"{case.get('expect_no_reply', False)}, kreeg {eventlog_payload.get('no_reply')}"
                        )
                    if eventlog_payload.get('suppressed_before_proof_deadline') is not case.get('expect_suppressed_before_proof_deadline', False):
                        failures.append(
                            'consumer eventlog-jsonl suppressed_before_proof_deadline verwacht '
                            f"{case.get('expect_suppressed_before_proof_deadline', False)}, kreeg {eventlog_payload.get('suppressed_before_proof_deadline')}"
                        )
                    if eventlog_payload.get('consumer_requested_output_count') != 3:
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_output_count verwacht 3, kreeg '
                            f"{eventlog_payload.get('consumer_requested_output_count')}"
                        )
                    if eventlog_payload.get('consumer_requested_output_channel_count') != 3:
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_output_channel_count verwacht 3, kreeg '
                            f"{eventlog_payload.get('consumer_requested_output_channel_count')}"
                        )
                    if eventlog_payload.get('consumer_requested_output_count_text') != 'consumer-output-aanvraag gevraagd=3, kanalen=3':
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_output_count_text verwacht consumer-output-aanvraag gevraagd=3, kanalen=3, kreeg '
                            f"{eventlog_payload.get('consumer_requested_output_count_text')}"
                        )
                    if eventlog_payload.get('consumer_requested_output_channel_count_text') != 'consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3':
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_output_channel_count_text verwacht consumer-output-aanvraag-kanalen gevraagd=3, kanalen=3, kreeg '
                            f"{eventlog_payload.get('consumer_requested_output_channel_count_text')}"
                        )
                    if eventlog_payload.get('consumer_requested_output_channels_text') != 'consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl':
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_output_channels_text verwacht consumer-output-aanvraag-kanalen: board-json, board-text, eventlog-jsonl, kreeg '
                            f"{eventlog_payload.get('consumer_requested_output_channels_text')}"
                        )
                    if eventlog_payload.get('consumer_requested_outputs_status_kind') != 'requested':
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_outputs_status_kind verwacht requested, kreeg '
                            f"{eventlog_payload.get('consumer_requested_outputs_status_kind')}"
                        )
                    if eventlog_payload.get('consumer_requested_outputs_status_text') != 'consumer-output-aanvraag vastgelegd voor 3 artifact(s)':
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_outputs_status_text verwacht consumer-output-aanvraag vastgelegd voor 3 artifact(s), kreeg '
                            f"{eventlog_payload.get('consumer_requested_outputs_status_text')}"
                        )
                    if eventlog_payload.get('consumer_requested_outputs_text') != expected_requested_outputs_text:
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_outputs_text verwacht '
                            f'{expected_requested_outputs_text}, kreeg {eventlog_payload.get("consumer_requested_outputs_text")}'
                        )
                    eventlog_requested_outputs = eventlog_payload.get('consumer_requested_outputs') or []
                    eventlog_requested_channels = [item.get('channel') for item in eventlog_requested_outputs]
                    if eventlog_requested_channels != ['board-json', 'board-text', 'eventlog-jsonl']:
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_outputs verwacht board-json/board-text/eventlog-jsonl, kreeg '
                            f'{eventlog_requested_channels}'
                        )
                    if eventlog_requested_outputs != expected_requested_outputs:
                        failures.append(
                            'consumer eventlog-jsonl consumer_requested_outputs verwacht exacte board-suite metadata, kreeg '
                            f'{eventlog_requested_outputs} versus {expected_requested_outputs}'
                        )

    return {
        'name': case['name'],
        'path': str(WATCHDOG_ALERT_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': text_output,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_watchdog_producer_case(case):
    mode = case.get('mode', 'proof-all')
    expected_status = run_status_json(case['reference_ms'])
    json_proc = subprocess.run(
        [
            'python3',
            str(WATCHDOG_PRODUCER_SCRIPT),
            mode,
            '--json',
            '--reference-ms',
            str(case['reference_ms']),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    quiet_proc = subprocess.run(
        [
            'python3',
            str(WATCHDOG_PRODUCER_SCRIPT),
            mode,
            '--quiet',
            '--reference-ms',
            str(case['reference_ms']),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    failures = []
    json_output = json_proc.stdout.strip() or json_proc.stderr.strip()
    quiet_output = quiet_proc.stdout.strip() or quiet_proc.stderr.strip()

    if json_proc.returncode != case['expect_exit_code']:
        failures.append(f"json-exitcode verwacht {case['expect_exit_code']}, kreeg {json_proc.returncode}")
        payload = {}
    elif not json_output:
        failures.append('geen JSON-output van ai-briefing-watchdog-producer.py')
        payload = {}
    else:
        try:
            payload = json.loads(json_output)
        except json.JSONDecodeError as exc:
            failures.append(f'ongeldige JSON van ai-briefing-watchdog-producer.py: {exc}')
            payload = {}

    if payload:
        assert_runtime_metadata(payload, 'watchdog-producer stdout-json', failures)

    if payload.get('mode') != mode:
        failures.append(f"mode verwacht {mode}, kreeg {payload.get('mode')}")
    if payload.get('item_count') != 1:
        failures.append(f"item_count verwacht 1, kreeg {payload.get('item_count')}")
    items = payload.get('items') or []
    child_payload = {}
    if len(items) != 1:
        failures.append(f"items verwacht 1 item, kreeg {len(items)}")
    else:
        child_payload = items[0].get('payload') or {}
        if items[0].get('returncode') != case['expect_exit_code']:
            failures.append(
                f"items[0].returncode verwacht {case['expect_exit_code']}, kreeg {items[0].get('returncode')}"
            )
        if child_payload:
            assert_runtime_metadata(child_payload, 'watchdog-producer child payload', failures)

    if quiet_proc.returncode != case['expect_exit_code']:
        failures.append(f"quiet-exitcode verwacht {case['expect_exit_code']}, kreeg {quiet_proc.returncode}")
    if not quiet_output:
        failures.append('geen quiet-output van ai-briefing-watchdog-producer.py')

    overall = payload.get('overall') or payload
    if overall.get('proof_recheck_schedule_kind') != 'ok':
        failures.append(
            'overall.proof_recheck_schedule_kind verwacht ok, kreeg '
            f"{overall.get('proof_recheck_schedule_kind')}"
        )
    if overall.get('proof_recheck_schedule_kind_text') != 'proof-recheck-cronstatus: ok':
        failures.append(
            'overall.proof_recheck_schedule_kind_text verwacht '
            f"proof-recheck-cronstatus: ok, kreeg {overall.get('proof_recheck_schedule_kind_text')}"
        )
    if overall.get('proof_recheck_schedule_job_name') != EXPECTED_PROOF_RECHECK_JOB_NAME:
        failures.append(
            'overall.proof_recheck_schedule_job_name verwacht '
            f"{EXPECTED_PROOF_RECHECK_JOB_NAME}, kreeg {overall.get('proof_recheck_schedule_job_name')}"
        )
    if overall.get('proof_recheck_schedule_expr') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR:
        failures.append(
            'overall.proof_recheck_schedule_expr verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPR}, kreeg {overall.get('proof_recheck_schedule_expr')}"
        )
    if overall.get('proof_recheck_schedule_tz') != EXPECTED_PROOF_RECHECK_SCHEDULE_TZ:
        failures.append(
            'overall.proof_recheck_schedule_tz verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_TZ}, kreeg {overall.get('proof_recheck_schedule_tz')}"
        )
    if overall.get('proof_recheck_schedule_found') is not True:
        failures.append(
            'overall.proof_recheck_schedule_found verwacht True, kreeg '
            f"{overall.get('proof_recheck_schedule_found')}"
        )
    if overall.get('proof_recheck_schedule_enabled') is not True:
        failures.append(
            'overall.proof_recheck_schedule_enabled verwacht True, kreeg '
            f"{overall.get('proof_recheck_schedule_enabled')}"
        )
    if overall.get('proof_recheck_schedule_expected_gap_minutes') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES:
        failures.append(
            'overall.proof_recheck_schedule_expected_gap_minutes verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES}, kreeg {overall.get('proof_recheck_schedule_expected_gap_minutes')}"
        )
    if overall.get('proof_recheck_schedule_same_day_after_target') is not True:
        failures.append(
            'overall.proof_recheck_schedule_same_day_after_target verwacht True, kreeg '
            f"{overall.get('proof_recheck_schedule_same_day_after_target')}"
        )
    if overall.get('proof_recheck_schedule_matches_grace') is not True:
        failures.append(
            'overall.proof_recheck_schedule_matches_grace verwacht True, kreeg '
            f"{overall.get('proof_recheck_schedule_matches_grace')}"
        )
    if overall.get('proof_recheck_schedule_delta_minutes') != EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES:
        failures.append(
            'overall.proof_recheck_schedule_delta_minutes verwacht '
            f"{EXPECTED_PROOF_RECHECK_SCHEDULE_EXPECTED_GAP_MINUTES}, kreeg {overall.get('proof_recheck_schedule_delta_minutes')}"
        )
    if overall.get('proof_config_hash') != expected_status.get('proof_config_hash'):
        failures.append(
            'overall.proof_config_hash verwacht '
            f"{expected_status.get('proof_config_hash')}, kreeg {overall.get('proof_config_hash')}"
        )
    if overall.get('proof_wait_until_at') != expected_status.get('proof_wait_until_at'):
        failures.append(
            'overall.proof_wait_until_at verwacht '
            f"{expected_status.get('proof_wait_until_at')}, kreeg {overall.get('proof_wait_until_at')}"
        )
    if overall.get('proof_next_qualifying_slot_at') != expected_status.get('proof_next_qualifying_slot_at'):
        failures.append(
            'overall.proof_next_qualifying_slot_at verwacht '
            f"{expected_status.get('proof_next_qualifying_slot_at')}, kreeg {overall.get('proof_next_qualifying_slot_at')}"
        )
    if overall.get('proof_recheck_after_at') != expected_status.get('proof_recheck_after_at'):
        failures.append(
            'overall.proof_recheck_after_at verwacht '
            f"{expected_status.get('proof_recheck_after_at')}, kreeg {overall.get('proof_recheck_after_at')}"
        )
    if overall.get('proof_target_due_at') != expected_status.get('proof_target_due_at'):
        failures.append(
            'overall.proof_target_due_at verwacht '
            f"{expected_status.get('proof_target_due_at')}, kreeg {overall.get('proof_target_due_at')}"
        )
    if overall.get('proof_target_due_at_if_next_slot_missed') != expected_status.get('proof_target_due_at_if_next_slot_missed'):
        failures.append(
            'overall.proof_target_due_at_if_next_slot_missed verwacht '
            f"{expected_status.get('proof_target_due_at_if_next_slot_missed')}, kreeg {overall.get('proof_target_due_at_if_next_slot_missed')}"
        )
    if overall.get('proof_schedule_slip_ms') != expected_status.get('proof_schedule_slip_ms'):
        failures.append(
            'overall.proof_schedule_slip_ms verwacht '
            f"{expected_status.get('proof_schedule_slip_ms')}, kreeg {overall.get('proof_schedule_slip_ms')}"
        )
    for expected_status_key in [
        'reference_context_text',
        'proof_config_identity_text',
        'last_run_config_relation',
        'last_run_config_relation_text',
        'proof_wait_until_text',
        'proof_wait_until_reason_text',
        'proof_next_action_text',
        'proof_next_action_window_text',
        'proof_recheck_commands_text',
        'proof_recheck_window_open',
        'proof_recheck_window_text',
        'proof_target_due_at_text',
        'proof_target_due_at_if_next_slot_missed_text',
        'proof_schedule_risk_text',
        'proof_countdown_text',
        'proof_target_check_gate',
        'proof_target_check_gate_text',
        'proof_target_run_slots_context_text',
    ]:
        if overall.get(expected_status_key) != expected_status.get(expected_status_key):
            failures.append(
                f'overall.{expected_status_key} verwacht {expected_status.get(expected_status_key)}, kreeg '
                f"{overall.get(expected_status_key)}"
            )
    for child_payload_key in [
        'proof_waiting_for_next_scheduled_run',
        'proof_runs_remaining',
        'proof_target_met',
        'proof_freshness_text',
        'proof_plan_text',
        'last_run_timeout_text',
        'recent_run_duration_text',
        'summary_output_examples',
        'consumer_requested_outputs',
        'consumer_requested_output_count',
        'consumer_requested_output_channel_count',
        'consumer_requested_output_count_text',
        'consumer_requested_output_channel_count_text',
        'consumer_requested_output_channels_text',
        'consumer_requested_outputs_status_kind',
        'consumer_requested_outputs_status_text',
        'consumer_requested_outputs_text',
    ]:
        if overall.get(child_payload_key) != child_payload.get(child_payload_key):
            failures.append(
                f'overall.{child_payload_key} verwacht passthrough {child_payload.get(child_payload_key)}, kreeg '
                f"{overall.get(child_payload_key)}"
            )
    if overall.get('proof_state') != case['expect_proof_state']:
        failures.append(
            f"overall.proof_state verwacht {case['expect_proof_state']}, kreeg {overall.get('proof_state')}"
        )
    if overall.get('proof_next_action_kind') != case['expect_proof_next_action_kind']:
        failures.append(
            'overall.proof_next_action_kind verwacht '
            f"{case['expect_proof_next_action_kind']}, kreeg {overall.get('proof_next_action_kind')}"
        )
    if payload.get('proof_recheck_schedule_kind') != overall.get('proof_recheck_schedule_kind'):
        failures.append(
            'top-level proof_recheck_schedule_kind verwacht alias-pariteit met overall, kreeg '
            f"{payload.get('proof_recheck_schedule_kind')} versus {overall.get('proof_recheck_schedule_kind')}"
        )
    if payload.get('proof_next_action_kind') != overall.get('proof_next_action_kind'):
        failures.append(
            'top-level proof_next_action_kind verwacht alias-pariteit met overall, kreeg '
            f"{payload.get('proof_next_action_kind')} versus {overall.get('proof_next_action_kind')}"
        )
    for alias_key in [
        'reference_context_text',
        'proof_state',
        'proof_state_text',
        'proof_blocker_kind',
        'proof_blocker_text',
        'proof_progress_text',
        'proof_runs_remaining',
        'proof_target_met',
        'proof_waiting_for_next_scheduled_run',
        'proof_config_hash',
        'proof_config_identity_text',
        'last_run_config_relation',
        'last_run_config_relation_text',
        'proof_next_action_text',
        'proof_next_action_window_text',
        'proof_recheck_commands_text',
        'proof_wait_until_at',
        'proof_wait_until_text',
        'proof_wait_until_reason_text',
        'proof_next_qualifying_slot_at',
        'proof_recheck_window_open',
        'proof_recheck_window_text',
        'proof_recheck_after_at',
        'proof_recheck_after_text',
        'proof_recheck_after_text_compact',
        'proof_target_due_at',
        'proof_target_due_at_text',
        'proof_target_due_at_if_next_slot_missed',
        'proof_target_due_at_if_next_slot_missed_text',
        'proof_schedule_slip_ms',
        'proof_schedule_risk_text',
        'proof_countdown_text',
        'proof_target_check_gate',
        'proof_target_check_gate_text',
        'proof_target_run_slots_context_text',
        'proof_target_run_slots_text',
        'proof_freshness_text',
        'proof_plan_text',
        'last_run_timeout_text',
        'recent_run_duration_text',
        'summary_output_examples',
        'consumer_requested_outputs',
        'consumer_requested_output_count',
        'consumer_requested_output_channel_count',
        'consumer_requested_output_count_text',
        'consumer_requested_output_channel_count_text',
        'consumer_requested_output_channels_text',
        'consumer_requested_outputs_status_kind',
        'consumer_requested_outputs_status_text',
        'consumer_requested_outputs_text',
        'proof_recheck_schedule_kind_text',
        'proof_recheck_schedule_job_name',
        'proof_recheck_schedule_expr',
        'proof_recheck_schedule_tz',
        'proof_recheck_schedule_text',
        'proof_recheck_schedule_found',
        'proof_recheck_schedule_enabled',
        'proof_recheck_schedule_expected_gap_minutes',
        'proof_recheck_schedule_same_day_after_target',
        'proof_recheck_schedule_matches_grace',
        'proof_recheck_schedule_delta_minutes',
    ]:
        if payload.get(alias_key) != overall.get(alias_key):
            failures.append(
                f'top-level {alias_key} verwacht alias-pariteit met overall, kreeg '
                f"{payload.get(alias_key)} versus {overall.get(alias_key)}"
            )

    combined_text = ' || '.join(
        bit for bit in [
            payload.get('proof_recheck_schedule_text'),
            payload.get('proof_recheck_schedule_kind_text'),
            payload.get('proof_plan_text'),
            overall.get('proof_recheck_schedule_text'),
            overall.get('proof_recheck_schedule_kind_text'),
            overall.get('proof_plan_text'),
            overall.get('proof_next_action_window_text'),
            overall.get('proof_next_action_text'),
            quiet_output,
        ] if bit
    )
    for snippet in case.get('expect_text_substrings', []):
        if snippet not in combined_text:
            failures.append(f"verwachte watchdog-producer-tekst ontbreekt: {snippet}")

    return {
        'name': case['name'],
        'path': str(WATCHDOG_PRODUCER_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': combined_text,
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_proof_recheck_consumer_format_passthrough_case():
    failures = []
    audit_bits: list[str] = []

    with tempfile.TemporaryDirectory(prefix='ai-briefing-proof-recheck-format-') as temp_dir:
        text_artifact = Path(temp_dir) / 'proof-recheck-text.txt'
        json_stdout_proc = subprocess.run(
            [
                'python3', str(PROOF_RECHECK_SCRIPT), '--json',
                '--reference-ms', '1776495480000',
                '--consumer-out', str(text_artifact),
                '--consumer-format', 'text',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if json_stdout_proc.returncode != 2:
            failures.append(f'json-stdout proof-recheck exitcode verwacht 2, kreeg {json_stdout_proc.returncode}')

        json_payload = {}
        json_stdout = json_stdout_proc.stdout.strip() or json_stdout_proc.stderr.strip()
        if not json_stdout:
            failures.append('json-stdout proof-recheck gaf geen output')
        else:
            try:
                json_payload = json.loads(json_stdout)
                audit_bits.append(json.dumps(json_payload, ensure_ascii=False))
            except json.JSONDecodeError as exc:
                failures.append(f'json-stdout proof-recheck hoort JSON te blijven, kreeg parsefout: {exc}')

        if json_payload and (json_payload.get('consumer_outputs') or [{}])[0].get('format') != 'text':
            failures.append(
                'json-stdout proof-recheck consumer_outputs[0].format verwacht text, kreeg '
                f"{(json_payload.get('consumer_outputs') or [{}])[0].get('format')}"
            )
        if json_payload and (json_payload.get('consumer_requested_outputs') or [{}])[0].get('format') != 'text':
            failures.append(
                'json-stdout proof-recheck consumer_requested_outputs[0].format verwacht text, kreeg '
                f"{(json_payload.get('consumer_requested_outputs') or [{}])[0].get('format')}"
            )
        if not text_artifact.exists():
            failures.append(f'tekstartifact ontbreekt: {text_artifact}')
        else:
            artifact_text = text_artifact.read_text(encoding='utf-8')
            audit_bits.append(artifact_text.strip())
            if not artifact_text.startswith('AI-briefing proof-recheck: '):
                failures.append('tekstartifact hoort plain-text te blijven wanneer --consumer-format text is gebruikt')
            try:
                json.loads(artifact_text)
                failures.append('tekstartifact hoort geen JSON te zijn wanneer --consumer-format text is gebruikt')
            except json.JSONDecodeError:
                pass

        json_artifact = Path(temp_dir) / 'proof-recheck-json.json'
        text_stdout_proc = subprocess.run(
            [
                'python3', str(PROOF_RECHECK_SCRIPT),
                '--reference-ms', '1776495480000',
                '--consumer-out', str(json_artifact),
                '--consumer-format', 'json',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if text_stdout_proc.returncode != 2:
            failures.append(f'text-stdout proof-recheck exitcode verwacht 2, kreeg {text_stdout_proc.returncode}')

        plain_stdout = text_stdout_proc.stdout.strip() or text_stdout_proc.stderr.strip()
        if not plain_stdout:
            failures.append('text-stdout proof-recheck gaf geen output')
        else:
            audit_bits.append(plain_stdout)
            if not plain_stdout.startswith('AI-briefing proof-recheck: '):
                failures.append('stdout hoort plain-text te blijven wanneer alleen --consumer-format json is gebruikt')
            try:
                json.loads(plain_stdout)
                failures.append('stdout hoort geen JSON te worden wanneer alleen --consumer-format json is gebruikt')
            except json.JSONDecodeError:
                pass

        if not json_artifact.exists():
            failures.append(f'json-artifact ontbreekt: {json_artifact}')
        else:
            try:
                artifact_payload = json.loads(json_artifact.read_text(encoding='utf-8'))
                audit_bits.append(json.dumps(artifact_payload, ensure_ascii=False))
                if (artifact_payload.get('consumer_outputs') or [{}])[0].get('format') != 'json':
                    failures.append(
                        'json-artifact consumer_outputs[0].format verwacht json, kreeg '
                        f"{(artifact_payload.get('consumer_outputs') or [{}])[0].get('format')}"
                    )
                if (artifact_payload.get('consumer_requested_outputs') or [{}])[0].get('format') != 'json':
                    failures.append(
                        'json-artifact consumer_requested_outputs[0].format verwacht json, kreeg '
                        f"{(artifact_payload.get('consumer_requested_outputs') or [{}])[0].get('format')}"
                    )
            except json.JSONDecodeError as exc:
                failures.append(f'json-artifact hoort parsebare JSON te zijn, kreeg parsefout: {exc}')

    return {
        'name': 'proof-recheck-consumer-format-keeps-stdout-format',
        'path': str(PROOF_RECHECK_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': ' || '.join(bit for bit in audit_bits if bit),
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_watchdog_consumer_format_passthrough_case():
    failures = []
    audit_bits: list[str] = []

    with tempfile.TemporaryDirectory(prefix='ai-briefing-watchdog-format-') as temp_dir:
        text_artifact = Path(temp_dir) / 'watchdog-text.txt'
        json_stdout_proc = subprocess.run(
            [
                'python3', str(WATCHDOG_SCRIPT), '--json',
                '--require-qualified-runs', '3',
                '--reference-ms', str(REFERENCE_MS_BEFORE_SLOT_TOMORROW),
                '--consumer-out', str(text_artifact),
                '--consumer-format', 'text',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if json_stdout_proc.returncode != 2:
            failures.append(f'json-stdout watchdog exitcode verwacht 2, kreeg {json_stdout_proc.returncode}')

        json_payload = {}
        json_stdout = json_stdout_proc.stdout.strip() or json_stdout_proc.stderr.strip()
        if not json_stdout:
            failures.append('json-stdout watchdog gaf geen output')
        else:
            try:
                json_payload = json.loads(json_stdout)
                audit_bits.append(json.dumps(json_payload, ensure_ascii=False))
            except json.JSONDecodeError as exc:
                failures.append(f'json-stdout watchdog hoort JSON te blijven, kreeg parsefout: {exc}')

        if json_payload and json_payload.get('proof_waiting_for_next_scheduled_run') is not True:
            failures.append(
                'json-stdout watchdog verwacht proof_waiting_for_next_scheduled_run=True voor deze wachtfase'
            )
        if not text_artifact.exists():
            failures.append(f'tekstartifact ontbreekt: {text_artifact}')
        else:
            artifact_text = text_artifact.read_text(encoding='utf-8')
            audit_bits.append(artifact_text.strip())
            if not artifact_text.startswith('ai briefing watchdog: attention - '):
                failures.append('tekstartifact hoort plain-text te blijven wanneer --consumer-format text is gebruikt')
            try:
                json.loads(artifact_text)
                failures.append('tekstartifact hoort geen JSON te zijn wanneer --consumer-format text is gebruikt')
            except json.JSONDecodeError:
                pass

        json_artifact = Path(temp_dir) / 'watchdog-json.json'
        text_stdout_proc = subprocess.run(
            [
                'python3', str(WATCHDOG_SCRIPT),
                '--require-qualified-runs', '3',
                '--reference-ms', str(REFERENCE_MS_BEFORE_SLOT_TOMORROW),
                '--consumer-out', str(json_artifact),
                '--consumer-format', 'json',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if text_stdout_proc.returncode != 2:
            failures.append(f'text-stdout watchdog exitcode verwacht 2, kreeg {text_stdout_proc.returncode}')

        plain_stdout = text_stdout_proc.stdout.strip() or text_stdout_proc.stderr.strip()
        if not plain_stdout:
            failures.append('text-stdout watchdog gaf geen output')
        else:
            audit_bits.append(plain_stdout)
            if not plain_stdout.startswith('ai briefing watchdog: attention - '):
                failures.append('stdout hoort plain-text te blijven wanneer alleen --consumer-format json is gebruikt')
            try:
                json.loads(plain_stdout)
                failures.append('stdout hoort geen JSON te worden wanneer alleen --consumer-format json is gebruikt')
            except json.JSONDecodeError:
                pass

        if not json_artifact.exists():
            failures.append(f'json-artifact ontbreekt: {json_artifact}')
        else:
            try:
                artifact_payload = json.loads(json_artifact.read_text(encoding='utf-8'))
                audit_bits.append(json.dumps(artifact_payload, ensure_ascii=False))
                if artifact_payload.get('proof_waiting_for_next_scheduled_run') is not True:
                    failures.append(
                        'json-artifact verwacht proof_waiting_for_next_scheduled_run=True voor deze wachtfase'
                    )
                if artifact_payload.get('proof_recheck_schedule_kind') != 'ok':
                    failures.append(
                        'json-artifact proof_recheck_schedule_kind verwacht ok, kreeg '
                        f"{artifact_payload.get('proof_recheck_schedule_kind')}"
                    )
            except json.JSONDecodeError as exc:
                failures.append(f'json-artifact hoort parsebare JSON te zijn, kreeg parsefout: {exc}')

    return {
        'name': 'watchdog-consumer-format-keeps-stdout-format',
        'path': str(WATCHDOG_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': ' || '.join(bit for bit in audit_bits if bit),
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_watchdog_alert_consumer_format_passthrough_case():
    failures = []
    audit_bits: list[str] = []

    with tempfile.TemporaryDirectory(prefix='ai-briefing-watchdog-alert-format-') as temp_dir:
        text_artifact = Path(temp_dir) / 'watchdog-alert-text.txt'
        json_stdout_proc = subprocess.run(
            [
                'python3', str(WATCHDOG_ALERT_SCRIPT), '--mode', 'proof-target-check', '--json',
                '--reference-ms', str(REFERENCE_MS_BEFORE_SLOT_TOMORROW),
                '--consumer-out', str(text_artifact),
                '--consumer-format', 'text',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if json_stdout_proc.returncode != 0:
            failures.append(f'json-stdout watchdog-alert exitcode verwacht 0, kreeg {json_stdout_proc.returncode}')

        json_payload = {}
        json_stdout = json_stdout_proc.stdout.strip() or json_stdout_proc.stderr.strip()
        if not json_stdout:
            failures.append('json-stdout watchdog-alert gaf geen output')
        else:
            try:
                json_payload = json.loads(json_stdout)
                audit_bits.append(json.dumps(json_payload, ensure_ascii=False))
            except json.JSONDecodeError as exc:
                failures.append(f'json-stdout watchdog-alert hoort JSON te blijven, kreeg parsefout: {exc}')

        if json_payload and (json_payload.get('consumer_requested_outputs') or [{}])[0].get('format') != 'text':
            failures.append(
                'json-stdout watchdog-alert consumer_requested_outputs[0].format verwacht text, kreeg '
                f"{(json_payload.get('consumer_requested_outputs') or [{}])[0].get('format')}"
            )
        if not text_artifact.exists():
            failures.append(f'tekstartifact ontbreekt: {text_artifact}')
        else:
            artifact_text = text_artifact.read_text(encoding='utf-8').strip()
            audit_bits.append(artifact_text)
            if artifact_text != 'NO_REPLY':
                failures.append(f'tekstartifact verwacht NO_REPLY, kreeg {artifact_text}')
            try:
                json.loads(artifact_text)
                failures.append('tekstartifact hoort geen JSON te zijn wanneer --consumer-format text is gebruikt')
            except json.JSONDecodeError:
                pass

        json_artifact = Path(temp_dir) / 'watchdog-alert-json.json'
        text_stdout_proc = subprocess.run(
            [
                'python3', str(WATCHDOG_ALERT_SCRIPT), '--mode', 'proof-target-check',
                '--reference-ms', str(REFERENCE_MS_BEFORE_SLOT_TOMORROW),
                '--consumer-out', str(json_artifact),
                '--consumer-format', 'json',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if text_stdout_proc.returncode != 0:
            failures.append(f'text-stdout watchdog-alert exitcode verwacht 0, kreeg {text_stdout_proc.returncode}')

        plain_stdout = text_stdout_proc.stdout.strip() or text_stdout_proc.stderr.strip()
        if not plain_stdout:
            failures.append('text-stdout watchdog-alert gaf geen output')
        else:
            audit_bits.append(plain_stdout)
            if plain_stdout != 'NO_REPLY':
                failures.append(f'stdout verwacht NO_REPLY, kreeg {plain_stdout}')
            try:
                json.loads(plain_stdout)
                failures.append('stdout hoort geen JSON te worden wanneer alleen --consumer-format json is gebruikt')
            except json.JSONDecodeError:
                pass

        if not json_artifact.exists():
            failures.append(f'json-artifact ontbreekt: {json_artifact}')
        else:
            try:
                artifact_payload = json.loads(json_artifact.read_text(encoding='utf-8'))
                audit_bits.append(json.dumps(artifact_payload, ensure_ascii=False))
                if (artifact_payload.get('consumer_requested_outputs') or [{}])[0].get('format') != 'json':
                    failures.append(
                        'json-artifact consumer_requested_outputs[0].format verwacht json, kreeg '
                        f"{(artifact_payload.get('consumer_requested_outputs') or [{}])[0].get('format')}"
                    )
                if artifact_payload.get('alert_text') != 'NO_REPLY':
                    failures.append(
                        'json-artifact alert_text verwacht NO_REPLY, kreeg '
                        f"{artifact_payload.get('alert_text')}"
                    )
                if artifact_payload.get('no_reply') is not True:
                    failures.append(
                        f"json-artifact no_reply verwacht True, kreeg {artifact_payload.get('no_reply')}"
                    )
            except json.JSONDecodeError as exc:
                failures.append(f'json-artifact hoort parsebare JSON te zijn, kreeg parsefout: {exc}')

    return {
        'name': 'watchdog-alert-consumer-format-keeps-stdout-format',
        'path': str(WATCHDOG_ALERT_SCRIPT),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': ' || '.join(bit for bit in audit_bits if bit),
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def evaluate_list_cases_output_case():
    failures = []
    audit_bits: list[str] = []
    filtered_case_names = [
        'watchdog-alert-consumer-format-passthrough',
        'watchdog-consumer-format-passthrough',
    ]
    unknown_case_name = 'definitely-not-a-real-regression-case'
    suggested_unknown_case_name = 'regression-check-list-case-output'
    expected_suggested_case_name = 'regression-check-list-cases-output'
    sorted_filtered_case_names = sorted(filtered_case_names)

    def assert_runtime_metadata(payload: dict, label: str) -> None:
        generated_at = payload.get('generated_at')
        started_at = payload.get('started_at')
        generated_at_text = payload.get('generated_at_text')
        started_at_text = payload.get('started_at_text')
        duration_ms = payload.get('duration_ms')
        duration_seconds = payload.get('duration_seconds')
        duration_text = payload.get('duration_text')

        if not isinstance(generated_at, str) or not generated_at:
            failures.append(f'{label} generated_at hoort een niet-lege ISO-tijdstring te zijn')
        else:
            try:
                datetime.fromisoformat(generated_at)
            except ValueError as exc:
                failures.append(f'{label} generated_at hoort parsebare ISO-tijd te zijn, kreeg {exc}')

        if not isinstance(started_at, str) or not started_at:
            failures.append(f'{label} started_at hoort een niet-lege ISO-tijdstring te zijn')
        else:
            try:
                started_dt = datetime.fromisoformat(started_at)
                finished_dt = datetime.fromisoformat(generated_at) if isinstance(generated_at, str) and generated_at else None
                if finished_dt is not None and started_dt > finished_dt:
                    failures.append(f'{label} started_at hoort niet ná generated_at te liggen')
            except ValueError as exc:
                failures.append(f'{label} started_at hoort parsebare ISO-tijd te zijn, kreeg {exc}')

        if not isinstance(generated_at_text, str) or not generated_at_text.strip():
            failures.append(f'{label} generated_at_text hoort een niet-lege teksttimestamp te zijn')
        if not isinstance(started_at_text, str) or not started_at_text.strip():
            failures.append(f'{label} started_at_text hoort een niet-lege teksttimestamp te zijn')
        if not isinstance(duration_ms, int) or duration_ms < 0:
            failures.append(f'{label} duration_ms hoort een niet-negatieve int te zijn')
        if not isinstance(duration_seconds, (int, float)) or duration_seconds < 0:
            failures.append(f'{label} duration_seconds hoort een niet-negatief getal te zijn')
        elif isinstance(duration_ms, int):
            expected_duration_seconds = round(duration_ms / 1000, 3)
            if abs(float(duration_seconds) - expected_duration_seconds) > 0.0005:
                failures.append(
                    f'{label} duration_seconds hoort duration_ms/1000 af te ronden op 3 decimalen'
                )
        if not isinstance(duration_text, str) or not duration_text.endswith('s'):
            failures.append(f'{label} duration_text hoort een secondenlabel te zijn')
        elif isinstance(duration_seconds, (int, float)):
            expected_duration_text = f'{float(duration_seconds):.3f}s'
            if duration_text != expected_duration_text:
                failures.append(
                    f'{label} duration_text hoort exact {expected_duration_text} te spiegelen, kreeg {duration_text}'
                )

    plain_proc = subprocess.run(
        ['python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--list-cases'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if plain_proc.returncode != 0:
        failures.append(f'plain --list-cases exitcode verwacht 0, kreeg {plain_proc.returncode}')

    plain_lines = [line.strip() for line in plain_proc.stdout.splitlines() if line.strip()]
    audit_bits.append('plain=' + ', '.join(plain_lines[:8]))
    if not plain_lines:
        failures.append('plain --list-cases gaf geen casenamen terug')
    if plain_lines != sorted(plain_lines):
        failures.append('plain --list-cases hoort alfabetisch gesorteerd te zijn')
    if len(plain_lines) != len(set(plain_lines)):
        failures.append('plain --list-cases hoort geen dubbele casenamen te bevatten')
    for expected_case_name in filtered_case_names:
        if expected_case_name not in plain_lines:
            failures.append(f'plain --list-cases mist verwachte casenaam {expected_case_name}')

    json_proc = subprocess.run(
        ['python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json', '--list-cases'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if json_proc.returncode != 0:
        failures.append(f'json --list-cases exitcode verwacht 0, kreeg {json_proc.returncode}')

    json_payload = {}
    json_stdout = json_proc.stdout.strip() or json_proc.stderr.strip()
    if not json_stdout:
        failures.append('json --list-cases gaf geen output')
    else:
        try:
            json_payload = json.loads(json_stdout)
            audit_bits.append('json=' + json.dumps(json_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(f'json --list-cases hoort parsebare JSON te geven, kreeg parsefout: {exc}')

    if json_payload:
        assert_runtime_metadata(json_payload, 'json --list-cases')
        listed_cases = json_payload.get('cases')
        if not isinstance(listed_cases, list):
            failures.append(f'json --list-cases cases verwacht lijst, kreeg {type(listed_cases).__name__}')
        else:
            if listed_cases != plain_lines:
                failures.append('json --list-cases cases hoort exact gelijk te zijn aan plain --list-cases')
            if json_payload.get('case_count') != len(listed_cases):
                failures.append(
                    'json --list-cases case_count verwacht '
                    f"{len(listed_cases)}, kreeg {json_payload.get('case_count')}"
                )
            if json_payload.get('selected_case_count') != len(listed_cases):
                failures.append(
                    'json --list-cases selected_case_count verwacht '
                    f"{len(listed_cases)}, kreeg {json_payload.get('selected_case_count')}"
                )
        if json_payload.get('ok') is not True:
            failures.append(f"json --list-cases ok verwacht True, kreeg {json_payload.get('ok')}")
        if json_payload.get('requested_case_names') != []:
            failures.append('json --list-cases requested_case_names hoort leeg te zijn zonder gerichte selectie')
        if json_payload.get('requested_case_count') != 0:
            failures.append(
                'json --list-cases requested_case_count verwacht 0, kreeg '
                f"{json_payload.get('requested_case_count')}"
            )
        if json_payload.get('selected_case_names') != plain_lines:
            failures.append('json --list-cases selected_case_names hoort de uitgegeven casenamen te weerspiegelen')
        if json_payload.get('available_case_names') != plain_lines:
            failures.append(
                'json --list-cases available_case_names hoort ook bij succes de volledige alfabetische caselijst mee te geven'
            )
        if json_payload.get('available_case_count') != len(plain_lines):
            failures.append(
                'json --list-cases available_case_count hoort ook bij succes exact de volledige caseteller te geven'
            )

    filtered_plain_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--list-cases',
            '--case', filtered_case_names[0], '--case', filtered_case_names[1],
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if filtered_plain_proc.returncode != 0:
        failures.append(
            'plain --list-cases met --case exitcode verwacht 0, kreeg '
            f'{filtered_plain_proc.returncode}'
        )
    filtered_plain_lines = [line.strip() for line in filtered_plain_proc.stdout.splitlines() if line.strip()]
    audit_bits.append('filtered-plain=' + ', '.join(filtered_plain_lines))
    if filtered_plain_lines != sorted_filtered_case_names:
        failures.append(
            'plain --list-cases met --case hoort alleen de gevraagde casenamen alfabetisch terug te geven'
        )

    filtered_json_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json', '--list-cases',
            '--case', filtered_case_names[0], '--case', filtered_case_names[1],
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if filtered_json_proc.returncode != 0:
        failures.append(
            'json --list-cases met --case exitcode verwacht 0, kreeg '
            f'{filtered_json_proc.returncode}'
        )

    filtered_json_payload = {}
    filtered_json_stdout = filtered_json_proc.stdout.strip() or filtered_json_proc.stderr.strip()
    if not filtered_json_stdout:
        failures.append('json --list-cases met --case gaf geen output')
    else:
        try:
            filtered_json_payload = json.loads(filtered_json_stdout)
            audit_bits.append('filtered-json=' + json.dumps(filtered_json_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(
                'json --list-cases met --case hoort parsebare JSON te geven, kreeg parsefout: '
                f'{exc}'
            )

    if filtered_json_payload:
        assert_runtime_metadata(filtered_json_payload, 'json --list-cases met --case')
        filtered_listed_cases = filtered_json_payload.get('cases')
        if filtered_listed_cases != sorted_filtered_case_names:
            failures.append(
                'json --list-cases met --case cases hoort exact de gevraagde alfabetische subset te geven'
            )
        if filtered_json_payload.get('requested_case_names') != filtered_case_names:
            failures.append(
                'json --list-cases met --case requested_case_names hoort de opgegeven invoervolgorde te spiegelen'
            )
        if filtered_json_payload.get('requested_case_count') != len(filtered_case_names):
            failures.append(
                'json --list-cases met --case requested_case_count verwacht '
                f"{len(filtered_case_names)}, kreeg {filtered_json_payload.get('requested_case_count')}"
            )
        if filtered_json_payload.get('selected_case_names') != sorted_filtered_case_names:
            failures.append(
                'json --list-cases met --case selected_case_names hoort exact de gevraagde subset te spiegelen'
            )
        if filtered_json_payload.get('selected_case_count') != len(sorted_filtered_case_names):
            failures.append(
                'json --list-cases met --case selected_case_count verwacht '
                f"{len(sorted_filtered_case_names)}, kreeg {filtered_json_payload.get('selected_case_count')}"
            )
        if filtered_json_payload.get('case_count') != len(sorted_filtered_case_names):
            failures.append(
                'json --list-cases met --case case_count verwacht '
                f"{len(sorted_filtered_case_names)}, kreeg {filtered_json_payload.get('case_count')}"
            )
        if filtered_json_payload.get('ok') is not True:
            failures.append(
                f"json --list-cases met --case ok verwacht True, kreeg {filtered_json_payload.get('ok')}"
            )
        if filtered_json_payload.get('available_case_names') != plain_lines:
            failures.append(
                'json --list-cases met --case available_case_names hoort ook bij succes de volledige alfabetische caselijst mee te geven'
            )
        if filtered_json_payload.get('available_case_count') != len(plain_lines):
            failures.append(
                'json --list-cases met --case available_case_count hoort ook bij succes exact de volledige caseteller te geven'
            )

    duplicate_filtered_case_names = [
        filtered_case_names[0],
        filtered_case_names[1],
        filtered_case_names[0],
    ]
    duplicate_expected_case_names = sorted_filtered_case_names

    duplicate_plain_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--list-cases',
            '--case', duplicate_filtered_case_names[0],
            '--case', duplicate_filtered_case_names[1],
            '--case', duplicate_filtered_case_names[2],
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if duplicate_plain_proc.returncode != 0:
        failures.append(
            'plain --list-cases met dubbele --case exitcode verwacht 0, kreeg '
            f'{duplicate_plain_proc.returncode}'
        )
    duplicate_plain_lines = [line.strip() for line in duplicate_plain_proc.stdout.splitlines() if line.strip()]
    audit_bits.append('duplicate-filtered-plain=' + ', '.join(duplicate_plain_lines))
    if duplicate_plain_lines != duplicate_expected_case_names:
        failures.append(
            'plain --list-cases met dubbele --case hoort dubbele invoer te dedupliceren'
        )

    duplicate_json_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json', '--list-cases',
            '--case', duplicate_filtered_case_names[0],
            '--case', duplicate_filtered_case_names[1],
            '--case', duplicate_filtered_case_names[2],
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if duplicate_json_proc.returncode != 0:
        failures.append(
            'json --list-cases met dubbele --case exitcode verwacht 0, kreeg '
            f'{duplicate_json_proc.returncode}'
        )

    duplicate_json_payload = {}
    duplicate_json_stdout = duplicate_json_proc.stdout.strip() or duplicate_json_proc.stderr.strip()
    if not duplicate_json_stdout:
        failures.append('json --list-cases met dubbele --case gaf geen output')
    else:
        try:
            duplicate_json_payload = json.loads(duplicate_json_stdout)
            audit_bits.append('duplicate-filtered-json=' + json.dumps(duplicate_json_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(
                'json --list-cases met dubbele --case hoort parsebare JSON te geven, kreeg parsefout: '
                f'{exc}'
            )

    if duplicate_json_payload:
        assert_runtime_metadata(duplicate_json_payload, 'json --list-cases met dubbele --case')
        if duplicate_json_payload.get('cases') != duplicate_expected_case_names:
            failures.append(
                'json --list-cases met dubbele --case cases hoort dubbele invoer te dedupliceren'
            )
        if duplicate_json_payload.get('requested_case_names') != duplicate_expected_case_names:
            failures.append(
                'json --list-cases met dubbele --case requested_case_names hoort dubbele invoer te dedupliceren'
            )
        if duplicate_json_payload.get('requested_case_count') != len(duplicate_expected_case_names):
            failures.append(
                'json --list-cases met dubbele --case requested_case_count verwacht '
                f"{len(duplicate_expected_case_names)}, kreeg {duplicate_json_payload.get('requested_case_count')}"
            )
        if duplicate_json_payload.get('selected_case_names') != duplicate_expected_case_names:
            failures.append(
                'json --list-cases met dubbele --case selected_case_names hoort dubbele invoer te dedupliceren'
            )
        if duplicate_json_payload.get('selected_case_count') != len(duplicate_expected_case_names):
            failures.append(
                'json --list-cases met dubbele --case selected_case_count verwacht '
                f"{len(duplicate_expected_case_names)}, kreeg {duplicate_json_payload.get('selected_case_count')}"
            )
        if duplicate_json_payload.get('case_count') != len(duplicate_expected_case_names):
            failures.append(
                'json --list-cases met dubbele --case case_count verwacht '
                f"{len(duplicate_expected_case_names)}, kreeg {duplicate_json_payload.get('case_count')}"
            )
        if duplicate_json_payload.get('ok') is not True:
            failures.append(
                f"json --list-cases met dubbele --case ok verwacht True, kreeg {duplicate_json_payload.get('ok')}"
            )
        if duplicate_json_payload.get('available_case_names') != plain_lines:
            failures.append(
                'json --list-cases met dubbele --case available_case_names hoort ook bij succes de volledige alfabetische caselijst mee te geven'
            )
        if duplicate_json_payload.get('available_case_count') != len(plain_lines):
            failures.append(
                'json --list-cases met dubbele --case available_case_count hoort ook bij succes exact de volledige caseteller te geven'
            )

    duplicate_run_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json',
            '--case', duplicate_filtered_case_names[0],
            '--case', duplicate_filtered_case_names[1],
            '--case', duplicate_filtered_case_names[2],
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if duplicate_run_proc.returncode != 0:
        failures.append(
            'json regressierun met dubbele --case exitcode verwacht 0, kreeg '
            f'{duplicate_run_proc.returncode}'
        )

    duplicate_run_payload = {}
    duplicate_run_stdout = duplicate_run_proc.stdout.strip() or duplicate_run_proc.stderr.strip()
    if not duplicate_run_stdout:
        failures.append('json regressierun met dubbele --case gaf geen output')
    else:
        try:
            duplicate_run_payload = json.loads(duplicate_run_stdout)
            audit_bits.append('duplicate-run-json=' + json.dumps(duplicate_run_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(
                'json regressierun met dubbele --case hoort parsebare JSON te geven, kreeg parsefout: '
                f'{exc}'
            )

    if duplicate_run_payload:
        assert_runtime_metadata(duplicate_run_payload, 'json regressierun met dubbele --case')
        if duplicate_run_payload.get('requested_case_names') != duplicate_expected_case_names:
            failures.append(
                'json regressierun met dubbele --case requested_case_names hoort de unieke invoervolgorde te spiegelen'
            )
        if duplicate_run_payload.get('requested_case_count') != len(duplicate_expected_case_names):
            failures.append(
                'json regressierun met dubbele --case requested_case_count verwacht '
                f"{len(duplicate_expected_case_names)}, kreeg {duplicate_run_payload.get('requested_case_count')}"
            )
        if duplicate_run_payload.get('case_count') != len(duplicate_expected_case_names):
            failures.append(
                'json regressierun met dubbele --case case_count verwacht '
                f"{len(duplicate_expected_case_names)}, kreeg {duplicate_run_payload.get('case_count')}"
            )
        result_names = [result.get('name') for result in duplicate_run_payload.get('cases') or []]
        if len(result_names) != len(duplicate_expected_case_names) or len(result_names) != len(set(result_names)):
            failures.append(
                'json regressierun met dubbele --case hoort elke case hooguit één keer uit te voeren'
            )
        if duplicate_run_payload.get('selected_case_names') != duplicate_expected_case_names:
            failures.append(
                'json regressierun met dubbele --case selected_case_names hoort de unieke invoervolgorde te spiegelen'
            )
        if duplicate_run_payload.get('selected_case_count') != len(duplicate_expected_case_names):
            failures.append(
                'json regressierun met dubbele --case selected_case_count verwacht '
                f"{len(duplicate_expected_case_names)}, kreeg {duplicate_run_payload.get('selected_case_count')}"
            )
        if duplicate_run_payload.get('failed_count') != 0 or duplicate_run_payload.get('ok') is not True:
            failures.append('json regressierun met dubbele --case hoort groen te blijven voor dezelfde unieke subset')
        if duplicate_run_payload.get('available_case_names') != plain_lines:
            failures.append(
                'json regressierun met dubbele --case available_case_names hoort ook bij succes de volledige alfabetische caselijst mee te geven'
            )
        if duplicate_run_payload.get('available_case_count') != len(plain_lines):
            failures.append(
                'json regressierun met dubbele --case available_case_count hoort ook bij succes exact de volledige caseteller te geven'
            )

    unknown_plain_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'),
            '--case', unknown_case_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if unknown_plain_proc.returncode != 2:
        failures.append(
            f'plain onbekende --case exitcode verwacht 2, kreeg {unknown_plain_proc.returncode}'
        )
    if f'onbekende regressiecase: {unknown_case_name}' not in (unknown_plain_proc.stderr or ''):
        failures.append('plain onbekende --case hoort een duidelijke stderr-melding te geven')

    suggested_plain_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'),
            '--case', suggested_unknown_case_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if suggested_plain_proc.returncode != 2:
        failures.append(
            f'plain onbekende typofout-case exitcode verwacht 2, kreeg {suggested_plain_proc.returncode}'
        )
    if expected_suggested_case_name not in (suggested_plain_proc.stderr or ''):
        failures.append('plain onbekende typofout-case hoort een suggestie op stderr te geven')

    unknown_json_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json',
            '--case', unknown_case_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if unknown_json_proc.returncode != 2:
        failures.append(
            f'json onbekende --case exitcode verwacht 2, kreeg {unknown_json_proc.returncode}'
        )

    unknown_json_payload = {}
    unknown_json_stdout = unknown_json_proc.stdout.strip() or unknown_json_proc.stderr.strip()
    if not unknown_json_stdout:
        failures.append('json onbekende --case gaf geen output')
    else:
        try:
            unknown_json_payload = json.loads(unknown_json_stdout)
            audit_bits.append('unknown-json=' + json.dumps(unknown_json_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(
                'json onbekende --case hoort parsebare JSON te geven, kreeg parsefout: '
                f'{exc}'
            )

    if unknown_json_payload:
        assert_runtime_metadata(unknown_json_payload, 'json onbekende --case')
        if unknown_json_payload.get('ok') is not False:
            failures.append(f"json onbekende --case ok verwacht False, kreeg {unknown_json_payload.get('ok')}")
        if unknown_json_payload.get('error') != 'unknown-cases':
            failures.append(
                'json onbekende --case error verwacht unknown-cases, kreeg '
                f"{unknown_json_payload.get('error')}"
            )
        if unknown_json_payload.get('requested_case_names') != [unknown_case_name]:
            failures.append('json onbekende --case requested_case_names hoort de opgegeven invoer te spiegelen')
        if unknown_json_payload.get('requested_case_count') != 1:
            failures.append(
                'json onbekende --case requested_case_count verwacht 1, kreeg '
                f"{unknown_json_payload.get('requested_case_count')}"
            )
        if unknown_json_payload.get('selected_case_names') != []:
            failures.append('json onbekende --case selected_case_names hoort leeg te zijn zonder geldige matches')
        if unknown_json_payload.get('selected_case_count') != 0:
            failures.append(
                'json onbekende --case selected_case_count verwacht 0, kreeg '
                f"{unknown_json_payload.get('selected_case_count')}"
            )
        if unknown_json_payload.get('unknown_case_names') != [unknown_case_name]:
            failures.append('json onbekende --case unknown_case_names hoort de onbekende invoer te spiegelen')
        if unknown_json_payload.get('unknown_case_count') != 1:
            failures.append(
                'json onbekende --case unknown_case_count verwacht 1, kreeg '
                f"{unknown_json_payload.get('unknown_case_count')}"
            )
        available_case_names = unknown_json_payload.get('available_case_names')
        if available_case_names != plain_lines:
            failures.append(
                'json onbekende --case available_case_names hoort de volledige alfabetische caselijst mee te geven'
            )
        available_case_count = unknown_json_payload.get('available_case_count')
        if available_case_count != len(plain_lines):
            failures.append(
                'json onbekende --case available_case_count hoort exact de volledige caseteller te geven'
            )
        unknown_json_suggestions = unknown_json_payload.get('suggested_case_names_by_input')
        if not isinstance(unknown_json_suggestions, dict):
            failures.append('json onbekende --case suggested_case_names_by_input hoort een dict te zijn')
        elif unknown_json_suggestions.get(unknown_case_name) != []:
            failures.append(
                'json onbekende --case zonder typofout hoort een lege suggestielijst te geven'
            )

    mixed_unknown_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json',
            '--case', expected_case_name,
            '--case', unknown_case_name,
            '--case', expected_case_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if mixed_unknown_proc.returncode != 2:
        failures.append(
            f'json gemengde geldige/onbekende --case exitcode verwacht 2, kreeg {mixed_unknown_proc.returncode}'
        )

    mixed_unknown_payload = {}
    mixed_unknown_stdout = mixed_unknown_proc.stdout.strip() or mixed_unknown_proc.stderr.strip()
    if not mixed_unknown_stdout:
        failures.append('json gemengde geldige/onbekende --case gaf geen output')
    else:
        try:
            mixed_unknown_payload = json.loads(mixed_unknown_stdout)
            audit_bits.append('unknown-json-mixed=' + json.dumps(mixed_unknown_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(
                'json gemengde geldige/onbekende --case hoort parsebare JSON te geven, kreeg parsefout: '
                f'{exc}'
            )

    if mixed_unknown_payload:
        assert_runtime_metadata(mixed_unknown_payload, 'json gemengde geldige/onbekende --case')
        if mixed_unknown_payload.get('ok') is not False:
            failures.append(
                'json gemengde geldige/onbekende --case ok verwacht False bij onbekende subset'
            )
        if mixed_unknown_payload.get('error') != 'unknown-cases':
            failures.append(
                'json gemengde geldige/onbekende --case error verwacht unknown-cases, kreeg '
                f"{mixed_unknown_payload.get('error')}"
            )
        if mixed_unknown_payload.get('requested_case_names') != [expected_case_name, unknown_case_name]:
            failures.append(
                'json gemengde geldige/onbekende --case requested_case_names hoort de unieke invoervolgorde te spiegelen'
            )
        if mixed_unknown_payload.get('requested_case_count') != 2:
            failures.append(
                'json gemengde geldige/onbekende --case requested_case_count verwacht 2, kreeg '
                f"{mixed_unknown_payload.get('requested_case_count')}"
            )
        if mixed_unknown_payload.get('selected_case_names') != [expected_case_name]:
            failures.append(
                'json gemengde geldige/onbekende --case selected_case_names hoort de geldige subset te bewaren'
            )
        if mixed_unknown_payload.get('selected_case_count') != 1:
            failures.append(
                'json gemengde geldige/onbekende --case selected_case_count verwacht 1, kreeg '
                f"{mixed_unknown_payload.get('selected_case_count')}"
            )
        if mixed_unknown_payload.get('unknown_case_names') != [unknown_case_name]:
            failures.append(
                'json gemengde geldige/onbekende --case unknown_case_names hoort alleen de onbekende subset te tonen'
            )
        if mixed_unknown_payload.get('unknown_case_count') != 1:
            failures.append(
                'json gemengde geldige/onbekende --case unknown_case_count verwacht 1, kreeg '
                f"{mixed_unknown_payload.get('unknown_case_count')}"
            )
        if mixed_unknown_payload.get('available_case_names') != plain_lines:
            failures.append(
                'json gemengde geldige/onbekende --case available_case_names hoort de volledige alfabetische caselijst mee te geven'
            )
        if mixed_unknown_payload.get('available_case_count') != len(plain_lines):
            failures.append(
                'json gemengde geldige/onbekende --case available_case_count hoort exact de volledige caseteller te geven'
            )

    suggested_json_proc = subprocess.run(
        [
            'python3', str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'), '--json',
            '--case', suggested_unknown_case_name,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if suggested_json_proc.returncode != 2:
        failures.append(
            f'json onbekende typofout-case exitcode verwacht 2, kreeg {suggested_json_proc.returncode}'
        )

    suggested_json_payload = {}
    suggested_json_stdout = suggested_json_proc.stdout.strip() or suggested_json_proc.stderr.strip()
    if not suggested_json_stdout:
        failures.append('json onbekende typofout-case gaf geen output')
    else:
        try:
            suggested_json_payload = json.loads(suggested_json_stdout)
            audit_bits.append('unknown-json-suggested=' + json.dumps(suggested_json_payload, ensure_ascii=False))
        except json.JSONDecodeError as exc:
            failures.append(
                'json onbekende typofout-case hoort parsebare JSON te geven, kreeg parsefout: '
                f'{exc}'
            )

    if suggested_json_payload:
        assert_runtime_metadata(suggested_json_payload, 'json onbekende typofout-case')
        if suggested_json_payload.get('ok') is not False:
            failures.append('json onbekende typofout-case ok verwacht False bij onbekende invoer')
        if suggested_json_payload.get('error') != 'unknown-cases':
            failures.append(
                'json onbekende typofout-case error verwacht unknown-cases, kreeg '
                f"{suggested_json_payload.get('error')}"
            )
        if suggested_json_payload.get('requested_case_names') != [suggested_unknown_case_name]:
            failures.append(
                'json onbekende typofout-case requested_case_names hoort de typo-invoer te spiegelen'
            )
        if suggested_json_payload.get('requested_case_count') != 1:
            failures.append(
                'json onbekende typofout-case requested_case_count verwacht 1, kreeg '
                f"{suggested_json_payload.get('requested_case_count')}"
            )
        if suggested_json_payload.get('selected_case_names') != []:
            failures.append('json onbekende typofout-case selected_case_names hoort leeg te zijn zonder geldige matches')
        if suggested_json_payload.get('selected_case_count') != 0:
            failures.append(
                'json onbekende typofout-case selected_case_count verwacht 0, kreeg '
                f"{suggested_json_payload.get('selected_case_count')}"
            )
        if suggested_json_payload.get('unknown_case_names') != [suggested_unknown_case_name]:
            failures.append(
                'json onbekende typofout-case unknown_case_names hoort de typo-subset te tonen'
            )
        if suggested_json_payload.get('unknown_case_count') != 1:
            failures.append(
                'json onbekende typofout-case unknown_case_count verwacht 1, kreeg '
                f"{suggested_json_payload.get('unknown_case_count')}"
            )
        if suggested_json_payload.get('available_case_names') != plain_lines:
            failures.append(
                'json onbekende typofout-case available_case_names hoort de volledige alfabetische caselijst mee te geven'
            )
        if suggested_json_payload.get('available_case_count') != len(plain_lines):
            failures.append(
                'json onbekende typofout-case available_case_count hoort exact de volledige caseteller te geven'
            )
        suggested_json_suggestions = suggested_json_payload.get('suggested_case_names_by_input')
        if not isinstance(suggested_json_suggestions, dict):
            failures.append('json onbekende typofout-case suggested_case_names_by_input hoort een dict te zijn')
        else:
            typo_suggestions = suggested_json_suggestions.get(suggested_unknown_case_name)
            if not isinstance(typo_suggestions, list) or expected_suggested_case_name not in typo_suggestions:
                failures.append(
                    'json onbekende typofout-case hoort de dichtstbijzijnde casenaam voor te stellen'
                )

    return {
        'name': 'regression-check-list-cases-output',
        'path': str(ROOT / 'scripts' / 'ai-briefing-regression-check.py'),
        'ok': not failures,
        'failures': failures,
        'audit_ok': not failures,
        'audit_text': ' || '.join(bit for bit in audit_bits if bit),
        'item_count': None,
        'items_with_source_count': None,
        'items_with_valid_source_line_count': None,
        'items_with_invalid_source_line_count': None,
        'first3_items_with_source_count': None,
        'first3_items_with_valid_source_line_count': None,
        'first3_items_with_multiple_sources_count': None,
        'first3_items_with_primary_source_count': None,
        'first3_primary_source_family_count': None,
        'first3_primary_fresh_item_count': None,
        'explicit_dated_item_count': None,
        'explicit_recent_dated_first3_count': None,
        'explicit_fresh_dated_first3_count': None,
        'future_dated_item_count': None,
        'invalid_source_line_issue_counts': None,
        'exact_field_line_counts': None,
        'items_with_exact_field_order_count': None,
        'items_with_field_order_mismatch_count': None,
        'numbered_title_heading_count': None,
    }


def build_named_case_runners(module, producer_module):
    named_cases = {}
    named_cases.update({case['name']: (lambda case=case: evaluate_case(module, case)) for case in DEFAULT_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_status_phase_case(module, case)) for case in STATUS_PHASE_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_status_stdout_case(case)) for case in STATUS_STDOUT_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_status_summary_audit_case(module, case)) for case in STATUS_SUMMARY_AUDIT_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_proof_recheck_case(case)) for case in PROOF_RECHECK_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_proof_recheck_producer_case(case)) for case in PROOF_RECHECK_PRODUCER_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_brief_consumer_case(case)) for case in BRIEF_CONSUMER_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_watchdog_alert_case(case)) for case in WATCHDOG_ALERT_CASES})
    named_cases.update({case['name']: (lambda case=case: evaluate_watchdog_producer_case(case)) for case in WATCHDOG_PRODUCER_CASES})
    named_cases['proof-recheck-producer-quiet-falls-back-to-requested-outputs'] = (
        lambda: evaluate_producer_quiet_requested_outputs_fallback_case(producer_module)
    )
    named_cases['regression-check-list-cases-output'] = evaluate_list_cases_output_case
    named_cases['proof-recheck-consumer-format-passthrough'] = evaluate_proof_recheck_consumer_format_passthrough_case
    named_cases['watchdog-consumer-format-passthrough'] = evaluate_watchdog_consumer_format_passthrough_case
    named_cases['watchdog-alert-consumer-format-passthrough'] = evaluate_watchdog_alert_consumer_format_passthrough_case
    return named_cases


def main():
    started_at = datetime.now(timezone.utc)
    started_monotonic = monotonic()
    parser = argparse.ArgumentParser(description='Regressiecheck voor AI-briefing output-audits')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument(
        '--case',
        action='append',
        default=[],
        help='draai alleen de opgegeven casenaam (mag meerdere keren)',
    )
    parser.add_argument('--list-cases', action='store_true', help='toon beschikbare casenamen en stop')
    args = parser.parse_args()

    module = load_status_module()
    producer_module = load_proof_recheck_producer_module()
    named_cases = build_named_case_runners(module, producer_module)

    unknown_cases = [case_name for case_name in args.case if case_name not in named_cases]
    if unknown_cases:
        emit_unknown_case_error(
            requested_case_names=args.case,
            unknown_cases=unknown_cases,
            available_case_names=sorted(named_cases.keys()),
            available_case_count=len(named_cases),
            as_json=args.json,
            run_metadata=build_run_metadata(
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
                duration_ms=int(round((monotonic() - started_monotonic) * 1000)),
            ),
        )
        raise SystemExit(2)

    if args.list_cases:
        requested_case_names = unique_case_names(args.case)
        selected_case_names = sorted(unique_case_names(args.case or list(named_cases.keys())))
        run_metadata = build_run_metadata(
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            duration_ms=int(round((monotonic() - started_monotonic) * 1000)),
        )
        if args.json:
            print(json.dumps({
                'ok': True,
                'requested_case_names': requested_case_names,
                'requested_case_count': len(requested_case_names),
                'case_count': len(selected_case_names),
                'cases': selected_case_names,
                'selected_case_names': selected_case_names,
                'selected_case_count': len(selected_case_names),
                'available_case_names': sorted(named_cases.keys()),
                'available_case_count': len(named_cases),
                **run_metadata,
            }, ensure_ascii=False, indent=2))
        else:
            for case_name in selected_case_names:
                print(case_name)
        raise SystemExit(0)

    requested_case_names = unique_case_names(args.case)
    selected_case_names = unique_case_names(args.case or list(named_cases.keys()))
    results = [named_cases[case_name]() for case_name in selected_case_names]
    overall_ok = all(result['ok'] for result in results)
    failing_results = [result for result in results if not result['ok']]
    summary = {
        'case_count': len(results),
        'passed_count': len(results) - len(failing_results),
        'failed_count': len(failing_results),
        'failing_case_names': [result['name'] for result in failing_results],
    }
    run_metadata = build_run_metadata(
        started_at=started_at,
        finished_at=datetime.now(timezone.utc),
        duration_ms=int(round((monotonic() - started_monotonic) * 1000)),
    )

    if args.json:
        print(json.dumps({
            'ok': overall_ok,
            'summary': summary,
            'requested_case_names': requested_case_names,
            'requested_case_count': len(requested_case_names),
            'case_count': summary['case_count'],
            'passed_count': summary['passed_count'],
            'failed_count': summary['failed_count'],
            'failing_case_names': summary['failing_case_names'],
            'selected_case_names': selected_case_names,
            'selected_case_count': len(selected_case_names),
            'available_case_names': sorted(named_cases.keys()),
            'available_case_count': len(named_cases),
            'cases': results,
            'results': results,
            **run_metadata,
        }, ensure_ascii=False, indent=2))
    else:
        for result in results:
            status = 'ok' if result['ok'] else 'FAIL'
            print(f"[{status}] {result['name']}: {result['audit_text']}")
            if result['failures']:
                for failure in result['failures']:
                    print(f"  - {failure}")
        print(
            f"samenvatting: {summary['passed_count']}/{summary['case_count']} ok"
            if overall_ok
            else f"samenvatting: {summary['failed_count']} fail van {summary['case_count']}"
        )
        print('ok' if overall_ok else 'FAIL')

    raise SystemExit(0 if overall_ok else 1)


if __name__ == '__main__':
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
