#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-sixteen', 'two-hundred-seventeen'),
    ('tweehonderdzestien', 'tweehonderdzeventien'),
    ('215', '216'),
    ('210, 211, 212, 213]', '210, 211, 212, 213, 214]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-sixteen-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-seventeen-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
