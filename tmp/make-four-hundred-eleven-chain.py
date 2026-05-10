#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-ten.py', 'gen-four-hundred-eleven.py', [
        ('four-hundred-ten', 'four-hundred-eleven'),
        ('vierhonderdtien', 'vierhonderdelf'),
        ('four-hundred-nine', 'four-hundred-ten'),
        ('vierhonderdnegen', 'vierhonderdtien'),
        ('all_cases[:403]', 'all_cases[:404]'),
        ('{UNKNOWN, TYPO}][:403]', '{UNKNOWN, TYPO}][:404]'),
        ('!= 403', '!= 404'),
        ('kreeg 403', 'kreeg 404'),
        (' 403)', ' 404)'),
        (', 400, 401, 402]', ', 400, 401, 402, 403]'),
    ]),
    ('verify-four-hundred-ten.py', 'verify-four-hundred-eleven.py', [
        ('four-hundred-ten', 'four-hundred-eleven'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
