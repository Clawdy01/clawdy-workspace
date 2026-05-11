#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-sixty-one-bootstrap.py',
    'create-four-hundred-sixty-one-minimal.py',
    'make-four-hundred-sixty-one.py',
    'create-four-hundred-sixty-one-files.py',
    'create-four-hundred-sixty-one.py',
    'generate-validate-four-hundred-sixty-one.py',
    'validate-four-hundred-sixty-one-valid-list-cases.py',
    'validate-four-hundred-sixty-one-valid-mixed.py',
    'verify-four-hundred-sixty-one.py',
]
repls = [
    ('four-hundred-sixty-one', 'four-hundred-sixty-two'),
    ('vierhonderdeenenzestig', 'vierhonderdtweeënzestig'),
    ('[:446]', '[:447]'),
    ('!= 446', '!= 447'),
    ('kreeg 446', 'kreeg 447'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    if name in {
        'validate-four-hundred-sixty-one-valid-list-cases.py',
        'validate-four-hundred-sixty-one-valid-mixed.py',
    }:
        old = ', 443, 444, 445]'
        new = ', 443, 444, 445, 446]'
        if old not in text:
            raise SystemExit(f'mis expected ORDER tail in {name}')
        text = text.replace(old, new, 1)
    (root / name.replace('four-hundred-sixty-one', 'four-hundred-sixty-two')).write_text(text)
print('created')
