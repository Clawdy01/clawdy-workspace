#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-four', 'one-hundred-sixty-five'),
    ('honderdvierenzestig', 'honderdvijfenzestig'),
    ('164', '165'),
    ('157, 158, 159, 160, 161, 162, 163]', '157, 158, 159, 160, 161, 162, 163, 164]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-four-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-five-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
