#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-ninety-four', 'three-hundred'),
    ('tweehonderdvierennegentig', 'driehonderd'),
    ('[:290]', '[:296]'),
    ('!= 290', '!= 296'),
    (' 283, 284, 285, 286, 287, 288, 289]', ' 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295]'),
]

for name in (
    'generate-validate-two-hundred-ninety-five.py',
    'validate-two-hundred-ninety-five-valid-list-cases.py',
    'validate-two-hundred-ninety-five-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('two-hundred-ninety-four', 'three-hundred')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
