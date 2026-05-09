#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-eighty-one', 'three-hundred-eighty-three'),
    ('driehonderdeenentachtig', 'driehonderddrieentachtig'),
    ('all_cases[:376]', 'all_cases[:378]'),
    ('{UNKNOWN, TYPO}][:376]', '{UNKNOWN, TYPO}][:378]'),
    ('!= 376', '!= 378'),
    ('373, 374, 375]', '373, 374, 375, 376, 377]'),
]
for name in (
    'create-three-hundred-eighty-one-files.py',
    'create-three-hundred-eighty-one.py',
    'generate-validate-three-hundred-eighty-one.py',
    'validate-three-hundred-eighty-one-valid-list-cases.py',
    'validate-three-hundred-eighty-one-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-one', 'three-hundred-eighty-three')).write_text(text)
