#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-one.py',
    'create-four-hundred-twenty-one-files.py',
    'create-four-hundred-twenty-one.py',
    'generate-validate-four-hundred-twenty-one.py',
    'validate-four-hundred-twenty-one-valid-list-cases.py',
    'validate-four-hundred-twenty-one-valid-mixed.py',
    'verify-four-hundred-twenty-one.py',
]
repls = [
    ('four-hundred-twenty-one', 'four-hundred-twenty-three'),
    ('vierhonderdeenentwintig', 'vierhonderddrieentwintig'),
    ('[:406]', '[:408]'),
    ('!= 406', '!= 408'),
    ('kreeg 406', 'kreeg 408'),
    (' 406)', ' 408)'),
    (', 403, 404, 405]', ', 403, 404, 405, 406, 407]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-one', 'four-hundred-twenty-three')).write_text(text)
