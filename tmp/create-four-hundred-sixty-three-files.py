#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-four', 'four-hundred-sixty-three'),
    ('driehonderdvierenzeventig', 'vierhonderddrieënzestig'),
    ('all_cases[:369]', 'all_cases[:448]'),
    ('{UNKNOWN, TYPO}][:369]', '{UNKNOWN, TYPO}][:448]'),
    ('!= 369', '!= 448'),
    ('366, 367, 368]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-four.py', 'create-four-hundred-sixty-three.py'),
    ('generate-validate-three-hundred-seventy-four.py', 'generate-validate-four-hundred-sixty-three.py'),
    ('validate-three-hundred-seventy-four-valid-list-cases.py', 'validate-four-hundred-sixty-three-valid-list-cases.py'),
    ('validate-three-hundred-seventy-four-valid-mixed.py', 'validate-four-hundred-sixty-three-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
