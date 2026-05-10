#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-fourteen.py', 'gen-four-hundred-fifteen.py', [
        ('four-hundred-fourteen', 'four-hundred-fifteen'),
        ('vierhonderdveertien', 'vierhonderdvijftien'),
        ('four-hundred-nine', 'four-hundred-fourteen'),
        ('vierhonderdnegen', 'vierhonderdveertien'),
        ('all_cases[:408]', 'all_cases[:408]'),
        ('{UNKNOWN, TYPO}][:408]', '{UNKNOWN, TYPO}][:408]'),
        ('!= 408', '!= 408'),
        ('kreeg 408', 'kreeg 408'),
        (' 408)', ' 408)'),
        (', 400, 401, 402]', ', 403, 404, 405, 406, 407]'),
    ]),
    ('verify-four-hundred-fourteen.py', 'verify-four-hundred-fifteen.py', [
        ('four-hundred-fourteen', 'four-hundred-fifteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
