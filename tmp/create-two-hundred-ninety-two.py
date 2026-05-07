#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ninety-one', 'two-hundred-ninety-two'),
    ('tweehonderdeenennegentig', 'tweehonderdtweeënnegentig'),
    ('[:287]', '[:288]'),
    ('!= 287', '!= 288'),
    (' 283, 284, 285, 286]', ' 283, 284, 285, 286, 287]'),
]

for name in (
    'generate-validate-two-hundred-ninety-one.py',
    'validate-two-hundred-ninety-one-valid-list-cases.py',
    'validate-two-hundred-ninety-one-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-ninety-one', 'two-hundred-ninety-two')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
