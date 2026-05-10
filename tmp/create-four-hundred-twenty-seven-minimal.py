#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-six.py',
    'create-four-hundred-twenty-six-files.py',
    'create-four-hundred-twenty-six.py',
    'generate-validate-four-hundred-twenty-six.py',
    'validate-four-hundred-twenty-six-valid-list-cases.py',
    'validate-four-hundred-twenty-six-valid-mixed.py',
    'verify-four-hundred-twenty-six.py',
]
repls = [
    ('four-hundred-twenty-six', 'four-hundred-twenty-seven'),
    ('vierhonderdzesentwintig', 'vierhonderdzevenentwintig'),
    ('[:411]', '[:412]'),
    ('!= 411', '!= 412'),
    ('kreeg 411', 'kreeg 412'),
    (' 411)', ' 412)'),
    (', 408, 409, 410]', ', 408, 409, 410, 411]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-six', 'four-hundred-twenty-seven')).write_text(text)
