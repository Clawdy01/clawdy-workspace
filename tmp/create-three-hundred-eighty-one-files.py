#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-four', 'three-hundred-eighty-one'),
    ('driehonderdvierenzeventig', 'driehonderdeenentachtig'),
    ('all_cases[:369]', 'all_cases[:376]'),
    ('{UNKNOWN, TYPO}][:369]', '{UNKNOWN, TYPO}][:376]'),
    ('!= 369', '!= 376'),
    ('366, 367, 368]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-four.py', 'create-three-hundred-eighty-one.py'),
    ('generate-validate-three-hundred-seventy-four.py', 'generate-validate-three-hundred-eighty-one.py'),
    ('validate-three-hundred-seventy-four-valid-list-cases.py', 'validate-three-hundred-eighty-one-valid-list-cases.py'),
    ('validate-three-hundred-seventy-four-valid-mixed.py', 'validate-three-hundred-eighty-one-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
