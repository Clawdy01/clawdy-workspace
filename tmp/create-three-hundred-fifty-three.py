#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-one', 'three-hundred-fifty-three'),
    ('driehonderdeenenvijftig', 'driehonderddrieënvijftig'),
    ('[:347]', '[:349]'),
    ('!= 347', '!= 349'),
    (' 342, 343, 344, 345, 346]', ' 342, 343, 344, 345, 346, 347, 348]'),
]

for name in (
    'generate-validate-three-hundred-fifty-one.py',
    'validate-three-hundred-fifty-one-valid-list-cases.py',
    'validate-three-hundred-fifty-one-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-one', 'three-hundred-fifty-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
