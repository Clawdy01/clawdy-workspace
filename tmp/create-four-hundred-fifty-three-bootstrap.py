#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-two', 'four-hundred-fifty-three'),
    ('vierhonderdtweeënvijftig', 'vierhonderddrieënvijftig'),
    ('all_cases[:437]', 'all_cases[:438]'),
    ('{UNKNOWN, TYPO}][:437]', '{UNKNOWN, TYPO}][:438]'),
    ('!= 437', '!= 438'),
    ('kreeg 437', 'kreeg 438'),
    (', 428, 429, 430, 431, 432, 433, 434, 435, 436]', ', 428, 429, 430, 431, 432, 433, 434, 435, 436, 437]'),
]
for src_name in [
    'create-four-hundred-fifty-two-minimal.py',
    'make-four-hundred-fifty-two.py',
    'create-four-hundred-fifty-two-files.py',
    'create-four-hundred-fifty-two.py',
    'generate-validate-four-hundred-fifty-two.py',
    'validate-four-hundred-fifty-two-valid-list-cases.py',
    'validate-four-hundred-fifty-two-valid-mixed.py',
    'verify-four-hundred-fifty-two.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-two', 'four-hundred-fifty-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
