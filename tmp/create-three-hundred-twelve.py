#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-eleven', 'three-hundred-twelve'),
    ('driehonderdelf', 'driehonderdtwaalf'),
    ('[:307]', '[:308]'),
    ('!= 307', '!= 308'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307]'),
]

for name in (
    'generate-validate-three-hundred-eleven.py',
    'validate-three-hundred-eleven-valid-list-cases.py',
    'validate-three-hundred-eleven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-eleven', 'three-hundred-twelve')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
