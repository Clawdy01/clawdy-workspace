#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-three', 'one-hundred-sixty-four'),
    ('honderddrieënzestig', 'honderdvierenzestig'),
    ('163', '164'),
    ('157, 158, 159, 160, 161, 162]', '157, 158, 159, 160, 161, 162, 163]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
