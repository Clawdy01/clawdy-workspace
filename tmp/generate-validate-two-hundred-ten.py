#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-nine', 'two-hundred-ten'),
    ('tweehonderdnegen', 'tweehonderdtien'),
    ('208', '209'),
    ('196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206]', '196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-ten-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
