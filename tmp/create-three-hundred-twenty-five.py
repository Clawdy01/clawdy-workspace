#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-twenty-four', 'three-hundred-twenty-five'),
    ('driehonderdvierentwintig', 'driehonderdvijfentwintig'),
    ('[:320]', '[:321]'),
    ('!= 320', '!= 321'),
    (' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319]', ' 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320]'),
]

for name in (
    'generate-validate-three-hundred-twenty-four.py',
    'validate-three-hundred-twenty-four-valid-list-cases.py',
    'validate-three-hundred-twenty-four-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-twenty-four', 'three-hundred-twenty-five')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
