#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-two', 'three-hundred-fifty-four'),
    ('driehonderdtweeënvijftig', 'driehonderdvierenvijftig'),
    ('[:348]', '[:350]'),
    ('!= 348', '!= 350'),
    (' 342, 343, 344, 345, 346, 347]', ' 342, 343, 344, 345, 346, 347, 348, 349]'),
]

for name in (
    'generate-validate-three-hundred-fifty-two.py',
    'validate-three-hundred-fifty-two-valid-list-cases.py',
    'validate-three-hundred-fifty-two-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-two', 'three-hundred-fifty-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
