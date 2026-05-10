#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-eleven-step.py'
dst = root / 'create-four-hundred-twelve-step.py'
text = src.read_text()
repls = [
    ('four-hundred-eleven', 'four-hundred-twelve'),
    ('vierhonderdelf', 'vierhonderdtwaalf'),
    ('four-hundred-ten', 'four-hundred-eleven'),
    ('vierhonderdtien', 'vierhonderdelf'),
    ('all_cases[:404]', 'all_cases[:405]'),
    ('{UNKNOWN, TYPO}][:404]', '{UNKNOWN, TYPO}][:405]'),
    ('!= 404', '!= 405'),
    ('kreeg 404', 'kreeg 405'),
    (' 404)', ' 405)'),
    (', 400, 401, 402, 403]', ', 400, 401, 402, 403, 404]'),
    ('all_cases[:402]', 'all_cases[:403]'),
    ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:403]'),
    ('!= 402', '!= 403'),
    ('kreeg 402', 'kreeg 403'),
    (' 402)', ' 403)'),
    (', 398, 399, 400, 401]', ', 398, 399, 400, 401, 402]'),
]
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)
