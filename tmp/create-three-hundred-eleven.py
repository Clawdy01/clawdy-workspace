#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-nine', 'three-hundred-eleven'),
    ('driehonderdnegen', 'driehonderdelf'),
    ('[:305]', '[:307]'),
    ('!= 305', '!= 307'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306]'),
]

for name in (
    'generate-validate-three-hundred-nine.py',
    'validate-three-hundred-nine-valid-list-cases.py',
    'validate-three-hundred-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-nine', 'three-hundred-eleven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
