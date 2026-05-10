#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-seven.py', 'gen-four-hundred-eight.py', [
        ('four-hundred-seven', 'four-hundred-eight'),
        ('vierhonderdzeven', 'vierhonderdacht'),
        ('four-hundred-five', 'four-hundred-seven'),
        ('vierhonderdvijf', 'vierhonderdzeven'),
        ('all_cases[:402]', 'all_cases[:402]'),
        ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:402]'),
        ('!= 402', '!= 402'),
        ('kreeg 402', 'kreeg 402'),
        (' 402)', ' 402)'),
        (', 397, 398, 399, 400, 401]', ', 397, 398, 399, 400, 401]'),
    ]),
    ('verify-four-hundred-seven.py', 'verify-four-hundred-eight.py', [
        ('four-hundred-seven', 'four-hundred-eight'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
