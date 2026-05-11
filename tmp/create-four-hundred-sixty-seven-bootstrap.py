#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-eight', 'four-hundred-sixty-seven'),
    ('vierhonderdachtenvijftig', 'vierhonderdzevenenzestig'),
    ('all_cases[:443]', 'all_cases[:452]'),
    ('{UNKNOWN, TYPO}][:443]', '{UNKNOWN, TYPO}][:452]'),
    ('!= 443', '!= 452'),
    ('kreeg 443', 'kreeg 452'),
    (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444]'),
]
for src_name in [
    'create-four-hundred-fifty-eight-minimal.py',
    'make-four-hundred-fifty-eight.py',
    'create-four-hundred-fifty-eight-files.py',
    'create-four-hundred-fifty-eight.py',
    'generate-validate-four-hundred-fifty-eight.py',
    'validate-four-hundred-fifty-eight-valid-list-cases.py',
    'validate-four-hundred-fifty-eight-valid-mixed.py',
    'verify-four-hundred-fifty-eight.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-eight', 'four-hundred-sixty-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
