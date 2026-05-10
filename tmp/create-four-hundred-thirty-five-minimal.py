#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-thirty-four.py',
    'create-four-hundred-thirty-four-files.py',
    'create-four-hundred-thirty-four.py',
    'generate-validate-four-hundred-thirty-four.py',
    'validate-four-hundred-thirty-four-valid-list-cases.py',
    'validate-four-hundred-thirty-four-valid-mixed.py',
    'verify-four-hundred-thirty-four.py',
]
repls = [
    ('four-hundred-thirty-four', 'four-hundred-thirty-five'),
    ('vierhonderdvierendertig', 'vierhonderdvijfendertig'),
    ('[:419]', '[:420]'),
    ('!= 419', '!= 420'),
    ('kreeg 419', 'kreeg 420'),
    (' 419)', ' 420)'),
    (', 413, 414, 415, 416, 417, 418]', ', 413, 414, 415, 416, 417, 418, 419]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty-four', 'four-hundred-thirty-five')).write_text(text)
