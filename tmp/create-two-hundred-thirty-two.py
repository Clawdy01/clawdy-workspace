#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-one', 'two-hundred-thirty-two'),
    ('tweehonderdeenendertig', 'tweehonderdtweeëndertig'),
    ('[:229]', '[:230]'),
    ('!= 229', '!= 230'),
    (' 226, 227, 228]', ' 226, 227, 228, 229]'),
    ('all_cases[:229]', 'all_cases[:230]'),
    ('{UNKNOWN, TYPO}][:229]', '{UNKNOWN, TYPO}][:230]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-one.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-two.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
