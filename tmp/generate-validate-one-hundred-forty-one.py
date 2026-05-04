#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty', 'one-hundred-forty-one'),
    ('honderdveertig', 'honderdeenenveertig'),
    ('140', '141'),
    ('137, 138, 139]', '137, 138, 139, 140]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
