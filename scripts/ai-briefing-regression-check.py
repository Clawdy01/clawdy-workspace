#!/usr/bin/env python3
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'
DEFAULT_CASES = [
    {
        'name': 'real-run-2026-04-14-0902-failed-summary',
        'path': ROOT / 'tmp' / 'ai-briefing-run-2026-04-14-0902-failed-summary.txt',
        'expect_ok': False,
        'expect_item_count': 10,
        'expect_items_with_source_count': 0,
        'expect_first3_items_with_source_count': 0,
        'expect_first3_items_with_multiple_sources_count': 0,
        'expect_first3_primary_source_family_count': 0,
        'expect_first3_primary_fresh_item_count': 0,
        'expect_reason_substrings': [
            'niet elk item heeft een zichtbare bron-URL',
            'te weinig top-3 items met meerdere bron-URLs',
            'geen herkenbare primaire bron in top 3 items',
        ],
    },
    {
        'name': 'format-compliant-sample',
        'path': ROOT / 'tmp' / 'ai-briefing-format-compliant-sample.txt',
        'expect_ok': True,
        'expect_item_count': 4,
        'expect_items_with_source_count': 4,
        'expect_first3_items_with_source_count': 3,
        'expect_first3_items_with_multiple_sources_count': 3,
        'expect_first3_primary_source_family_count': 2,
        'expect_first3_primary_fresh_item_count': 2,
        'expect_reason_substrings': [],
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
    audit = module.audit_summary_output(summary_text)
    failures = []
    if audit.get('ok') != case['expect_ok']:
        failures.append(f"ok verwacht {case['expect_ok']}, kreeg {audit.get('ok')}")
    if 'expect_item_count' in case and audit.get('item_count') != case['expect_item_count']:
        failures.append(f"item_count verwacht {case['expect_item_count']}, kreeg {audit.get('item_count')}")
    if 'expect_items_with_source_count' in case and audit.get('items_with_source_count') != case['expect_items_with_source_count']:
        failures.append(
            f"items_with_source_count verwacht {case['expect_items_with_source_count']}, kreeg {audit.get('items_with_source_count')}"
        )
    if 'expect_first3_items_with_source_count' in case and audit.get('first3_items_with_source_count') != case['expect_first3_items_with_source_count']:
        failures.append(
            'first3_items_with_source_count verwacht '
            f"{case['expect_first3_items_with_source_count']}, kreeg {audit.get('first3_items_with_source_count')}"
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
        'first3_items_with_source_count': audit.get('first3_items_with_source_count'),
        'first3_items_with_multiple_sources_count': audit.get('first3_items_with_multiple_sources_count'),
        'first3_primary_source_family_count': audit.get('first3_primary_source_family_count'),
        'first3_primary_fresh_item_count': audit.get('first3_primary_fresh_item_count'),
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
