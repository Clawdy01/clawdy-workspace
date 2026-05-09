#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-three', 'three-hundred-fifty-five'),
    ('driehonderddrieënvijftig', 'driehonderdvijfenvijftig'),
    ('[:349]', '[:351]'),
    ('!= 349', '!= 351'),
    (' 342, 343, 344, 345, 346, 347, 348]', ' 342, 343, 344, 345, 346, 347, 348, 349, 350]'),
]

for name in (
    'generate-validate-three-hundred-fifty-three.py',
    'validate-three-hundred-fifty-three-valid-list-cases.py',
    'validate-three-hundred-fifty-three-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-three', 'three-hundred-fifty-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
