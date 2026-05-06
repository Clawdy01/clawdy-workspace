#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ten', 'two-hundred-eleven'),
    ('tweehonderdtien', 'tweehonderdelf'),
    ('209', '210'),
    ('206, 207]', '206, 207, 208]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-ten-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-eleven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
