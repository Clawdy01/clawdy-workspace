#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-five', 'one-hundred-forty-six'),
    ('honderdvijfenveertig', 'honderdzesenveertig'),
    ('145', '146'),
    ('141, 142, 143, 144]', '141, 142, 143, 144, 145]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-five-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
