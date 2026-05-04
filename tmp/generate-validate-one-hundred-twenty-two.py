#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-one', 'one-hundred-twenty-two'),
    ('honderdeenentwintig', 'honderdtweeëntwintig'),
    ('121', '122'),
    ('120]', '120, 121]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
