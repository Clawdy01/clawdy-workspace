#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-three', 'one-hundred-fifty-four'),
    ('honderddrieënvijftig', 'honderdvierenvijftig'),
    ('153', '154'),
    ('149, 150, 151, 152]', '149, 150, 151, 152, 153]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
