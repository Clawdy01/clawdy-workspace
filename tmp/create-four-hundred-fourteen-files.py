#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-four', 'four-hundred-fourteen'),
    ('driehonderdvierenzeventig', 'vierhonderdveertien'),
    ('all_cases[:369]', 'all_cases[:401]'),
    ('{UNKNOWN, TYPO}][:369]', '{UNKNOWN, TYPO}][:401]'),
    ('!= 369', '!= 401'),
    ('366, 367, 368]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-four.py', 'create-four-hundred-fourteen.py'),
    ('generate-validate-three-hundred-seventy-four.py', 'generate-validate-four-hundred-fourteen.py'),
    ('validate-three-hundred-seventy-four-valid-list-cases.py', 'validate-four-hundred-fourteen-valid-list-cases.py'),
    ('validate-three-hundred-seventy-four-valid-mixed.py', 'validate-four-hundred-fourteen-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
