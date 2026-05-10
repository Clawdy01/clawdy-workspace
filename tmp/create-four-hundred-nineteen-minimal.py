#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-eighteen.py',
    'create-four-hundred-eighteen-files.py',
    'create-four-hundred-eighteen.py',
    'generate-validate-four-hundred-eighteen.py',
    'validate-four-hundred-eighteen-valid-list-cases.py',
    'validate-four-hundred-eighteen-valid-mixed.py',
    'verify-four-hundred-eighteen.py',
]
repls = [
    ('four-hundred-eighteen', 'four-hundred-nineteen'),
    ('vierhonderdachttien', 'vierhonderdnegentien'),
    ('[:403]', '[:404]'),
    ('!= 403', '!= 404'),
    ('kreeg 403', 'kreeg 404'),
    (' 403)', ' 404)'),
    (', 400, 401, 402]', ', 400, 401, 402, 403]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-eighteen', 'four-hundred-nineteen')).write_text(text)
