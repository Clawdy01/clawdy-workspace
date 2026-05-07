#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-eighty-eight', 'two-hundred-eighty-nine'),
    ('tweehonderdachtentachtig', 'tweehonderdnegenentachtig'),
    ('[:284]', '[:285]'),
    ('!= 284', '!= 285'),
    (' 283]', ' 283, 284]'),
]

for name in (
    'generate-validate-two-hundred-eighty-eight.py',
    'validate-two-hundred-eighty-eight-valid-list-cases.py',
    'validate-two-hundred-eighty-eight-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-eighty-eight', 'two-hundred-eighty-nine')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
