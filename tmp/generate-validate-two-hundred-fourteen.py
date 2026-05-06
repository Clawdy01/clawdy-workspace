#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-thirteen', 'two-hundred-fourteen'),
    ('tweehonderddertien', 'tweehonderdveertien'),
    ('212', '213'),
    ('208, 209, 210]', '208, 209, 210, 211]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-thirteen-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-fourteen-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
