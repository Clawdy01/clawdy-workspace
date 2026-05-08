#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-forty-five', 'three-hundred-forty-six'),
    ('driehonderdvijfenveertig', 'driehonderdzesenveertig'),
    ('[:341]', '[:342]'),
    ('!= 341', '!= 342'),
    (' 340]', ' 340, 341]'),
]

for name in (
    'generate-validate-three-hundred-forty-five.py',
    'validate-three-hundred-forty-five-valid-list-cases.py',
    'validate-three-hundred-forty-five-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-forty-five', 'three-hundred-forty-six')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
