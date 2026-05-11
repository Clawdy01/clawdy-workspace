#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-one', 'four-hundred-fifty-two'),
    ('vierhonderdeenenvijftig', 'vierhonderdtweeënvijftig'),
    ('all_cases[:436]', 'all_cases[:437]'),
    ('{UNKNOWN, TYPO}][:436]', '{UNKNOWN, TYPO}][:437]'),
    ('!= 436', '!= 437'),
    ('kreeg 436', 'kreeg 437'),
    (', 427, 428, 429, 430, 431, 432, 433, 434, 435]', ', 427, 428, 429, 430, 431, 432, 433, 434, 435, 436]'),
]
for src_name in [
    'create-four-hundred-fifty-one-minimal.py',
    'make-four-hundred-fifty-one.py',
    'create-four-hundred-fifty-one-files.py',
    'create-four-hundred-fifty-one.py',
    'generate-validate-four-hundred-fifty-one.py',
    'validate-four-hundred-fifty-one-valid-list-cases.py',
    'validate-four-hundred-fifty-one-valid-mixed.py',
    'verify-four-hundred-fifty-one.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-one', 'four-hundred-fifty-two')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
