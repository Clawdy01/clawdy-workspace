#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-eight', 'two-hundred-twenty-nine'),
    ('tweehonderdachtentwintig', 'tweehonderdnegenentwintig'),
    ('[:226]', '[:227]'),
    ('!= 226', '!= 227'),
    (' 225]', ' 225, 226]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-twenty-eight.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-twenty-nine.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twenty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
