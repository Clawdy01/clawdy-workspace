#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-eight', 'four-hundred-forty-nine'),
    ('vierhonderdachtenveertig', 'vierhonderdnegenenveertig'),
    ('all_cases[:433]', 'all_cases[:434]'),
    ('{UNKNOWN, TYPO}][:433]', '{UNKNOWN, TYPO}][:434]'),
    ('!= 433', '!= 434'),
    ('kreeg 433', 'kreeg 434'),
    (', 426, 427, 428, 429, 430, 431, 432]', ', 426, 427, 428, 429, 430, 431, 432, 433]'),
]
for src_name in [
    'create-four-hundred-forty-eight-minimal.py',
    'make-four-hundred-forty-eight.py',
    'create-four-hundred-forty-eight-files.py',
    'create-four-hundred-forty-eight.py',
    'generate-validate-four-hundred-forty-eight.py',
    'validate-four-hundred-forty-eight-valid-list-cases.py',
    'validate-four-hundred-forty-eight-valid-mixed.py',
    'verify-four-hundred-forty-eight.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-eight', 'four-hundred-forty-nine')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
