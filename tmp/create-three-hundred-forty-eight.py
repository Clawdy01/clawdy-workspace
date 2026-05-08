#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-forty-seven', 'three-hundred-forty-eight'),
    ('driehonderdzevenenveertig', 'driehonderdachtenveertig'),
    ('[:343]', '[:344]'),
    ('!= 343', '!= 344'),
    (' 340, 341, 342]', ' 340, 341, 342, 343]'),
]

for name in (
    'generate-validate-three-hundred-forty-seven.py',
    'validate-three-hundred-forty-seven-valid-list-cases.py',
    'validate-three-hundred-forty-seven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-forty-seven', 'three-hundred-forty-eight')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
