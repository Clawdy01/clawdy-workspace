#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-three', 'four-hundred-forty-four'),
    ('vierhonderddrieenveertig', 'vierhonderdvierenveertig'),
    ('all_cases[:428]', 'all_cases[:429]'),
    ('{UNKNOWN, TYPO}][:428]', '{UNKNOWN, TYPO}][:429]'),
    ('!= 428', '!= 429'),
    ('kreeg 428', 'kreeg 429'),
    (', 424, 425, 426, 427]', ', 424, 425, 426, 427, 428]'),
]
for src_name in [
    'create-four-hundred-forty-three-minimal.py',
    'make-four-hundred-forty-three.py',
    'create-four-hundred-forty-three-files.py',
    'create-four-hundred-forty-three.py',
    'generate-validate-four-hundred-forty-three.py',
    'validate-four-hundred-forty-three-valid-list-cases.py',
    'validate-four-hundred-forty-three-valid-mixed.py',
    'verify-four-hundred-forty-three.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-three', 'four-hundred-forty-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
