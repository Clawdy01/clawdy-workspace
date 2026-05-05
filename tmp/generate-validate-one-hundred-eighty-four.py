#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-eighty-three', 'one-hundred-eighty-four'),
    ('honderddrieëntachtig', 'honderdvierentachtig'),
    ('183', '184'),
    ('181, 182]', '181, 182, 183]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-eighty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-eighty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
