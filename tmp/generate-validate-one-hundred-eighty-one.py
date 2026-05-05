#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-eighty', 'one-hundred-eighty-one'),
    ('honderdtachtig', 'honderdeenentachtig'),
    ('180', '181'),
    ('178, 179]', '178, 179, 180]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-eighty-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-eighty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
