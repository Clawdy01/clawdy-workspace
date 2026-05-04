#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-six', 'one-hundred-twenty-seven'),
    ('honderdzesentwintig', 'honderdzevenentwintig'),
    ('126', '127'),
    ('124, 125]', '124, 125, 126]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-six-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
