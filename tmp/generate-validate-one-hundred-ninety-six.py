#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-five', 'one-hundred-ninety-six'),
    ('honderdvijfennegentig', 'honderdzesennegentig'),
    ('194', '195'),
    ('181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192]', '181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-five-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
