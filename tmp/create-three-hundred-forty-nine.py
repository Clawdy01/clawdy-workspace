#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-forty-eight', 'three-hundred-forty-nine'),
    ('driehonderdachtenveertig', 'driehonderdnegenenveertig'),
    ('[:344]', '[:345]'),
    ('!= 344', '!= 345'),
    (' 341, 342, 343]', ' 341, 342, 343, 344]'),
]

for name in (
    'generate-validate-three-hundred-forty-eight.py',
    'validate-three-hundred-forty-eight-valid-list-cases.py',
    'validate-three-hundred-forty-eight-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-forty-eight', 'three-hundred-forty-nine')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
