#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-eighty', 'three-hundred-eighty-one'),
    ('driehonderdtachtig', 'driehonderdeenentachtig'),
    ('all_cases[:375]', 'all_cases[:376]'),
    ('{UNKNOWN, TYPO}][:375]', '{UNKNOWN, TYPO}][:376]'),
    ('!= 375', '!= 376'),
    ('372, 373, 374]', '372, 373, 374, 375]'),
]
for name in (
    'create-three-hundred-eighty-files.py',
    'create-three-hundred-eighty.py',
    'generate-validate-three-hundred-eighty.py',
    'validate-three-hundred-eighty-valid-list-cases.py',
    'validate-three-hundred-eighty-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty', 'three-hundred-eighty-one')).write_text(text)
