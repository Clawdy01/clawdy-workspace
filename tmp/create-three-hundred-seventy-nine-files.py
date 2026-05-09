#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-four', 'three-hundred-seventy-nine'),
    ('driehonderdvierenzeventig', 'driehonderdnegenenzeventig'),
    ('all_cases[:369]', 'all_cases[:374]'),
    ('{UNKNOWN, TYPO}][:369]', '{UNKNOWN, TYPO}][:374]'),
    ('!= 369', '!= 374'),
    ('366, 367, 368]', '366, 367, 368, 369, 370, 371, 372, 373]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-four.py', 'create-three-hundred-seventy-nine.py'),
    ('generate-validate-three-hundred-seventy-four.py', 'generate-validate-three-hundred-seventy-nine.py'),
    ('validate-three-hundred-seventy-four-valid-list-cases.py', 'validate-three-hundred-seventy-nine-valid-list-cases.py'),
    ('validate-three-hundred-seventy-four-valid-mixed.py', 'validate-three-hundred-seventy-nine-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
