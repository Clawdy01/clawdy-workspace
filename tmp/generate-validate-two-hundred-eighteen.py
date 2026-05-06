#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-seventeen', 'two-hundred-eighteen'),
    ('tweehonderdzeventien', 'tweehonderdachttien'),
    ('216', '217'),
    ('210, 211, 212, 213, 214]', '210, 211, 212, 213, 214, 215]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-seventeen-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-eighteen-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
