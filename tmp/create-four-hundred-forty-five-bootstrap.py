#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-four', 'four-hundred-forty-five'),
    ('vierhonderdvierenveertig', 'vierhonderdvijfenveertig'),
    ('all_cases[:429]', 'all_cases[:430]'),
    ('{UNKNOWN, TYPO}][:429]', '{UNKNOWN, TYPO}][:430]'),
    ('!= 429', '!= 430'),
    ('kreeg 429', 'kreeg 430'),
    (', 425, 426, 427, 428]', ', 425, 426, 427, 428, 429]'),
]
for src_name in [
    'create-four-hundred-forty-four-minimal.py',
    'make-four-hundred-forty-four.py',
    'create-four-hundred-forty-four-files.py',
    'create-four-hundred-forty-four.py',
    'generate-validate-four-hundred-forty-four.py',
    'validate-four-hundred-forty-four-valid-list-cases.py',
    'validate-four-hundred-forty-four-valid-mixed.py',
    'verify-four-hundred-forty-four.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-four', 'four-hundred-forty-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
