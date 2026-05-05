#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-one', 'two-hundred-two'),
    ('tweehonderdéén', 'tweehonderdtwee'),
    ('200', '201'),
    ('193, 194, 195, 196, 197, 198]', '193, 194, 195, 196, 197, 198, 199]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-one-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
