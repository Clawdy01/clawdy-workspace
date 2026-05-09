#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-four', 'three-hundred-fifty-six'),
    ('driehonderdvierenvijftig', 'driehonderdzesenvijftig'),
    ('[:350]', '[:352]'),
    ('!= 350', '!= 352'),
    (' 342, 343, 344, 345, 346, 347, 348, 349]', ' 342, 343, 344, 345, 346, 347, 348, 349, 350, 351]'),
]

for name in (
    'generate-validate-three-hundred-fifty-four.py',
    'validate-three-hundred-fifty-four-valid-list-cases.py',
    'validate-three-hundred-fifty-four-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-four', 'three-hundred-fifty-six')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
