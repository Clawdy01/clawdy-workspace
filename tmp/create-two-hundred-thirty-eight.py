#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-seven', 'two-hundred-thirty-eight'),
    ('tweehonderdzevenendertig', 'tweehonderdachtendertig'),
    ('[:235]', '[:236]'),
    ('!= 235', '!= 236'),
    (' 227, 228, 229, 230, 231, 232, 233, 234]', ' 227, 228, 229, 230, 231, 232, 233, 234, 235]'),
    ('all_cases[:235]', 'all_cases[:236]'),
    ('{UNKNOWN, TYPO}][:235]', '{UNKNOWN, TYPO}][:236]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-seven.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-eight.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
