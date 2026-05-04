#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-three', 'one-hundred-twenty-four'),
    ('honderddrieëntwintig', 'honderdvierenentwintig'),
    ('123', '124'),
    ('121, 122]', '121, 122, 123]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
