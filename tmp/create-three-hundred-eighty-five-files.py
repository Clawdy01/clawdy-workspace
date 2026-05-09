#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-four', 'three-hundred-eighty-five'),
    ('driehonderdvierenzeventig', 'driehonderdvijfentachtig'),
    ('all_cases[:369]', 'all_cases[:380]'),
    ('{UNKNOWN, TYPO}][:369]', '{UNKNOWN, TYPO}][:380]'),
    ('!= 369', '!= 380'),
    ('366, 367, 368]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-four.py', 'create-three-hundred-eighty-five.py'),
    ('generate-validate-three-hundred-seventy-four.py', 'generate-validate-three-hundred-eighty-five.py'),
    ('validate-three-hundred-seventy-four-valid-list-cases.py', 'validate-three-hundred-eighty-five-valid-list-cases.py'),
    ('validate-three-hundred-seventy-four-valid-mixed.py', 'validate-three-hundred-eighty-five-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
