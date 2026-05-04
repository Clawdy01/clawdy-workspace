#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-seven', 'one-hundred-twenty-eight'),
    ('honderdzevenentwintig', 'honderdachtentwintig'),
    ('127', '128'),
    ('124, 125, 126]', '124, 125, 126, 127]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
