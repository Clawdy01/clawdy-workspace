#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-three', 'three-hundred-four'),
    ('driehonderddrie', 'driehonderdvier'),
    ('[:299]', '[:300]'),
    ('!= 299', '!= 300'),
    (' 290, 291, 292, 293, 294, 295, 296, 297, 298]', ' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299]'),
]

for name in (
    'generate-validate-three-hundred-three.py',
    'validate-three-hundred-three-valid-list-cases.py',
    'validate-three-hundred-three-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-three', 'three-hundred-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
