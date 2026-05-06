#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-nine', 'two-hundred-thirty-three'),
    ('tweehonderdnegenentwintig', 'tweehonderddrieëndertig'),
    ('[:227]', '[:231]'),
    ('!= 227', '!= 231'),
    (' 226]', ' 226, 227, 228, 229, 230]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
