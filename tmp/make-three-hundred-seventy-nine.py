#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-eight', 'three-hundred-seventy-nine'),
    ('driehonderdachtenzeventig', 'driehonderdnegenenzeventig'),
    ('all_cases[:373]', 'all_cases[:374]'),
    ('{UNKNOWN, TYPO}][:373]', '{UNKNOWN, TYPO}][:374]'),
    ('!= 373', '!= 374'),
    ('371, 372]', '371, 372, 373]'),
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
    (root / name.replace('three-hundred-seventy-eight', 'three-hundred-seventy-nine')).write_text(text)
