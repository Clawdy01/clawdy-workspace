#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-five', 'two-hundred-thirty-six'),
    ('tweehonderdvijfendertig', 'tweehonderdzesendertig'),
    ('[:233]', '[:234]'),
    ('!= 233', '!= 234'),
    (' 227, 228, 229, 230, 231, 232]', ' 227, 228, 229, 230, 231, 232, 233]'),
    ('all_cases[:233]', 'all_cases[:234]'),
    ('{UNKNOWN, TYPO}][:233]', '{UNKNOWN, TYPO}][:234]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-five.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-six.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-five-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
