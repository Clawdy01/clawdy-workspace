#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-seven', 'three-hundred-fifty-nine'),
    ('driehonderdzevenenvijftig', 'driehonderdnegenenvijftig'),
    ('[:353]', '[:355]'),
    ('!= 353', '!= 355'),
    (' 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352]', ' 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354]'),
]

for name in (
    'generate-validate-three-hundred-fifty-seven.py',
    'validate-three-hundred-fifty-seven-valid-list-cases.py',
    'validate-three-hundred-fifty-seven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-seven', 'three-hundred-fifty-nine')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
