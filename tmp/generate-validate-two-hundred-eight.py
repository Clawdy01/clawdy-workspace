#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-seven', 'two-hundred-eight'),
    ('tweehonderdzeven', 'tweehonderdacht'),
    ('206', '207'),
    ('196, 197, 198, 199, 200, 201, 202, 203, 204]', '196, 197, 198, 199, 200, 201, 202, 203, 204, 205]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
