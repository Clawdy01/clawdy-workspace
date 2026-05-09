#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-six', 'three-hundred-sixty-seven'),
    ('driehonderdzesenzestig', 'driehonderdzevenenzestig'),
    ('all_cases[:361]', 'all_cases[:362]'),
    ('{UNKNOWN, TYPO}][:361]', '{UNKNOWN, TYPO}][:362]'),
    ('!= 361', '!= 362'),
    ('355, 356, 357, 358, 359, 360]', '355, 356, 357, 358, 359, 360, 361]'),
]

for name in (
    'generate-validate-three-hundred-sixty-six.py',
    'validate-three-hundred-sixty-six-valid-list-cases.py',
    'validate-three-hundred-sixty-six-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-six', 'three-hundred-sixty-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
