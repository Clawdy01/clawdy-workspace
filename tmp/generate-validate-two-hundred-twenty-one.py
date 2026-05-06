#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty', 'two-hundred-twenty-one'),
    ('tweehonderdtwintig', 'tweehonderdeenentwintig'),
    ('219', '220'),
    ('215, 216, 217]', '215, 216, 217, 218]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
