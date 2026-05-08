#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-eighteen', 'three-hundred-nineteen'),
    ('driehonderdachttien', 'driehonderdnegentien'),
    ('[:314]', '[:315]'),
    ('!= 314', '!= 315'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314]'),
]

for name in (
    'generate-validate-three-hundred-eighteen.py',
    'validate-three-hundred-eighteen-valid-list-cases.py',
    'validate-three-hundred-eighteen-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-eighteen', 'three-hundred-nineteen')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
