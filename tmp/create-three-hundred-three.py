#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-two', 'three-hundred-three'),
    ('driehonderdtwee', 'driehonderddrie'),
    ('[:298]', '[:299]'),
    ('!= 298', '!= 299'),
    (' 290, 291, 292, 293, 294, 295, 296, 297]', ' 290, 291, 292, 293, 294, 295, 296, 297, 298]'),
]

for name in (
    'generate-validate-three-hundred-two.py',
    'validate-three-hundred-two-valid-list-cases.py',
    'validate-three-hundred-two-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-two', 'three-hundred-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
