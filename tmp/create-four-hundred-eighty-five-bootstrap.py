#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-eight', 'four-hundred-eighty-five'),
    ('vierhonderdachtenvijftig', 'vierhonderdvijfentachtig'),
    ('all_cases[:443]', 'all_cases[:470]'),
    ('{UNKNOWN, TYPO}][:443]', '{UNKNOWN, TYPO}][:470]'),
    ('!= 443', '!= 470'),
    ('kreeg 443', 'kreeg 470'),
    (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]'),
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
    dst = root / src_name.replace('four-hundred-fifty-eight', 'four-hundred-eighty-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
