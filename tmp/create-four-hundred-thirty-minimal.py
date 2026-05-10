#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-nine.py',
    'create-four-hundred-twenty-nine-files.py',
    'create-four-hundred-twenty-nine.py',
    'generate-validate-four-hundred-twenty-nine.py',
    'validate-four-hundred-twenty-nine-valid-list-cases.py',
    'validate-four-hundred-twenty-nine-valid-mixed.py',
    'verify-four-hundred-twenty-nine.py',
]
repls = [
    ('four-hundred-twenty-nine', 'four-hundred-thirty'),
    ('vierhonderdnegenentwintig', 'vierhonderddertig'),
    ('[:414]', '[:415]'),
    ('!= 414', '!= 415'),
    ('kreeg 414', 'kreeg 415'),
    (' 414)', ' 415)'),
    (', 409, 410, 411, 412, 413]', ', 409, 410, 411, 412, 413, 414]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-nine', 'four-hundred-thirty')).write_text(text)
