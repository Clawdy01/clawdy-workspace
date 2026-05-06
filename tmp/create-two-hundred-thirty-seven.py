#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirty-six', 'two-hundred-thirty-seven'),
    ('tweehonderdzesendertig', 'tweehonderdzevenendertig'),
    ('[:234]', '[:235]'),
    ('!= 234', '!= 235'),
    (' 227, 228, 229, 230, 231, 232, 233]', ' 227, 228, 229, 230, 231, 232, 233, 234]'),
    ('all_cases[:234]', 'all_cases[:235]'),
    ('{UNKNOWN, TYPO}][:234]', '{UNKNOWN, TYPO}][:235]'),
]

src = root / 'tmp' / 'generate-validate-two-hundred-thirty-six.py'
dst = root / 'tmp' / 'generate-validate-two-hundred-thirty-seven.py'
text = src.read_text()
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirty-six-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirty-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
