#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-two', 'one-hundred-twenty-three'),
    ('honderdtweeëntwintig', 'honderddrieëntwintig'),
    ('122', '123'),
    ('120, 121]', '120, 121, 122]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
