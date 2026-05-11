#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-sixty-two-bootstrap.py',
    'create-four-hundred-sixty-two-minimal.py',
    'make-four-hundred-sixty-two.py',
    'create-four-hundred-sixty-two-files.py',
    'create-four-hundred-sixty-two.py',
    'generate-validate-four-hundred-sixty-two.py',
    'validate-four-hundred-sixty-two-valid-list-cases.py',
    'validate-four-hundred-sixty-two-valid-mixed.py',
    'verify-four-hundred-sixty-two.py',
]
repls = [
    ('four-hundred-sixty-two', 'four-hundred-sixty-three'),
    ('vierhonderdtweeënzestig', 'vierhonderddrieënzestig'),
    ('[:447]', '[:448]'),
    ('!= 447', '!= 448'),
    ('kreeg 447', 'kreeg 448'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    if name in {
        'validate-four-hundred-sixty-two-valid-list-cases.py',
        'validate-four-hundred-sixty-two-valid-mixed.py',
    }:
        old = ', 443, 444, 445, 446]'
        new = ', 443, 444, 445, 446, 447]'
        if old not in text:
            raise SystemExit(f'mis expected ORDER tail in {name}')
        text = text.replace(old, new, 1)
    (root / name.replace('four-hundred-sixty-two', 'four-hundred-sixty-three')).write_text(text)
print('created')
