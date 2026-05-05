#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy-six', 'one-hundred-seventy-seven'),
    ('honderdzesenzeventig', 'honderdzevenenzeventig'),
    ('176', '177'),
    ('172, 173, 174, 175]', '172, 173, 174, 175, 176]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-six-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
