#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixteen', 'three-hundred-seventeen'),
    ('driehonderdzestien', 'driehonderdzeventien'),
    ('[:312]', '[:313]'),
    ('!= 312', '!= 313'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312]'),
]

for name in (
    'generate-validate-three-hundred-sixteen.py',
    'validate-three-hundred-sixteen-valid-list-cases.py',
    'validate-three-hundred-sixteen-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixteen', 'three-hundred-seventeen')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
