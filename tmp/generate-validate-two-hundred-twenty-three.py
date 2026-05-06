#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-two', 'two-hundred-twenty-three'),
    ('tweehonderdtweeëntwintig', 'tweehonderddrieëntwintig'),
    ('221', '222'),
    ('215, 216, 217, 218, 219]', '215, 216, 217, 218, 219, 220]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
