#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-four', 'two-hundred-thirty-five'),
    ('tweehonderdvierendertig', 'tweehonderdvijfendertig'),
    ('[:232]', '[:233]'),
    ('!= 232', '!= 233'),
    (' 227, 228, 229, 230, 231]', ' 227, 228, 229, 230, 231, 232]'),
    ('all_cases[:232]', 'all_cases[:233]'),
    ('{UNKNOWN, TYPO}][:232]', '{UNKNOWN, TYPO}][:233]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-four.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-five.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-four-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-five-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
