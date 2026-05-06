#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty', 'two-hundred-thirty-one'),
    ('tweehonderddertig', 'tweehonderdeenendertig'),
    ('[:228]', '[:229]'),
    ('!= 228', '!= 229'),
    (' 226, 227]', ' 226, 227, 228]'),
    ('all_cases[:228]', 'all_cases[:229]'),
    ('{UNKNOWN, TYPO}][:228]', '{UNKNOWN, TYPO}][:229]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-one.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
