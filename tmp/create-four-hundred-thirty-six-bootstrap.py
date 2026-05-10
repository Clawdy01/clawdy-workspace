#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
replacements = [
    ('four-hundred-thirty-five', 'four-hundred-thirty-six'),
    ('vierhonderdvijfendertig', 'vierhonderdzesendertig'),
    ('all_cases[:420]', 'all_cases[:421]'),
    ('{UNKNOWN, TYPO}][:420]', '{UNKNOWN, TYPO}][:421]'),
    ('!= 420', '!= 421'),
    ('kreeg 420', 'kreeg 421'),
    (' 419]', ' 419, 420]'),
    ('[:419]', '[:420]'),
    ('!= 419', '!= 420'),
    ('kreeg 419', 'kreeg 420'),
    (' 420)', ' 421)'),
    (', 413, 414, 415, 416, 417, 418, 419]', ', 413, 414, 415, 416, 417, 418, 419, 420]'),
]
for src_name in [
    'create-four-hundred-thirty-five-minimal.py',
    'make-four-hundred-thirty-five.py',
    'create-four-hundred-thirty-five-files.py',
    'create-four-hundred-thirty-five.py',
    'generate-validate-four-hundred-thirty-five.py',
    'validate-four-hundred-thirty-five-valid-list-cases.py',
    'validate-four-hundred-thirty-five-valid-mixed.py',
    'verify-four-hundred-thirty-five.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-thirty-five', 'four-hundred-thirty-six')
    text = src.read_text()
    for old, new in replacements:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
