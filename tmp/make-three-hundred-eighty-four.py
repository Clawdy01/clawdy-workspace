#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-eighty-three', 'three-hundred-eighty-four'),
    ('driehonderddrieentachtig', 'driehonderdvierentachtig'),
    ('all_cases[:378]', 'all_cases[:379]'),
    ('{UNKNOWN, TYPO}][:378]', '{UNKNOWN, TYPO}][:379]'),
    ('!= 378', '!= 379'),
    ('373, 374, 375, 376, 377]', '373, 374, 375, 376, 377, 378]'),
]
for name in (
    'create-three-hundred-eighty-three-files.py',
    'create-three-hundred-eighty-three.py',
    'generate-validate-three-hundred-eighty-three.py',
    'validate-three-hundred-eighty-three-valid-list-cases.py',
    'validate-three-hundred-eighty-three-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-three', 'three-hundred-eighty-four')).write_text(text)
