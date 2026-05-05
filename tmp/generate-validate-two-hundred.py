#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-nine', 'two-hundred'),
    ('honderdnegenennegentig', 'tweehonderd'),
    ('198', '199'),
    ('191, 192, 193, 194, 195, 196]', '191, 192, 193, 194, 195, 196, 197]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
