#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-fifteen', 'three-hundred-sixteen'),
    ('driehonderdvijftien', 'driehonderdzestien'),
    ('[:311]', '[:312]'),
    ('!= 311', '!= 312'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]'),
]

for name in (
    'generate-validate-three-hundred-fifteen.py',
    'validate-three-hundred-fifteen-valid-list-cases.py',
    'validate-three-hundred-fifteen-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-fifteen', 'three-hundred-sixteen')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
