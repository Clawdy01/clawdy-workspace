#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-seven', 'one-hundred-sixty-eight'),
    ('honderdzevenenzestig', 'honderdachtenzestig'),
    ('167', '168'),
    ('160, 161, 162, 163, 164, 165, 166]', '160, 161, 162, 163, 164, 165, 166, 167]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
