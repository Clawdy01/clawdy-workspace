#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-thirty-two.py',
    'create-four-hundred-thirty-two-files.py',
    'create-four-hundred-thirty-two.py',
    'generate-validate-four-hundred-thirty-two.py',
    'validate-four-hundred-thirty-two-valid-list-cases.py',
    'validate-four-hundred-thirty-two-valid-mixed.py',
    'verify-four-hundred-thirty-two.py',
]
repls = [
    ('four-hundred-thirty-two', 'four-hundred-thirty-three'),
    ('vierhonderdtweeendertig', 'vierhonderddrieendertig'),
    ('[:417]', '[:418]'),
    ('!= 417', '!= 418'),
    ('kreeg 417', 'kreeg 418'),
    (' 417)', ' 418)'),
    (', 412, 413, 414, 415, 416]', ', 412, 413, 414, 415, 416, 417]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty-two', 'four-hundred-thirty-three')).write_text(text)
