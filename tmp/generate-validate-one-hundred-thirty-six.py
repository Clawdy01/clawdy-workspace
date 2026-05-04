#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty-five', 'one-hundred-thirty-six'),
    ('honderdvijfendertig', 'honderdzesendertig'),
    ('135', '136'),
    ('131, 132, 133, 134]', '131, 132, 133, 134, 135]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-five-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
