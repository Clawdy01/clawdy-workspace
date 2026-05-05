#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred', 'two-hundred-one'),
    ('tweehonderd', 'tweehonderdéén'),
    ('199', '200'),
    ('192, 193, 194, 195, 196, 197]', '192, 193, 194, 195, 196, 197, 198]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
