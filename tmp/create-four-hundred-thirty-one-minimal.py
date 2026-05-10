#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-thirty.py',
    'create-four-hundred-thirty-files.py',
    'create-four-hundred-thirty.py',
    'generate-validate-four-hundred-thirty.py',
    'validate-four-hundred-thirty-valid-list-cases.py',
    'validate-four-hundred-thirty-valid-mixed.py',
    'verify-four-hundred-thirty.py',
]
repls = [
    ('four-hundred-thirty', 'four-hundred-thirty-one'),
    ('vierhonderddertig', 'vierhonderdeenendertig'),
    ('[:415]', '[:416]'),
    ('!= 415', '!= 416'),
    ('kreeg 415', 'kreeg 416'),
    (' 415)', ' 416)'),
    (', 410, 411, 412, 413, 414]', ', 410, 411, 412, 413, 414, 415]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty', 'four-hundred-thirty-one')).write_text(text)
