#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-thirteen', 'three-hundred-fourteen'),
    ('driehonderddertien', 'driehonderdveertien'),
    ('[:309]', '[:310]'),
    ('!= 309', '!= 310'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309]'),
]

for name in (
    'generate-validate-three-hundred-thirteen.py',
    'validate-three-hundred-thirteen-valid-list-cases.py',
    'validate-three-hundred-thirteen-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-thirteen', 'three-hundred-fourteen')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
