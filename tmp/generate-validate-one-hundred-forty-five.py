#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-four', 'one-hundred-forty-five'),
    ('honderdvierenveertig', 'honderdvijfenveertig'),
    ('144', '145'),
    ('140, 141, 142, 143]', '140, 141, 142, 143, 144]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-four-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-five-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
