#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-eighty-eight', 'one-hundred-eighty-nine'),
    ('honderdachtentachtig', 'honderdnegenentachtig'),
    ('187', '188'),
    ('180, 181, 182, 183, 184, 185]', '180, 181, 182, 183, 184, 185, 186]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-eighty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-eighty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
