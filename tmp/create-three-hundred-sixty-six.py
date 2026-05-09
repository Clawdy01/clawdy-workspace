#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-five', 'three-hundred-sixty-six'),
    ('driehonderdvijfenzestig', 'driehonderdzesenzestig'),
    ('all_cases[:360]', 'all_cases[:361]'),
    ('{UNKNOWN, TYPO}][:360]', '{UNKNOWN, TYPO}][:361]'),
    ('!= 360', '!= 361'),
    ('354, 355, 356, 357, 358, 359]', '354, 355, 356, 357, 358, 359, 360]'),
]

for name in (
    'generate-validate-three-hundred-sixty-five.py',
    'validate-three-hundred-sixty-five-valid-list-cases.py',
    'validate-three-hundred-sixty-five-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-five', 'three-hundred-sixty-six')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
