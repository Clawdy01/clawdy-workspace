#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-eighty-five', 'three-hundred-eighty-six'),
    ('driehonderdvijfentachtig', 'driehonderdzesentachtig'),
    ('all_cases[:380]', 'all_cases[:381]'),
    ('{UNKNOWN, TYPO}][:380]', '{UNKNOWN, TYPO}][:381]'),
    ('!= 380', '!= 381'),
    ('373, 374, 375, 376, 377, 378, 379]', '373, 374, 375, 376, 377, 378, 379, 380]'),
]
for name in (
    'make-three-hundred-eighty-five.py',
    'create-three-hundred-eighty-five-files.py',
    'create-three-hundred-eighty-five.py',
    'generate-validate-three-hundred-eighty-five.py',
    'validate-three-hundred-eighty-five-valid-list-cases.py',
    'validate-three-hundred-eighty-five-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-five', 'three-hundred-eighty-six')).write_text(text)
