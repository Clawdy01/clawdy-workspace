#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-six.py', 'gen-four-hundred-seven.py', [
        ('four-hundred-six', 'four-hundred-seven'),
        ('vierhonderdzes', 'vierhonderdzeven'),
        ('four-hundred-five', 'four-hundred-six'),
        ('vierhonderdvijf', 'vierhonderdzes'),
        ('all_cases[:401]', 'all_cases[:402]'),
        ('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:402]'),
        ('!= 401', '!= 402'),
        ('kreeg 401', 'kreeg 402'),
        (' 401)', ' 402)'),
        (', 397, 398, 399, 400]', ', 397, 398, 399, 400, 401]'),
    ]),
    ('verify-four-hundred-six.py', 'verify-four-hundred-seven.py', [
        ('four-hundred-six', 'four-hundred-seven'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
