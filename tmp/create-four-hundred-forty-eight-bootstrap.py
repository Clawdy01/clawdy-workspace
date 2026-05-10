#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-seven', 'four-hundred-forty-eight'),
    ('vierhonderdzevenenveertig', 'vierhonderdachtenveertig'),
    ('all_cases[:432]', 'all_cases[:433]'),
    ('{UNKNOWN, TYPO}][:432]', '{UNKNOWN, TYPO}][:433]'),
    ('!= 432', '!= 433'),
    ('kreeg 432', 'kreeg 433'),
    (', 426, 427, 428, 429, 430, 431]', ', 426, 427, 428, 429, 430, 431, 432]'),
]
for src_name in [
    'create-four-hundred-forty-seven-minimal.py',
    'make-four-hundred-forty-seven.py',
    'create-four-hundred-forty-seven-files.py',
    'create-four-hundred-forty-seven.py',
    'generate-validate-four-hundred-forty-seven.py',
    'validate-four-hundred-forty-seven-valid-list-cases.py',
    'validate-four-hundred-forty-seven-valid-mixed.py',
    'verify-four-hundred-forty-seven.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-seven', 'four-hundred-forty-eight')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
