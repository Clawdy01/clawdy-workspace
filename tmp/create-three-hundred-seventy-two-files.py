#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-one', 'three-hundred-seventy-two'),
    ('driehonderdeenenzeventig', 'driehonderdtweeënzeventig'),
    ('all_cases[:366]', 'all_cases[:367]'),
    ('{UNKNOWN, TYPO}][:366]', '{UNKNOWN, TYPO}][:367]'),
    ('!= 366', '!= 367'),
    ('364, 365]', '364, 365, 366]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-one.py', 'create-three-hundred-seventy-two.py'),
    ('generate-validate-three-hundred-seventy-one.py', 'generate-validate-three-hundred-seventy-two.py'),
    ('validate-three-hundred-seventy-one-valid-list-cases.py', 'validate-three-hundred-seventy-two-valid-list-cases.py'),
    ('validate-three-hundred-seventy-one-valid-mixed.py', 'validate-three-hundred-seventy-two-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
