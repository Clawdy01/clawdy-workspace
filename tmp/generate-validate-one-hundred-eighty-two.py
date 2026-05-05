#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-eighty-one', 'one-hundred-eighty-two'),
    ('honderdeenentachtig', 'honderdtweeëntachtig'),
    ('181', '182'),
    ('179, 180]', '179, 180, 181]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-eighty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-eighty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
