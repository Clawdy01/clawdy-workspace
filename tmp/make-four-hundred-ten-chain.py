#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-nine.py', 'gen-four-hundred-ten.py', [
        ('four-hundred-nine', 'four-hundred-ten'),
        ('vierhonderdnegen', 'vierhonderdtien'),
        ('four-hundred-eight', 'four-hundred-nine'),
        ('vierhonderdacht', 'vierhonderdnegen'),
        ('all_cases[:402]', 'all_cases[:403]'),
        ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:403]'),
        ('!= 402', '!= 403'),
        ('kreeg 402', 'kreeg 403'),
        (' 402)', ' 403)'),
        (', 399, 400, 401]', ', 399, 400, 401, 402]'),
    ]),
    ('verify-four-hundred-nine.py', 'verify-four-hundred-ten.py', [
        ('four-hundred-nine', 'four-hundred-ten'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
