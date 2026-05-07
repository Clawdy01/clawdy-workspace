#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ninety-three', 'two-hundred-ninety-four'),
    ('tweehonderddrieënnegentig', 'tweehonderdvierennegentig'),
    ('[:289]', '[:290]'),
    ('!= 289', '!= 290'),
    (' 283, 284, 285, 286, 287, 288]', ' 283, 284, 285, 286, 287, 288, 289]'),
]

for name in (
    'generate-validate-two-hundred-ninety-three.py',
    'validate-two-hundred-ninety-three-valid-list-cases.py',
    'validate-two-hundred-ninety-three-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-ninety-three', 'two-hundred-ninety-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
