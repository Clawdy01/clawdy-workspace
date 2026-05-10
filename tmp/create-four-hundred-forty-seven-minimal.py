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
    ('four-hundred-thirty-four', 'four-hundred-forty-seven'),
    ('vierhonderdvierendertig', 'vierhonderdzevenenveertig'),
    ('[:424]', '[:424]'),
    ('!= 422', '!= 432'),
    ('kreeg 422', 'kreeg 432'),
    (' 419)', ' 420)'),
    (', 413, 414, 415, 416, 417, 418]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty-four', 'four-hundred-forty-seven')).write_text(text)
