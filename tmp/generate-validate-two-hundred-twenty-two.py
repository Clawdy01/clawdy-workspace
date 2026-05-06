#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-one', 'two-hundred-twenty-two'),
    ('tweehonderdeenentwintig', 'tweehonderdtweeëntwintig'),
    ('220', '221'),
    ('215, 216, 217, 218]', '215, 216, 217, 218, 219]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
