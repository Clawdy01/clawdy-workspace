#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-sixty-two'),
    ('driehonderdeenenzestig', 'driehonderdtweeënzestig'),
    ('353, 354, 355]', '353, 354, 355, 356]'),
]

for name in (
    'generate-validate-three-hundred-sixty-one.py',
    'validate-three-hundred-sixty-one-valid-list-cases.py',
    'validate-three-hundred-sixty-one-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-one', 'three-hundred-sixty-two')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
