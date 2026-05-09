#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-three', 'three-hundred-seventy-four'),
    ('driehonderddrieënzeventig', 'driehonderdvierenzeventig'),
    ('all_cases[:368]', 'all_cases[:369]'),
    ('{UNKNOWN, TYPO}][:368]', '{UNKNOWN, TYPO}][:369]'),
    ('!= 368', '!= 369'),
    ('365, 366, 367]', '365, 366, 367, 368]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-three.py', 'create-three-hundred-seventy-four.py'),
    ('generate-validate-three-hundred-seventy-three.py', 'generate-validate-three-hundred-seventy-four.py'),
    ('validate-three-hundred-seventy-three-valid-list-cases.py', 'validate-three-hundred-seventy-four-valid-list-cases.py'),
    ('validate-three-hundred-seventy-three-valid-mixed.py', 'validate-three-hundred-seventy-four-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
