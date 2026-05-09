#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-five', 'three-hundred-fifty-seven'),
    ('driehonderdvijfenvijftig', 'driehonderdzevenenvijftig'),
    ('[:351]', '[:353]'),
    ('!= 351', '!= 353'),
    (' 342, 343, 344, 345, 346, 347, 348, 349, 350]', ' 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352]'),
]

for name in (
    'generate-validate-three-hundred-fifty-five.py',
    'validate-three-hundred-fifty-five-valid-list-cases.py',
    'validate-three-hundred-fifty-five-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-five', 'three-hundred-fifty-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
