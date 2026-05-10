#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-seventeen.py',
    'create-four-hundred-seventeen-files.py',
    'create-four-hundred-seventeen.py',
    'generate-validate-four-hundred-seventeen.py',
    'validate-four-hundred-seventeen-valid-list-cases.py',
    'validate-four-hundred-seventeen-valid-mixed.py',
    'verify-four-hundred-seventeen.py',
]
repls = [
    ('four-hundred-seventeen', 'four-hundred-eighteen'),
    ('vierhonderdzeventien', 'vierhonderdachttien'),
    ('[:402]', '[:403]'),
    ('!= 402', '!= 403'),
    ('kreeg 402', 'kreeg 403'),
    (' 402)', ' 403)'),
    (', 400, 401]', ', 400, 401, 402]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-seventeen', 'four-hundred-eighteen')).write_text(text)
