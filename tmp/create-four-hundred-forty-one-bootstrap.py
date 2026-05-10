#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty', 'four-hundred-forty-one'),
    ('vierhonderdveertig', 'vierhonderdeenenveertig'),
    ('all_cases[:425]', 'all_cases[:426]'),
    ('{UNKNOWN, TYPO}][:425]', '{UNKNOWN, TYPO}][:426]'),
    ('!= 425', '!= 426'),
    ('kreeg 425', 'kreeg 426'),
    (', 423, 424]', ', 423, 424, 425]'),
]
for src_name in [
    'create-four-hundred-forty-minimal.py',
'make-four-hundred-forty.py',
'create-four-hundred-forty-files.py',
'create-four-hundred-forty.py',
'generate-validate-four-hundred-forty.py',
'validate-four-hundred-forty-valid-list-cases.py',
'validate-four-hundred-forty-valid-mixed.py',
'verify-four-hundred-forty.py'
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty', 'four-hundred-forty-one')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
