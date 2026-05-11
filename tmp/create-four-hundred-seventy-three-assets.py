#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-sixty-three-bootstrap.py',
    'create-four-hundred-sixty-three-minimal.py',
    'make-four-hundred-sixty-three.py',
    'create-four-hundred-sixty-three-files.py',
    'create-four-hundred-sixty-three.py',
    'generate-validate-four-hundred-sixty-three.py',
    'validate-four-hundred-sixty-three-valid-list-cases.py',
    'validate-four-hundred-sixty-three-valid-mixed.py',
    'verify-four-hundred-sixty-three.py',
]
repls = [
    ('four-hundred-sixty-three', 'four-hundred-seventy-three'),
    ('vierhonderddrieënzestig', 'vierhonderddrieënzeventig'),
    ('[:448]', '[:458]'),
    ('!= 448', '!= 458'),
    ('kreeg 448', 'kreeg 458'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    if name in {
        'validate-four-hundred-sixty-three-valid-list-cases.py',
        'validate-four-hundred-sixty-three-valid-mixed.py',
    }:
        old = ', 443, 444, 445, 446, 447]'
        new = ', 443, 444, 445, 446, 447, 448, 449, 450, 451]'
        if old not in text:
            raise SystemExit(f'mis expected ORDER tail in {name}')
        text = text.replace(old, new, 1)
    (root / name.replace('four-hundred-sixty-three', 'four-hundred-seventy-three')).write_text(text)
print('created')
