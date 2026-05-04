#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-eight', 'one-hundred-twenty-nine'),
    ('honderdachtentwintig', 'honderdnegenentwintig'),
    ('128', '129'),
    ('125, 126, 127]', '125, 126, 127, 128]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
