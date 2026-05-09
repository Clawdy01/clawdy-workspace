#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty', 'three-hundred-fifty-one'),
    ('driehonderdvijftig', 'driehonderdeenenvijftig'),
    ('[:346]', '[:347]'),
    ('!= 346', '!= 347'),
    (' 342, 343, 344, 345]', ' 342, 343, 344, 345, 346]'),
]

for name in (
    'generate-validate-three-hundred-fifty.py',
    'validate-three-hundred-fifty-valid-list-cases.py',
    'validate-three-hundred-fifty-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty', 'three-hundred-fifty-one')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
