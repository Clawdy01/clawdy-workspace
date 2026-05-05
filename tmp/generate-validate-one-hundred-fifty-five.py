#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-four', 'one-hundred-fifty-five'),
    ('honderdvierenvijftig', 'honderdvijfenvijftig'),
    ('154', '155'),
    ('150, 151, 152, 153]', '150, 151, 152, 153, 154]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-four-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-five-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
