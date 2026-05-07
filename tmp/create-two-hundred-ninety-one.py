#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ninety', 'two-hundred-ninety-one'),
    ('tweehonderdnegentig', 'tweehonderdeenennegentig'),
    ('[:286]', '[:287]'),
    ('!= 286', '!= 287'),
    (' 283, 284, 285]', ' 283, 284, 285, 286]'),
]

for name in (
    'generate-validate-two-hundred-ninety.py',
    'validate-two-hundred-ninety-valid-list-cases.py',
    'validate-two-hundred-ninety-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-ninety', 'two-hundred-ninety-one')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
