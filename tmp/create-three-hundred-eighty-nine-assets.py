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
    ('three-hundred-eighty-seven', 'three-hundred-eighty-nine'),
    ('driehonderdzevenentachtig', 'driehonderdnegenentachtig'),
    ('all_cases[:382]', 'all_cases[:384]'),
    ('{UNKNOWN, TYPO}][:382]', '{UNKNOWN, TYPO}][:384]'),
    ('!= 382', '!= 384'),
    ('381]', '381, 382, 383]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-seven', 'three-hundred-eighty-nine')).write_text(text)
