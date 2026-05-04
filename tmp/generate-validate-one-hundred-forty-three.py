#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-two', 'one-hundred-forty-three'),
    ('honderdtweeënveertig', 'honderddrieënveertig'),
    ('142', '143'),
    ('138, 139, 140, 141]', '138, 139, 140, 141, 142]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
