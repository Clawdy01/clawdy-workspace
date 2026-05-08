#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-seven', 'three-hundred-eight'),
    ('driehonderdzeven', 'driehonderdacht'),
    ('[:303]', '[:304]'),
    ('!= 303', '!= 304'),
    (' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302]', ' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303]'),
]

for name in (
    'generate-validate-three-hundred-seven.py',
    'validate-three-hundred-seven-valid-list-cases.py',
    'validate-three-hundred-seven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-seven', 'three-hundred-eight')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
