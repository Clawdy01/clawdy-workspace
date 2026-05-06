#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-eight', 'two-hundred-forty'),
    ('tweehonderdachtendertig', 'tweehonderdveertig'),
    ('[:236]', '[:238]'),
    ('!= 236', '!= 238'),
    (' 227, 228, 229, 230, 231, 232, 233, 234, 235]', ' 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237]'),
    ('all_cases[:236]', 'all_cases[:238]'),
    ('{UNKNOWN, TYPO}][:236]', '{UNKNOWN, TYPO}][:238]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-eight.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-forty.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-forty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
