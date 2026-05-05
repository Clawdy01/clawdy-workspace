#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy-three', 'one-hundred-seventy-four'),
    ('honderddrieënzeventig', 'honderdvierenzeventig'),
    ('173', '174'),
    ('170, 171, 172]', '170, 171, 172, 173]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
