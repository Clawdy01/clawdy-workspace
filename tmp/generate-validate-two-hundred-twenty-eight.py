#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-seven', 'two-hundred-twenty-eight'),
    ('tweehonderdzevenentwintig', 'tweehonderdachtentwintig'),
    ('225', '226'),
    ('216, 217, 218, 219, 220, 221, 222, 223, 224]', '216, 217, 218, 219, 220, 221, 222, 223, 224, 225]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
