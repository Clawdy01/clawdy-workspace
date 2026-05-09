#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-two', 'three-hundred-seventy-three'),
    ('driehonderdtweeënzeventig', 'driehonderddrieënzeventig'),
    ('all_cases[:367]', 'all_cases[:368]'),
    ('{UNKNOWN, TYPO}][:367]', '{UNKNOWN, TYPO}][:368]'),
    ('!= 367', '!= 368'),
    ('365, 366]', '365, 366, 367]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-two.py', 'create-three-hundred-seventy-three.py'),
    ('generate-validate-three-hundred-seventy-two.py', 'generate-validate-three-hundred-seventy-three.py'),
    ('validate-three-hundred-seventy-two-valid-list-cases.py', 'validate-three-hundred-seventy-three-valid-list-cases.py'),
    ('validate-three-hundred-seventy-two-valid-mixed.py', 'validate-three-hundred-seventy-three-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
