#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-eight', 'three-hundred-eighty'),
    ('driehonderdachtenzeventig', 'driehonderdtachtig'),
    ('all_cases[:373]', 'all_cases[:375]'),
    ('{UNKNOWN, TYPO}][:373]', '{UNKNOWN, TYPO}][:375]'),
    ('!= 373', '!= 375'),
    ('371, 372]', '371, 372, 373, 374]'),
]
for name in (
    'create-three-hundred-seventy-eight-files.py',
    'create-three-hundred-seventy-eight.py',
    'generate-validate-three-hundred-seventy-eight.py',
    'validate-three-hundred-seventy-eight-valid-list-cases.py',
    'validate-three-hundred-seventy-eight-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-seventy-eight', 'three-hundred-eighty')).write_text(text)
