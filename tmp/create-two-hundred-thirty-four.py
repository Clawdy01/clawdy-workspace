#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-three', 'two-hundred-thirty-four'),
    ('tweehonderddrieëndertig', 'tweehonderdvierendertig'),
    ('[:231]', '[:232]'),
    ('!= 231', '!= 232'),
    (' 227, 228, 229, 230]', ' 227, 228, 229, 230, 231]'),
    ('all_cases[:231]', 'all_cases[:232]'),
    ('{UNKNOWN, TYPO}][:231]', '{UNKNOWN, TYPO}][:232]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-three.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-four.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
