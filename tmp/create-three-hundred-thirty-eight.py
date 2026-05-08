#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-thirty-seven', 'three-hundred-thirty-eight'),
    ('driehonderdzevenendertig', 'driehonderdachtendertig'),
    ('[:333]', '[:334]'),
    ('!= 333', '!= 334'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333]'),
]

for name in (
    'generate-validate-three-hundred-thirty-seven.py',
    'validate-three-hundred-thirty-seven-valid-list-cases.py',
    'validate-three-hundred-thirty-seven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-thirty-seven', 'three-hundred-thirty-eight')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
