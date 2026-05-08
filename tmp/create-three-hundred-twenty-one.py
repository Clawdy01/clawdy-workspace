#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-twenty', 'three-hundred-twenty-one'),
    ('driehonderdtwintig', 'driehonderdeenentwintig'),
    ('[:316]', '[:317]'),
    ('!= 316', '!= 317'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316]'),
]

for name in (
    'generate-validate-three-hundred-twenty.py',
    'validate-three-hundred-twenty-valid-list-cases.py',
    'validate-three-hundred-twenty-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-twenty', 'three-hundred-twenty-one')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
