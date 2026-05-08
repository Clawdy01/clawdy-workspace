#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-twelve', 'three-hundred-thirteen'),
    ('driehonderdtwaalf', 'driehonderddertien'),
    ('[:308]', '[:309]'),
    ('!= 308', '!= 309'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308]'),
]

for name in (
    'generate-validate-three-hundred-twelve.py',
    'validate-three-hundred-twelve-valid-list-cases.py',
    'validate-three-hundred-twelve-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-twelve', 'three-hundred-thirteen')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
