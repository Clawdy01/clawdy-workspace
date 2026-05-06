#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-fourteen', 'two-hundred-fifteen'),
    ('tweehonderdveertien', 'tweehonderdvijftien'),
    ('213', '214'),
    ('208, 209, 210, 211]', '208, 209, 210, 211, 212]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-fourteen-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-fifteen-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
