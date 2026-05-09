#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy', 'three-hundred-seventy-one'),
    ('driehonderdzeventig', 'driehonderdeenenzeventig'),
    ('all_cases[:365]', 'all_cases[:366]'),
    ('{UNKNOWN, TYPO}][:365]', '{UNKNOWN, TYPO}][:366]'),
    ('!= 365', '!= 366'),
    ('356, 357, 358, 359, 360, 361, 362, 363, 364]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy.py', 'create-three-hundred-seventy-one.py'),
    ('generate-validate-three-hundred-seventy.py', 'generate-validate-three-hundred-seventy-one.py'),
    ('validate-three-hundred-seventy-valid-list-cases.py', 'validate-three-hundred-seventy-one-valid-list-cases.py'),
    ('validate-three-hundred-seventy-valid-mixed.py', 'validate-three-hundred-seventy-one-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
