#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-thirty-nine', 'one-hundred-forty'),
    ('honderdnegenendertig', 'honderdveertig'),
    ('139', '140'),
    ('137, 138]', '137, 138, 139]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-thirty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
