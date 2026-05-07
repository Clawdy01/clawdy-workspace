#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-eighty-nine', 'two-hundred-ninety'),
    ('tweehonderdnegenentachtig', 'tweehonderdnegentig'),
    ('[:285]', '[:286]'),
    ('!= 285', '!= 286'),
    (' 283, 284]', ' 283, 284, 285]'),
]

for name in (
    'generate-validate-two-hundred-eighty-nine.py',
    'validate-two-hundred-eighty-nine-valid-list-cases.py',
    'validate-two-hundred-eighty-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-eighty-nine', 'two-hundred-ninety')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
