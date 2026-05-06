#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-eight', 'two-hundred-thirty-nine'),
    ('tweehonderdachtendertig', 'tweehonderdnegenendertig'),
    ('[:236]', '[:237]'),
    ('!= 236', '!= 237'),
    (' 227, 228, 229, 230, 231, 232, 233, 234, 235]', ' 227, 228, 229, 230, 231, 232, 233, 234, 235, 236]'),
    ('all_cases[:236]', 'all_cases[:237]'),
    ('{UNKNOWN, TYPO}][:236]', '{UNKNOWN, TYPO}][:237]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-eight.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-nine.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
