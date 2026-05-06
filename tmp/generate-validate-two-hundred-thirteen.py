#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twelve', 'two-hundred-thirteen'),
    ('tweehonderdtwaalf', 'tweehonderddertien'),
    ('211', '212'),
    ('208, 209]', '208, 209, 210]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twelve-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-thirteen-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
