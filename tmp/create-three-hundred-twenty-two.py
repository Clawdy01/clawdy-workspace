#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-twenty-one', 'three-hundred-twenty-two'),
    ('driehonderdeenentwintig', 'driehonderdtweeentwintig'),
    ('[:317]', '[:318]'),
    ('!= 317', '!= 318'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317]'),
]

for name in (
    'generate-validate-three-hundred-twenty-one.py',
    'validate-three-hundred-twenty-one-valid-list-cases.py',
    'validate-three-hundred-twenty-one-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-twenty-one', 'three-hundred-twenty-two')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
