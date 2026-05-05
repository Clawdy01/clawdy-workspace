#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-eighty-nine', 'one-hundred-ninety'),
    ('honderdnegenentachtig', 'honderdnegentig'),
    ('188', '189'),
    ('180, 181, 182, 183, 184, 185, 186]', '180, 181, 182, 183, 184, 185, 186, 187]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-eighty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
