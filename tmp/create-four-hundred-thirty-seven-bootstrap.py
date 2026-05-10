#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
replacements = [
    ('four-hundred-thirty-six', 'four-hundred-thirty-seven'),
    ('vierhonderdzesendertig', 'vierhonderdzevenendertig'),
    ('all_cases[:421]', 'all_cases[:422]'),
    ('{UNKNOWN, TYPO}][:421]', '{UNKNOWN, TYPO}][:422]'),
    ('!= 421', '!= 422'),
    ('kreeg 421', 'kreeg 422'),
    (' 420]', ' 420, 421]'),
    ('[:420]', '[:421]'),
    ('!= 420', '!= 421'),
    ('kreeg 420', 'kreeg 421'),
    (' 421)', ' 422)'),
    (', 413, 414, 415, 416, 417, 418, 419, 420]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421]'),
]
for src_name in [
    'create-four-hundred-thirty-six-minimal.py',
    'make-four-hundred-thirty-six.py',
    'create-four-hundred-thirty-six-files.py',
    'create-four-hundred-thirty-six.py',
    'generate-validate-four-hundred-thirty-six.py',
    'validate-four-hundred-thirty-six-valid-list-cases.py',
    'validate-four-hundred-thirty-six-valid-mixed.py',
    'verify-four-hundred-thirty-six.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-thirty-six', 'four-hundred-thirty-seven')
    text = src.read_text()
    for old, new in replacements:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
