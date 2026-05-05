#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-seven', 'one-hundred-ninety-eight'),
    ('honderdzevenennegentig', 'honderdachtennegentig'),
    ('196', '197'),
    ('191, 192, 193, 194]', '191, 192, 193, 194, 195]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
