#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-fourteen-step.py'
dst = root / 'create-four-hundred-fourteen-step.py'
text = src.read_text()
repls = [
    ('four-hundred-fourteen', 'four-hundred-fourteen'),
    ('vierhonderdveertien', 'vierhonderdveertien'),
    ('four-hundred-twelve', 'four-hundred-fourteen'),
    ('vierhonderdtien', 'vierhonderdveertien'),
    ('all_cases[:405]', 'all_cases[:407]'),
    ('{UNKNOWN, TYPO}][:405]', '{UNKNOWN, TYPO}][:407]'),
    ('!= 405', '!= 407'),
    ('kreeg 405', 'kreeg 407'),
    (' 405)', ' 407)'),
    (', 400, 401, 402, 403]', ', 402, 403, 404, 405, 406]'),
    ('all_cases[:402]', 'all_cases[:405]'),
    ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:405]'),
    ('!= 402', '!= 405'),
    ('kreeg 402', 'kreeg 405'),
    (' 402)', ' 405)'),
    (', 398, 399, 400, 401]', ', 400, 401, 402, 403, 404]'),
]
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)
