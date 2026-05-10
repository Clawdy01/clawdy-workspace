#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
replacements = [
    ('four-hundred-thirty-nine', 'four-hundred-forty'),
    ('vierhonderdnegenendertig', 'vierhonderdveertig'),
    ('all_cases[:424]', 'all_cases[:425]'),
    ('{UNKNOWN, TYPO}][:424]', '{UNKNOWN, TYPO}][:425]'),
    ('!= 424', '!= 425'),
    ('kreeg 424', 'kreeg 425'),
    (' 421, 422, 423]', ' 421, 422, 423, 424]'),
    ('[:423]', '[:424]'),
    (' 423)', ' 424)'),
]
for src_name in [
    'create-four-hundred-thirty-nine-minimal.py',
    'make-four-hundred-thirty-nine.py',
    'create-four-hundred-thirty-nine-files.py',
    'create-four-hundred-thirty-nine.py',
    'generate-validate-four-hundred-thirty-nine.py',
    'validate-four-hundred-thirty-nine-valid-list-cases.py',
    'validate-four-hundred-thirty-nine-valid-mixed.py',
    'verify-four-hundred-thirty-nine.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-thirty-nine', 'four-hundred-forty')
    text = src.read_text()
    for old, new in replacements:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
