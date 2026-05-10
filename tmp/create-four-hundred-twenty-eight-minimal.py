#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-seven.py',
    'create-four-hundred-twenty-seven-files.py',
    'create-four-hundred-twenty-seven.py',
    'generate-validate-four-hundred-twenty-seven.py',
    'validate-four-hundred-twenty-seven-valid-list-cases.py',
    'validate-four-hundred-twenty-seven-valid-mixed.py',
    'verify-four-hundred-twenty-seven.py',
]
repls = [
    ('four-hundred-twenty-seven', 'four-hundred-twenty-eight'),
    ('vierhonderdzevenentwintig', 'vierhonderdachtentwintig'),
    ('[:412]', '[:413]'),
    ('!= 412', '!= 413'),
    ('kreeg 412', 'kreeg 413'),
    (' 412)', ' 413)'),
    (', 409, 410, 411]', ', 409, 410, 411, 412]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-seven', 'four-hundred-twenty-eight')).write_text(text)
