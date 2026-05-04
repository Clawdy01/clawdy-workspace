#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-seven', 'one-hundred-forty-eight'),
    ('honderdzevenenveertig', 'honderdachtenveertig'),
    ('147', '148'),
    ('145, 146]', '145, 146, 147]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
