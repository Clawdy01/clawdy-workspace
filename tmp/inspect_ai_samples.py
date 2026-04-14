#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

files = [
    Path('tmp/ai-briefing-duplicate-sample.txt'),
    Path('tmp/ai-briefing-duplicate-top3-source-sample.txt'),
    Path('tmp/ai-briefing-future-sample.txt'),
    Path('tmp/ai-briefing-multi-source-weak-sample.txt'),
    Path('tmp/ai-briefing-top3-nonprimary-sample.txt'),
    Path('tmp/ai-briefing-top3-same-primary-family-sample.txt'),
]
keys = [
    'ok','item_count','items_with_source_count','items_with_valid_source_line_count','items_with_invalid_source_line_count',
    'first3_items_with_source_count','first3_items_with_valid_source_line_count','first3_items_with_multiple_sources_count',
    'first3_items_with_primary_source_count','first3_evidenced_item_count','first3_primary_source_domain_count',
    'first3_primary_source_family_count','first3_primary_fresh_item_count','source_url_count','unique_source_url_count',
    'source_domain_count','first3_unique_source_url_count','first3_source_domain_count','future_dated_item_count',
    'invalid_source_line_issue_counts','exact_field_line_counts','reasons'
]
for path in files:
    proc = subprocess.run([
        'python3', 'scripts/ai-briefing-status.py', '--summary-file', str(path), '--json'
    ], check=True, capture_output=True, text=True)
    data = json.loads(proc.stdout)
    print(f'FILE:{path.name}')
    for key in keys:
        if key in data:
            print(f'{key}={json.dumps(data[key], ensure_ascii=False, sort_keys=True)}')
