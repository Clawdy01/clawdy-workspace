#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-five', 'four-hundred-fifty-seven'),
    ('vierhonderdvijfenvijftig', 'vierhonderdzevenenvijftig'),
    ('all_cases[:440]', 'all_cases[:442]'),
    ('{UNKNOWN, TYPO}][:440]', '{UNKNOWN, TYPO}][:442]'),
    ('!= 440', '!= 442'),
    ('kreeg 440', 'kreeg 442'),
    (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441]'),
]
for src_name in [
    'create-four-hundred-fifty-five-minimal.py',
    'make-four-hundred-fifty-five.py',
    'create-four-hundred-fifty-five-files.py',
    'create-four-hundred-fifty-five.py',
    'generate-validate-four-hundred-fifty-five.py',
    'validate-four-hundred-fifty-five-valid-list-cases.py',
    'validate-four-hundred-fifty-five-valid-mixed.py',
    'verify-four-hundred-fifty-five.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-five', 'four-hundred-fifty-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
