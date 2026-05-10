#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-thirty-three.py',
    'create-four-hundred-thirty-three-files.py',
    'create-four-hundred-thirty-three.py',
    'generate-validate-four-hundred-thirty-three.py',
    'validate-four-hundred-thirty-three-valid-list-cases.py',
    'validate-four-hundred-thirty-three-valid-mixed.py',
    'verify-four-hundred-thirty-three.py',
]
repls = [
    ('four-hundred-thirty-three', 'four-hundred-thirty-four'),
    ('vierhonderddrieendertig', 'vierhonderdvierendertig'),
    ('[:418]', '[:419]'),
    ('!= 418', '!= 419'),
    ('kreeg 418', 'kreeg 419'),
    (' 418)', ' 419)'),
    (', 413, 414, 415, 416, 417]', ', 413, 414, 415, 416, 417, 418]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty-three', 'four-hundred-thirty-four')).write_text(text)
