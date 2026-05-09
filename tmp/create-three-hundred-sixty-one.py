#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty', 'three-hundred-sixty-one'),
    ('driehonderdzestig', 'driehonderdeenenzestig'),
    ('353, 354]', '353, 354, 355]'),
]

for name in (
    'generate-validate-three-hundred-sixty.py',
    'validate-three-hundred-sixty-valid-list-cases.py',
    'validate-three-hundred-sixty-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty', 'three-hundred-sixty-one')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
