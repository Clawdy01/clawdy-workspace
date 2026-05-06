#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-three', 'two-hundred-twenty-four'),
    ('tweehonderddrieëntwintig', 'tweehonderdvierentwintig'),
    ('222', '223'),
    ('216, 217, 218, 219, 220]', '216, 217, 218, 219, 220, 221]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
