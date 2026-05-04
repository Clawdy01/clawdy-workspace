#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-three', 'one-hundred-forty-four'),
    ('honderddrieënveertig', 'honderdvierenveertig'),
    ('143', '144'),
    ('139, 140, 141, 142]', '139, 140, 141, 142, 143]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-forty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
