#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty-one', 'one-hundred-thirty-two'),
    ('honderdeenendertig', 'honderdtweeëndertig'),
    ('131', '132'),
    ('128, 129, 130]', '128, 129, 130, 131]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
