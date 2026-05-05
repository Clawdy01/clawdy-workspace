#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-eight', 'one-hundred-ninety-nine'),
    ('honderdachtennegentig', 'honderdnegenennegentig'),
    ('197', '198'),
    ('191, 192, 193, 194, 195]', '191, 192, 193, 194, 195, 196]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
