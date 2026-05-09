#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-four', 'three-hundred-sixty-five'),
    ('driehonderdvierenzestig', 'driehonderdvijfenzestig'),
    ('all_cases[:359]', 'all_cases[:360]'),
    ('{UNKNOWN, TYPO}][:359]', '{UNKNOWN, TYPO}][:360]'),
    ('!= 359', '!= 360'),
    ('354, 355, 356, 357, 358]', '354, 355, 356, 357, 358, 359]'),
]

for name in (
    'generate-validate-three-hundred-sixty-four.py',
    'validate-three-hundred-sixty-four-valid-list-cases.py',
    'validate-three-hundred-sixty-four-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-four', 'three-hundred-sixty-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
