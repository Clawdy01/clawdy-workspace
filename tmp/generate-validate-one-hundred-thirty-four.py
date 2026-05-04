#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty-three', 'one-hundred-thirty-four'),
    ('honderddrieëndertig', 'honderdvierendertig'),
    ('133', '134'),
    ('130, 131, 132]', '130, 131, 132, 133]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
