#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-thirty-one.py',
    'create-four-hundred-thirty-one-files.py',
    'create-four-hundred-thirty-one.py',
    'generate-validate-four-hundred-thirty-one.py',
    'validate-four-hundred-thirty-one-valid-list-cases.py',
    'validate-four-hundred-thirty-one-valid-mixed.py',
    'verify-four-hundred-thirty-one.py',
]
repls = [
    ('four-hundred-thirty-one', 'four-hundred-thirty-two'),
    ('vierhonderdeenendertig', 'vierhonderdtweeendertig'),
    ('[:416]', '[:417]'),
    ('!= 416', '!= 417'),
    ('kreeg 416', 'kreeg 417'),
    (' 416)', ' 417)'),
    (', 411, 412, 413, 414, 415]', ', 411, 412, 413, 414, 415, 416]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty-one', 'four-hundred-thirty-two')).write_text(text)
