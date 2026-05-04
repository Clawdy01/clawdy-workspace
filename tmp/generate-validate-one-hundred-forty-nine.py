#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-eight', 'one-hundred-forty-nine'),
    ('honderdachtenveertig', 'honderdnegenenveertig'),
    ('148', '149'),
    ('145, 146, 147]', '145, 146, 147, 148]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
