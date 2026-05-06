#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-fifteen', 'two-hundred-sixteen'),
    ('tweehonderdvijftien', 'tweehonderdzestien'),
    ('214', '215'),
    ('209, 210, 211, 212]', '209, 210, 211, 212, 213]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-fifteen-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-sixteen-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
