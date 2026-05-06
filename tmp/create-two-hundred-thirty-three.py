#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-two', 'two-hundred-thirty-three'),
    ('tweehonderdtweeëndertig', 'tweehonderddrieëndertig'),
    ('[:230]', '[:231]'),
    ('!= 230', '!= 231'),
    (' 227, 228, 229]', ' 227, 228, 229, 230]'),
    ('all_cases[:230]', 'all_cases[:231]'),
    ('{UNKNOWN, TYPO}][:230]', '{UNKNOWN, TYPO}][:231]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-two.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-three.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
