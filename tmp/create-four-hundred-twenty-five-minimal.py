#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-four.py',
    'create-four-hundred-twenty-four-files.py',
    'create-four-hundred-twenty-four.py',
    'generate-validate-four-hundred-twenty-four.py',
    'validate-four-hundred-twenty-four-valid-list-cases.py',
    'validate-four-hundred-twenty-four-valid-mixed.py',
    'verify-four-hundred-twenty-four.py',
]
repls = [
    ('four-hundred-twenty-four', 'four-hundred-twenty-five'),
    ('vierhonderdvierentwintig', 'vierhonderdvijfentwintig'),
    ('[:409]', '[:410]'),
    ('!= 409', '!= 410'),
    ('kreeg 409', 'kreeg 410'),
    (' 409)', ' 410)'),
    (', 406, 407, 408]', ', 406, 407, 408, 409]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-four', 'four-hundred-twenty-five')).write_text(text)
