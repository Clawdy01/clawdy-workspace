#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-nineteen', 'two-hundred-twenty'),
    ('tweehonderdnegentien', 'tweehonderdtwintig'),
    ('218', '219'),
    ('215, 216]', '215, 216, 217]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-nineteen-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
