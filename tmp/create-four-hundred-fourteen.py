#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-nine', 'four-hundred-fourteen'),
    ('driehonderdnegenenzestig', 'vierhonderdveertien'),
    ('all_cases[:364]', 'all_cases[:401]'),
    ('{UNKNOWN, TYPO}][:364]', '{UNKNOWN, TYPO}][:401]'),
    ('!= 364', '!= 401'),
    ('356, 357, 358, 359, 360, 361, 362, 363]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]'),
]

for name in (
    'generate-validate-three-hundred-sixty-nine.py',
    'validate-three-hundred-sixty-nine-valid-list-cases.py',
    'validate-three-hundred-sixty-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-nine', 'four-hundred-fourteen')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
