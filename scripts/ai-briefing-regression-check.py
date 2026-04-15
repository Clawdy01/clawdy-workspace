#!/usr/bin/env python3
import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'
DEFAULT_REFERENCE_MS = int(datetime(2026, 4, 15, 0, 0, tzinfo=timezone.utc).timestamp() * 1000)
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
        'expect_first3_items_with_primary_source_count': 2,
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
            'niet elk top-3 item heeft een herkenbare primaire bron (2/3)',
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


def load_status_module():
    spec = importlib.util.spec_from_file_location('ai_briefing_status', STATUS_SCRIPT)
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


def main():
    parser = argparse.ArgumentParser(description='Regressiecheck voor AI-briefing output-audits')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    args = parser.parse_args()

    module = load_status_module()
    results = [evaluate_case(module, case) for case in DEFAULT_CASES]
    overall_ok = all(result['ok'] for result in results)

    if args.json:
        print(json.dumps({'ok': overall_ok, 'results': results}, ensure_ascii=False, indent=2))
    else:
        for result in results:
            status = 'ok' if result['ok'] else 'FAIL'
            print(f"[{status}] {result['name']}: {result['audit_text']}")
            if result['failures']:
                for failure in result['failures']:
                    print(f"  - {failure}")
        print('ok' if overall_ok else 'FAIL')

    raise SystemExit(0 if overall_ok else 1)


if __name__ == '__main__':
    main()
