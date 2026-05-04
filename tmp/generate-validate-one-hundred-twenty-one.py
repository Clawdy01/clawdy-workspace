#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty', 'one-hundred-twenty-one'),
    ('honderdtwintig', 'honderdeenentwintig'),
    ('120', '121'),
    ('119]', '119, 120]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
