#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-three-hundred-eighty-seven.py',
    'create-three-hundred-eighty-seven-files.py',
    'create-three-hundred-eighty-seven.py',
    'generate-validate-three-hundred-eighty-seven.py',
    'validate-three-hundred-eighty-seven-valid-list-cases.py',
    'validate-three-hundred-eighty-seven-valid-mixed.py',
    'verify-three-hundred-eighty-seven.py',
]
repls = [
    ('three-hundred-eighty-seven', 'three-hundred-ninety-seven'),
    ('driehonderdzevenentachtig', 'driehonderdzevenennegentig'),
    ('all_cases[:382]', 'all_cases[:392]'),
    ('{UNKNOWN, TYPO}][:382]', '{UNKNOWN, TYPO}][:392]'),
    ('!= 382', '!= 392'),
    ('381]', '381, 382, 383, 384, 385, 386, 387]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-seven', 'three-hundred-ninety-seven')).write_text(text)
