#!/usr/bin/env python3
import argparse
import importlib.util
import json
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'
PROOF_RECHECK_SCRIPT = ROOT / 'scripts' / 'ai-briefing-proof-recheck.py'
PROOF_RECHECK_PRODUCER_SCRIPT = ROOT / 'scripts' / 'ai-briefing-proof-recheck-producer.py'
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
REFERENCE_MS_BEFORE_SLOT_TOMORROW = CURRENT_PROOF_NEXT_SLOT_AT - ((24 * 60 * 60 + 2 * 60) * 1000)
REFERENCE_MS_NEXT_DAY_BEFORE_SLOT = CURRENT_PROOF_NEXT_SLOT_AT - (2 * 60 * 1000)
REFERENCE_MS_CURRENT_SLOT_GRACE = CURRENT_PROOF_NEXT_SLOT_AT + (5 * 60 * 1000)
REFERENCE_MS_RECHECK_WINDOW_OPEN = CURRENT_PROOF_RECHECK_AFTER_AT
STATUS_BEFORE_SLOT_TOMORROW = run_status_json(REFERENCE_MS_BEFORE_SLOT_TOMORROW)
STATUS_NEXT_DAY_BEFORE_SLOT = run_status_json(REFERENCE_MS_NEXT_DAY_BEFORE_SLOT)
STATUS_CURRENT_SLOT_GRACE = run_status_json(REFERENCE_MS_CURRENT_SLOT_GRACE)
STATUS_RECHECK_WINDOW_OPEN = run_status_json(REFERENCE_MS_RECHECK_WINDOW_OPEN)
CURRENT_PROOF_NEXT_SLOT_TEXT = STATUS_BEFORE_SLOT_TOMORROW['proof_wait_until_text']
CURRENT_PROOF_RECHECK_AFTER_TEXT = STATUS_BEFORE_SLOT_TOMORROW['proof_recheck_after_text']
CURRENT_PROOF_CONFIG_HASH = LIVE_STATUS_BASELINE.get('proof_config_hash')
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
            'hercheckvenster is open; draai nu ai-briefing-status/watchdog opnieuw',
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

        overall = payload.get('overall') or {}
        top_level_overall_alias_keys = [
            'returncode',
            'exit_code',
            'summary',
            'state',
            'result_kind',
            'result_text',
            'reference_now_text',
            'reference_context_text',
            'proof_state',
            'proof_blocker_kind',
            'proof_wait_until_at',
            'proof_wait_until_text',
            'proof_recheck_after_at',
            'proof_next_action_kind',
            'proof_next_action_window_text',
            'proof_recheck_schedule_ok',
            'proof_recheck_schedule_job_name',
            'proof_recheck_schedule_expr',
            'proof_recheck_schedule_tz',
            'proof_config_hash',
            'last_run_config_relation',
            'consumer_output_paths',
            'consumer_requested_output_paths',
            'consumer_requested_output_count',
            'consumer_requested_output_channel_count',
            'consumer_requested_output_count_text',
            'consumer_requested_output_channel_count_text',
            'consumer_requested_output_channels_text',
            'consumer_requested_outputs_status_kind',
            'consumer_requested_outputs_status_text',
            'consumer_output_count',
            'consumer_output_channel_count',
            'consumer_output_channel_count_text',
            'consumer_output_channels_text',
            'consumer_outputs_count_text',
            'consumer_outputs_status_kind',
            'consumer_outputs_missing_count',
            'consumer_outputs_unexpected_count',
            'consumer_effective_output_source_text',
            'consumer_effective_output_channel_count',
            'consumer_effective_output_channel_count_text',
            'consumer_effective_output_channels_text',
            'consumer_effective_outputs_status_kind',
        ]
        if payload.get('consumer_root') != temp_dir:
            failures.append(f"consumer_root verwacht {temp_dir}, kreeg {payload.get('consumer_root')}")
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

        artifact_text_combined = ' || '.join(
            bit
            for bit in [
                artifact_text,
                json.dumps(artifact_json_payload, ensure_ascii=False) if artifact_json_payload else '',
                json.dumps(artifact_jsonl_payload, ensure_ascii=False) if artifact_jsonl_payload else '',
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


def main():
    parser = argparse.ArgumentParser(description='Regressiecheck voor AI-briefing output-audits')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    args = parser.parse_args()

    module = load_status_module()
    producer_module = load_proof_recheck_producer_module()
    results = [evaluate_case(module, case) for case in DEFAULT_CASES]
    results.extend(evaluate_status_phase_case(module, case) for case in STATUS_PHASE_CASES)
    results.extend(evaluate_proof_recheck_case(case) for case in PROOF_RECHECK_CASES)
    results.extend(evaluate_proof_recheck_producer_case(case) for case in PROOF_RECHECK_PRODUCER_CASES)
    results.append(evaluate_producer_quiet_requested_outputs_fallback_case(producer_module))
    results.append(evaluate_proof_recheck_consumer_format_passthrough_case())
    overall_ok = all(result['ok'] for result in results)
    failing_results = [result for result in results if not result['ok']]
    summary = {
        'case_count': len(results),
        'passed_count': len(results) - len(failing_results),
        'failed_count': len(failing_results),
        'failing_case_names': [result['name'] for result in failing_results],
    }

    if args.json:
        print(json.dumps({
            'ok': overall_ok,
            'summary': summary,
            'case_count': summary['case_count'],
            'passed_count': summary['passed_count'],
            'failed_count': summary['failed_count'],
            'failing_case_names': summary['failing_case_names'],
            'cases': results,
            'results': results,
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
