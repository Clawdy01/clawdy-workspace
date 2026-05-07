#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ninety-four', 'two-hundred-ninety-five'),
    ('tweehonderdvierennegentig', 'tweehonderdvijfennegentig'),
    ('[:290]', '[:291]'),
    ('!= 290', '!= 291'),
    (' 283, 284, 285, 286, 287, 288, 289]', ' 283, 284, 285, 286, 287, 288, 289, 290]'),
]

for name in (
    'generate-validate-two-hundred-ninety-four.py',
    'validate-two-hundred-ninety-four-valid-list-cases.py',
    'validate-two-hundred-ninety-four-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-ninety-four', 'two-hundred-ninety-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
