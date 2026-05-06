#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-nine', 'two-hundred-thirty-seven'),
    ('tweehonderdnegenentwintig', 'tweehonderdzevenendertig'),
    ('[:227]', '[:235]'),
    ('!= 227', '!= 235'),
    (' 226]', ' 226, 227, 228, 229, 230, 231, 232, 233, 234]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
