#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-four', 'four-hundred-fifty-five'),
    ('vierhonderdvierenvijftig', 'vierhonderdvijfenvijftig'),
    ('all_cases[:439]', 'all_cases[:440]'),
    ('{UNKNOWN, TYPO}][:439]', '{UNKNOWN, TYPO}][:440]'),
    ('!= 439', '!= 440'),
    ('kreeg 439', 'kreeg 440'),
    (', 429, 430, 431, 432, 433, 434, 435, 436, 437, 438]', ', 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439]'),
]
for src_name in [
    'create-four-hundred-fifty-four-minimal.py',
    'make-four-hundred-fifty-four.py',
    'create-four-hundred-fifty-four-files.py',
    'create-four-hundred-fifty-four.py',
    'generate-validate-four-hundred-fifty-four.py',
    'validate-four-hundred-fifty-four-valid-list-cases.py',
    'validate-four-hundred-fifty-four-valid-mixed.py',
    'verify-four-hundred-fifty-four.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-four', 'four-hundred-fifty-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
