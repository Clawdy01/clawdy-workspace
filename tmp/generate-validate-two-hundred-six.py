#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-five', 'two-hundred-six'),
    ('tweehonderdvijf', 'tweehonderdzes'),
    ('204', '205'),
    ('196, 197, 198, 199, 200, 201, 202]', '196, 197, 198, 199, 200, 201, 202, 203]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-five-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
