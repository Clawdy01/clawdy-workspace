#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
replacements = [
    ('four-hundred-thirty-eight', 'four-hundred-thirty-nine'),
    ('vierhonderdachtendertig', 'vierhonderdnegenendertig'),
    ('all_cases[:423]', 'all_cases[:424]'),
    ('{UNKNOWN, TYPO}][:423]', '{UNKNOWN, TYPO}][:424]'),
    ('!= 423', '!= 424'),
    ('kreeg 423', 'kreeg 424'),
    (' 421, 422]', ' 421, 422, 423]'),
    ('[:422]', '[:423]'),
    (' 422)', ' 423)'),
]
for src_name in [
    'create-four-hundred-thirty-eight-minimal.py',
    'make-four-hundred-thirty-eight.py',
    'create-four-hundred-thirty-eight-files.py',
    'create-four-hundred-thirty-eight.py',
    'generate-validate-four-hundred-thirty-eight.py',
    'validate-four-hundred-thirty-eight-valid-list-cases.py',
    'validate-four-hundred-thirty-eight-valid-mixed.py',
    'verify-four-hundred-thirty-eight.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-thirty-eight', 'four-hundred-thirty-nine')
    text = src.read_text()
    for old, new in replacements:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
