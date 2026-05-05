#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-eight', 'one-hundred-sixty-nine'),
    ('honderdachtenzestig', 'honderdnegenenzestig'),
    ('168', '169'),
    ('160, 161, 162, 163, 164, 165, 166, 167]', '160, 161, 162, 163, 164, 165, 166, 167, 168]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
