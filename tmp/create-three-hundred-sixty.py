#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-nine', 'three-hundred-sixty'),
    ('driehonderdnegenenvijftig', 'driehonderdzestig'),
    ('353]', '353, 354]'),
]

for name in (
    'generate-validate-three-hundred-fifty-nine.py',
    'validate-three-hundred-fifty-nine-valid-list-cases.py',
    'validate-three-hundred-fifty-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-nine', 'three-hundred-sixty')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
