#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-three', 'four-hundred-fifty-four'),
    ('vierhonderddrieënvijftig', 'vierhonderdvierenvijftig'),
    ('all_cases[:438]', 'all_cases[:439]'),
    ('{UNKNOWN, TYPO}][:438]', '{UNKNOWN, TYPO}][:439]'),
    ('!= 438', '!= 439'),
    ('kreeg 438', 'kreeg 439'),
    (', 429, 430, 431, 432, 433, 434, 435, 436, 437]', ', 429, 430, 431, 432, 433, 434, 435, 436, 437, 438]'),
]
for src_name in [
    'create-four-hundred-fifty-three-minimal.py',
    'make-four-hundred-fifty-three.py',
    'create-four-hundred-fifty-three-files.py',
    'create-four-hundred-fifty-three.py',
    'generate-validate-four-hundred-fifty-three.py',
    'validate-four-hundred-fifty-three-valid-list-cases.py',
    'validate-four-hundred-fifty-three-valid-mixed.py',
    'verify-four-hundred-fifty-three.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-three', 'four-hundred-fifty-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
