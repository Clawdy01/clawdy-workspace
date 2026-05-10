#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-eleven.py', 'gen-four-hundred-twelve.py', [
        ('four-hundred-eleven', 'four-hundred-twelve'),
        ('vierhonderdelf', 'vierhonderdtwaalf'),
        ('four-hundred-nine', 'four-hundred-eleven'),
        ('vierhonderdnegen', 'vierhonderdelf'),
        ('all_cases[:403]', 'all_cases[:405]'),
        ('{UNKNOWN, TYPO}][:403]', '{UNKNOWN, TYPO}][:405]'),
        ('!= 403', '!= 405'),
        ('kreeg 403', 'kreeg 405'),
        (' 403)', ' 405)'),
        (', 400, 401, 402]', ', 400, 401, 402, 403, 404]'),
    ]),
    ('verify-four-hundred-eleven.py', 'verify-four-hundred-twelve.py', [
        ('four-hundred-eleven', 'four-hundred-twelve'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
