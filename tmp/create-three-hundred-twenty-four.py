#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-twenty-two', 'three-hundred-twenty-four'),
    ('driehonderdtweeentwintig', 'driehonderdvierentwintig'),
    ('[:318]', '[:320]'),
    ('!= 318', '!= 320'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319]'),
]

for name in (
    'generate-validate-three-hundred-twenty-two.py',
    'validate-three-hundred-twenty-two-valid-list-cases.py',
    'validate-three-hundred-twenty-two-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-twenty-two', 'three-hundred-twenty-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
