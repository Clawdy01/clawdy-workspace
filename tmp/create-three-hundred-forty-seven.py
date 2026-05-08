#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-forty-six', 'three-hundred-forty-seven'),
    ('driehonderdzesenveertig', 'driehonderdzevenenveertig'),
    ('[:342]', '[:343]'),
    ('!= 342', '!= 343'),
    (' 340, 341]', ' 340, 341, 342]'),
]

for name in (
    'generate-validate-three-hundred-forty-six.py',
    'validate-three-hundred-forty-six-valid-list-cases.py',
    'validate-three-hundred-forty-six-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-forty-six', 'three-hundred-forty-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
