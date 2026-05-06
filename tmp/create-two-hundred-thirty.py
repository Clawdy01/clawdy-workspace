#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-nine', 'two-hundred-thirty'),
    ('tweehonderdnegenentwintig', 'tweehonderddertig'),
    ('[:227]', '[:228]'),
    ('!= 227', '!= 228'),
    (' 226]', ' 226, 227]'),
    ('all_cases[:227]', 'all_cases[:228]'),
    ('[:227]', '[:228]'),
    ('{UNKNOWN, TYPO}][:227]', '{UNKNOWN, TYPO}][:228]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-twenty-nine.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
