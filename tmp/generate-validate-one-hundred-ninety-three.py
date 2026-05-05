#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-two', 'one-hundred-ninety-three'),
    ('honderdtweeënnegentig', 'honderddrieënnegentig'),
    ('191', '192'),
    ('181, 182, 183, 184, 185, 186, 187, 188, 189]', '181, 182, 183, 184, 185, 186, 187, 188, 189, 190]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-two-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
