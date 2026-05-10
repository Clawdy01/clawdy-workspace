#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-fifteen-step.py'
dst = root / 'create-four-hundred-fifteen-step.py'
text = src.read_text()
repls = [
    ('four-hundred-fifteen', 'four-hundred-fifteen'),
    ('vierhonderdvijftien', 'vierhonderdvijftien'),
    ('four-hundred-thirteen', 'four-hundred-fifteen'),
    ('vierhonderdtien', 'vierhonderdvijftien'),
    ('all_cases[:406]', 'all_cases[:408]'),
    ('{UNKNOWN, TYPO}][:406]', '{UNKNOWN, TYPO}][:408]'),
    ('!= 406', '!= 408'),
    ('kreeg 406', 'kreeg 408'),
    (' 406)', ' 408)'),
    (', 400, 401, 402, 403]', ', 403, 404, 405, 406, 407]'),
    ('all_cases[:402]', 'all_cases[:406]'),
    ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:406]'),
    ('!= 402', '!= 406'),
    ('kreeg 402', 'kreeg 406'),
    (' 402)', ' 406)'),
    (', 398, 399, 400, 401]', ', 401, 402, 403, 404, 405]'),
]
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)
