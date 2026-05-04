#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-one', 'one-hundred-forty-two'),
    ('honderdeenenveertig', 'honderdtweeënveertig'),
    ('141', '142'),
    ('138, 139, 140]', '138, 139, 140, 141]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
