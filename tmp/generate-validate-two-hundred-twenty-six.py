#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-five', 'two-hundred-twenty-six'),
    ('tweehonderdvijfentwintig', 'tweehonderdzesentwintig'),
    ('223', '224'),
    ('216, 217, 218, 219, 220, 221, 222]', '216, 217, 218, 219, 220, 221, 222, 223]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-five-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
