#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-three', 'two-hundred-four'),
    ('tweehonderddrie', 'tweehonderdvier'),
    ('202', '203'),
    ('195, 196, 197, 198, 199, 200]', '195, 196, 197, 198, 199, 200, 201]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-three-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
