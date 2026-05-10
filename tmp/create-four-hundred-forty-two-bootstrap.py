#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-one', 'four-hundred-forty-two'),
    ('vierhonderdeenenveertig', 'vierhonderdtweeenveertig'),
    ('all_cases[:426]', 'all_cases[:427]'),
    ('{UNKNOWN, TYPO}][:426]', '{UNKNOWN, TYPO}][:427]'),
    ('!= 426', '!= 427'),
    ('kreeg 426', 'kreeg 427'),
    (', 424, 425]', ', 424, 425, 426]'),
]
for src_name in [
    'create-four-hundred-forty-one-minimal.py',
    'make-four-hundred-forty-one.py',
    'create-four-hundred-forty-one-files.py',
    'create-four-hundred-forty-one.py',
    'generate-validate-four-hundred-forty-one.py',
    'validate-four-hundred-forty-one-valid-list-cases.py',
    'validate-four-hundred-forty-one-valid-mixed.py',
    'verify-four-hundred-forty-one.py'
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-one', 'four-hundred-forty-two')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
