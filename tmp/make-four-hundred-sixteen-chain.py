#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-fifteen.py', 'gen-four-hundred-sixteen.py', [
        ('four-hundred-fifteen', 'four-hundred-sixteen'),
        ('vierhonderdvijftien', 'vierhonderdzestien'),
        ('four-hundred-nine', 'four-hundred-fifteen'),
        ('vierhonderdnegen', 'vierhonderdvijftien'),
        ('all_cases[:409]', 'all_cases[:409]'),
        ('{UNKNOWN, TYPO}][:409]', '{UNKNOWN, TYPO}][:409]'),
        ('!= 409', '!= 409'),
        ('kreeg 409', 'kreeg 409'),
        (' 409)', ' 409)'),
        (', 400, 401, 402]', ', 404, 405, 406, 407, 408]'),
    ]),
    ('verify-four-hundred-fifteen.py', 'verify-four-hundred-sixteen.py', [
        ('four-hundred-fifteen', 'four-hundred-sixteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
