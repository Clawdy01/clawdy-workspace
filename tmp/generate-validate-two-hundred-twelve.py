#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-eleven', 'two-hundred-twelve'),
    ('tweehonderdelf', 'tweehonderdtwaalf'),
    ('210', '211'),
    ('207, 208]', '207, 208, 209]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-eleven-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-twelve-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
