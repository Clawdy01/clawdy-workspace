#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-thirteen-step.py'
dst = root / 'create-four-hundred-thirteen-step.py'
text = src.read_text()
repls = [
    ('four-hundred-thirteen', 'four-hundred-thirteen'),
    ('vierhonderddertien', 'vierhonderddertien'),
    ('four-hundred-eleven', 'four-hundred-thirteen'),
    ('vierhonderdtien', 'vierhonderddertien'),
    ('all_cases[:404]', 'all_cases[:406]'),
    ('{UNKNOWN, TYPO}][:404]', '{UNKNOWN, TYPO}][:406]'),
    ('!= 404', '!= 406'),
    ('kreeg 404', 'kreeg 406'),
    (' 404)', ' 406)'),
    (', 400, 401, 402, 403]', ', 401, 402, 403, 404, 405]'),
    ('all_cases[:402]', 'all_cases[:404]'),
    ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:404]'),
    ('!= 402', '!= 404'),
    ('kreeg 402', 'kreeg 404'),
    (' 402)', ' 404)'),
    (', 398, 399, 400, 401]', ', 399, 400, 401, 402, 403]'),
]
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)
