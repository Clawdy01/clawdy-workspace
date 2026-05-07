#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-one', 'three-hundred-two'),
    ('driehonderdeen', 'driehonderdtwee'),
    ('[:297]', '[:298]'),
    ('!= 297', '!= 298'),
    (' 290, 291, 292, 293, 294, 295, 296]', ' 290, 291, 292, 293, 294, 295, 296, 297]'),
]

for name in (
    'generate-validate-three-hundred-one.py',
    'validate-three-hundred-one-valid-list-cases.py',
    'validate-three-hundred-one-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-one', 'three-hundred-two')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
