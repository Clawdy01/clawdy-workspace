#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty.py',
    'create-four-hundred-twenty-files.py',
    'create-four-hundred-twenty.py',
    'generate-validate-four-hundred-twenty.py',
    'validate-four-hundred-twenty-valid-list-cases.py',
    'validate-four-hundred-twenty-valid-mixed.py',
    'verify-four-hundred-twenty.py',
]
repls = [
    ('four-hundred-twenty', 'four-hundred-twenty-one'),
    ('vierhonderdtwintig', 'vierhonderdeenentwintig'),
    ('[:405]', '[:406]'),
    ('!= 405', '!= 406'),
    ('kreeg 405', 'kreeg 406'),
    (' 405)', ' 406)'),
    (', 403, 404]', ', 403, 404, 405]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty', 'four-hundred-twenty-one')).write_text(text)
