#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-three.py',
    'create-four-hundred-twenty-three-files.py',
    'create-four-hundred-twenty-three.py',
    'generate-validate-four-hundred-twenty-three.py',
    'validate-four-hundred-twenty-three-valid-list-cases.py',
    'validate-four-hundred-twenty-three-valid-mixed.py',
    'verify-four-hundred-twenty-three.py',
]
repls = [
    ('four-hundred-twenty-three', 'four-hundred-twenty-four'),
    ('vierhonderddrieentwintig', 'vierhonderdvierentwintig'),
    ('[:408]', '[:409]'),
    ('!= 408', '!= 409'),
    ('kreeg 408', 'kreeg 409'),
    (' 408)', ' 409)'),
    (', 406, 407]', ', 406, 407, 408]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-three', 'four-hundred-twenty-four')).write_text(text)
