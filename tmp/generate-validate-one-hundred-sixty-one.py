#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty', 'one-hundred-sixty-one'),
    ('honderdzestig', 'honderdeenenzestig'),
    ('160', '161'),
    ('155, 156, 157, 158, 159]', '155, 156, 157, 158, 159, 160]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
