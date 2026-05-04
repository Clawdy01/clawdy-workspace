#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-nine', 'one-hundred-thirty'),
    ('honderdnegenentwintig', 'honderddertig'),
    ('129', '130'),
    ('126, 127, 128]', '126, 127, 128, 129]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-thirty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
