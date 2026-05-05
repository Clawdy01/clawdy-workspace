#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-three', 'one-hundred-ninety-four'),
    ('honderddrieënnegentig', 'honderdvierennegentig'),
    ('192', '193'),
    ('181, 182, 183, 184, 185, 186, 187, 188, 189, 190]', '181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-three-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
