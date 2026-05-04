#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty-two', 'one-hundred-thirty-three'),
    ('honderdtweeëndertig', 'honderddrieëndertig'),
    ('132', '133'),
    ('129, 130, 131]', '129, 130, 131, 132]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
