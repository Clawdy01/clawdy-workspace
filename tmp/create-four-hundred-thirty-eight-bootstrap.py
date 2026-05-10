#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
replacements = [
    ('four-hundred-thirty-seven', 'four-hundred-thirty-eight'),
    ('vierhonderdzevenendertig', 'vierhonderdachtendertig'),
    ('all_cases[:422]', 'all_cases[:423]'),
    ('{UNKNOWN, TYPO}][:422]', '{UNKNOWN, TYPO}][:423]'),
    ('!= 422', '!= 423'),
    ('kreeg 422', 'kreeg 423'),
    (' 421]', ' 421, 422]'),
    ('[:421]', '[:422]'),
    ('!= 421', '!= 422'),
    ('kreeg 421', 'kreeg 422'),
    (' 422)', ' 423)'),
    (', 413, 414, 415, 416, 417, 418, 419, 420, 421]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422]'),
]
for src_name in [
    'create-four-hundred-thirty-seven-minimal.py',
    'make-four-hundred-thirty-seven.py',
    'create-four-hundred-thirty-seven-files.py',
    'create-four-hundred-thirty-seven.py',
    'generate-validate-four-hundred-thirty-seven.py',
    'validate-four-hundred-thirty-seven-valid-list-cases.py',
    'validate-four-hundred-thirty-seven-valid-mixed.py',
    'verify-four-hundred-thirty-seven.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-thirty-seven', 'four-hundred-thirty-eight')
    text = src.read_text()
    for old, new in replacements:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
