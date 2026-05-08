#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-four', 'three-hundred-five'),
    ('driehonderdvier', 'driehonderdvijf'),
    ('[:300]', '[:301]'),
    ('!= 300', '!= 301'),
    (' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299]', ' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300]'),
]

for name in (
    'generate-validate-three-hundred-four.py',
    'validate-three-hundred-four-valid-list-cases.py',
    'validate-three-hundred-four-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-four', 'three-hundred-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
