#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-one', 'one-hundred-ninety-two'),
    ('honderdeenennegentig', 'honderdtweeënnegentig'),
    ('190', '191'),
    ('181, 182, 183, 184, 185, 186, 187, 188]', '181, 182, 183, 184, 185, 186, 187, 188, 189]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
