#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty-six', 'one-hundred-thirty-seven'),
    ('honderdzesendertig', 'honderdzevenendertig'),
    ('136', '137'),
    ('132, 133, 134, 135]', '132, 133, 134, 135, 136]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-six-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
