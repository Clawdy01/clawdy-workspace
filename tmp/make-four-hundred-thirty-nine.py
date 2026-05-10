#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-eighty-four', 'four-hundred-thirty-nine'),
    ('driehonderdvierentachtig', 'vierhonderdnegenendertig'),
    ('all_cases[:379]', 'all_cases[:424]'),
    ('{UNKNOWN, TYPO}][:379]', '{UNKNOWN, TYPO}][:424]'),
    ('!= 379', '!= 424'),
    ('373, 374, 375, 376, 377, 378]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]'),
]
for name in (
    'create-three-hundred-eighty-four-files.py',
    'create-three-hundred-eighty-four.py',
    'generate-validate-three-hundred-eighty-four.py',
    'validate-three-hundred-eighty-four-valid-list-cases.py',
    'validate-three-hundred-eighty-four-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-four', 'four-hundred-thirty-nine')).write_text(text)
