#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-twenty-eight.py',
    'create-four-hundred-twenty-eight-files.py',
    'create-four-hundred-twenty-eight.py',
    'generate-validate-four-hundred-twenty-eight.py',
    'validate-four-hundred-twenty-eight-valid-list-cases.py',
    'validate-four-hundred-twenty-eight-valid-mixed.py',
    'verify-four-hundred-twenty-eight.py',
]
repls = [
    ('four-hundred-twenty-eight', 'four-hundred-twenty-nine'),
    ('vierhonderdachtentwintig', 'vierhonderdnegenentwintig'),
    ('[:413]', '[:414]'),
    ('!= 413', '!= 414'),
    ('kreeg 413', 'kreeg 414'),
    (' 413)', ' 414)'),
    (', 409, 410, 411, 412]', ', 409, 410, 411, 412, 413]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-twenty-eight', 'four-hundred-twenty-nine')).write_text(text)
