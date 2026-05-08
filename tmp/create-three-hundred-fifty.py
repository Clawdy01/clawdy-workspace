#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-forty-nine', 'three-hundred-fifty'),
    ('driehonderdnegenenveertig', 'driehonderdvijftig'),
    ('[:345]', '[:346]'),
    ('!= 345', '!= 346'),
    (' 342, 343, 344]', ' 342, 343, 344, 345]'),
]

for name in (
    'generate-validate-three-hundred-forty-nine.py',
    'validate-three-hundred-forty-nine-valid-list-cases.py',
    'validate-three-hundred-forty-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-forty-nine', 'three-hundred-fifty')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
