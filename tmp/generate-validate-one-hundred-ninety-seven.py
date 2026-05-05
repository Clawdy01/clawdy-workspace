#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-six', 'one-hundred-ninety-seven'),
    ('honderdzesennegentig', 'honderdzevenennegentig'),
    ('195', '196'),
    ('191, 192, 193]', '191, 192, 193, 194]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-six-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
