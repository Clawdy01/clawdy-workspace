#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-sixteen.py',
    'create-four-hundred-sixteen-files.py',
    'create-four-hundred-sixteen.py',
    'generate-validate-four-hundred-sixteen.py',
    'validate-four-hundred-sixteen-valid-list-cases.py',
    'validate-four-hundred-sixteen-valid-mixed.py',
    'verify-four-hundred-sixteen.py',
]
repls = [
    ('four-hundred-sixteen', 'four-hundred-seventeen'),
    ('vierhonderdzestien', 'vierhonderdzeventien'),
    ('[:401]', '[:402]'),
    ('!= 401', '!= 402'),
    ('kreeg 401', 'kreeg 402'),
    (' 401)', ' 402)'),
    (', 399, 400]', ', 399, 400, 401]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-sixteen', 'four-hundred-seventeen')).write_text(text)
