#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty', 'one-hundred-thirty-one'),
    ('honderddertig', 'honderdeenendertig'),
    ('130', '131'),
    ('127, 128, 129]', '127, 128, 129, 130]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
