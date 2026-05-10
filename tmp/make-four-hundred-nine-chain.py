#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-eight.py', 'gen-four-hundred-nine.py', [
        ('four-hundred-eight', 'four-hundred-nine'),
        ('vierhonderdacht', 'vierhonderdnegen'),
        ('four-hundred-six', 'four-hundred-eight'),
        ('vierhonderdzes', 'vierhonderdacht'),
        ('all_cases[:401]', 'all_cases[:402]'),
        ('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:402]'),
        ('!= 401', '!= 402'),
        ('kreeg 401', 'kreeg 402'),
        (' 401)', ' 402)'),
        (', 398, 399, 400]', ', 398, 399, 400, 401]'),
    ]),
    ('verify-four-hundred-eight.py', 'verify-four-hundred-nine.py', [
        ('four-hundred-eight', 'four-hundred-nine'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
