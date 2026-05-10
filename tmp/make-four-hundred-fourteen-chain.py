#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-thirteen.py', 'gen-four-hundred-fourteen.py', [
        ('four-hundred-thirteen', 'four-hundred-fourteen'),
        ('vierhonderddertien', 'vierhonderdveertien'),
        ('four-hundred-nine', 'four-hundred-thirteen'),
        ('vierhonderdnegen', 'vierhonderddertien'),
        ('all_cases[:407]', 'all_cases[:407]'),
        ('{UNKNOWN, TYPO}][:407]', '{UNKNOWN, TYPO}][:407]'),
        ('!= 407', '!= 407'),
        ('kreeg 407', 'kreeg 407'),
        (' 407)', ' 407)'),
        (', 400, 401, 402]', ', 402, 403, 404, 405, 406]'),
    ]),
    ('verify-four-hundred-thirteen.py', 'verify-four-hundred-fourteen.py', [
        ('four-hundred-thirteen', 'four-hundred-fourteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
