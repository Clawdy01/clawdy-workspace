#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-twelve.py', 'gen-four-hundred-thirteen.py', [
        ('four-hundred-twelve', 'four-hundred-thirteen'),
        ('vierhonderdtwaalf', 'vierhonderddertien'),
        ('four-hundred-nine', 'four-hundred-twelve'),
        ('vierhonderdnegen', 'vierhonderdtwaalf'),
        ('all_cases[:406]', 'all_cases[:406]'),
        ('{UNKNOWN, TYPO}][:406]', '{UNKNOWN, TYPO}][:406]'),
        ('!= 406', '!= 406'),
        ('kreeg 406', 'kreeg 406'),
        (' 406)', ' 406)'),
        (', 400, 401, 402]', ', 401, 402, 403, 404, 405]'),
    ]),
    ('verify-four-hundred-twelve.py', 'verify-four-hundred-thirteen.py', [
        ('four-hundred-twelve', 'four-hundred-thirteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
