#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-six', 'three-hundred-seven'),
    ('driehonderdzes', 'driehonderdzeven'),
    ('[:302]', '[:303]'),
    ('!= 302', '!= 303'),
    (' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301]', ' 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302]'),
]

for name in (
    'generate-validate-three-hundred-six.py',
    'validate-three-hundred-six-valid-list-cases.py',
    'validate-three-hundred-six-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-six', 'three-hundred-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
