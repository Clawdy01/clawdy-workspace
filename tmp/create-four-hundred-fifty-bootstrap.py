#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-nine', 'four-hundred-fifty'),
    ('vierhonderdnegenenveertig', 'vierhonderdvijftig'),
    ('all_cases[:434]', 'all_cases[:435]'),
    ('{UNKNOWN, TYPO}][:434]', '{UNKNOWN, TYPO}][:435]'),
    ('!= 434', '!= 435'),
    ('kreeg 434', 'kreeg 435'),
    (', 427, 428, 429, 430, 431, 432, 433]', ', 427, 428, 429, 430, 431, 432, 433, 434]'),
]
for src_name in [
    'create-four-hundred-forty-nine-minimal.py',
    'make-four-hundred-forty-nine.py',
    'create-four-hundred-forty-nine-files.py',
    'create-four-hundred-forty-nine.py',
    'generate-validate-four-hundred-forty-nine.py',
    'validate-four-hundred-forty-nine-valid-list-cases.py',
    'validate-four-hundred-forty-nine-valid-mixed.py',
    'verify-four-hundred-forty-nine.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-nine', 'four-hundred-fifty')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
