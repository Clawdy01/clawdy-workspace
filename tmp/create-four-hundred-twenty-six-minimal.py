#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-five.py',
    'create-four-hundred-twenty-five-files.py',
    'create-four-hundred-twenty-five.py',
    'generate-validate-four-hundred-twenty-five.py',
    'validate-four-hundred-twenty-five-valid-list-cases.py',
    'validate-four-hundred-twenty-five-valid-mixed.py',
    'verify-four-hundred-twenty-five.py',
]
repls = [
    ('four-hundred-twenty-five', 'four-hundred-twenty-six'),
    ('vierhonderdvijfentwintig', 'vierhonderdzesentwintig'),
    ('[:410]', '[:411]'),
    ('!= 410', '!= 411'),
    ('kreeg 410', 'kreeg 411'),
    (' 410)', ' 411)'),
    (', 407, 408, 409]', ', 407, 408, 409, 410]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-five', 'four-hundred-twenty-six')).write_text(text)
