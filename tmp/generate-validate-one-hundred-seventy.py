#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-nine', 'one-hundred-seventy'),
    ('honderdnegenenzestig', 'honderdzeventig'),
    ('169', '170'),
    ('161, 162, 163, 164, 165, 166, 167, 168]', '161, 162, 163, 164, 165, 166, 167, 168, 169]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
