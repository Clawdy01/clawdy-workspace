#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifty-six', 'three-hundred-fifty-eight'),
    ('driehonderdzesenvijftig', 'driehonderdachtenvijftig'),
    ('[:352]', '[:354]'),
    ('!= 352', '!= 354'),
    (' 342, 343, 344, 345, 346, 347, 348, 349, 350, 351]', ' 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353]'),
]

for name in (
    'generate-validate-three-hundred-fifty-six.py',
    'validate-three-hundred-fifty-six-valid-list-cases.py',
    'validate-three-hundred-fifty-six-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifty-six', 'three-hundred-fifty-eight')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
