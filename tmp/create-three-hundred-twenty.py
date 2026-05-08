#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-nineteen', 'three-hundred-twenty'),
    ('driehonderdnegentien', 'driehonderdtwintig'),
    ('[:315]', '[:316]'),
    ('!= 315', '!= 316'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315]'),
]

for name in (
    'generate-validate-three-hundred-nineteen.py',
    'validate-three-hundred-nineteen-valid-list-cases.py',
    'validate-three-hundred-nineteen-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-nineteen', 'three-hundred-twenty')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
