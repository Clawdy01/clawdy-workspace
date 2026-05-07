#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred', 'three-hundred-one'),
    ('driehonderd', 'driehonderdeen'),
    ('[:296]', '[:297]'),
    ('!= 296', '!= 297'),
    (' 290, 291, 292, 293, 294, 295]', ' 290, 291, 292, 293, 294, 295, 296]'),
]

for name in (
    'generate-validate-three-hundred.py',
    'validate-three-hundred-valid-list-cases.py',
    'validate-three-hundred-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred', 'three-hundred-one')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
