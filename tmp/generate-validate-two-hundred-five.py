#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-four', 'two-hundred-five'),
    ('tweehonderdvier', 'tweehonderdvijf'),
    ('203', '204'),
    ('196, 197, 198, 199, 200, 201]', '196, 197, 198, 199, 200, 201, 202]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-four-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-five-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
