#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ninety-two', 'two-hundred-ninety-three'),
    ('tweehonderdtweeënnegentig', 'tweehonderddrieënnegentig'),
    ('[:288]', '[:289]'),
    ('!= 288', '!= 289'),
    (' 283, 284, 285, 286, 287]', ' 283, 284, 285, 286, 287, 288]'),
]

for name in (
    'generate-validate-two-hundred-ninety-two.py',
    'validate-two-hundred-ninety-two-valid-list-cases.py',
    'validate-two-hundred-ninety-two-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-ninety-two', 'two-hundred-ninety-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
