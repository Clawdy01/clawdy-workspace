#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-five', 'three-hundred-six'),
    ('driehonderdvijf', 'driehonderdzes'),
    ('[:301]', '[:302]'),
    ('!= 301', '!= 302'),
    (' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300]', ' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301]'),
]

for name in (
    'generate-validate-three-hundred-five.py',
    'validate-three-hundred-five-valid-list-cases.py',
    'validate-three-hundred-five-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-five', 'three-hundred-six')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
