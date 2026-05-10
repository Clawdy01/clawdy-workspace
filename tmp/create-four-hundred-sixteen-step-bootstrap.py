#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-sixteen-step.py'
dst = root / 'create-four-hundred-sixteen-step.py'
text = src.read_text()
repls = [
    ('four-hundred-sixteen', 'four-hundred-sixteen'),
    ('vierhonderdzestien', 'vierhonderdzestien'),
    ('four-hundred-fourteen', 'four-hundred-sixteen'),
    ('vierhonderdtien', 'vierhonderdzestien'),
    ('all_cases[:407]', 'all_cases[:409]'),
    ('{UNKNOWN, TYPO}][:407]', '{UNKNOWN, TYPO}][:409]'),
    ('!= 407', '!= 409'),
    ('kreeg 407', 'kreeg 409'),
    (' 407)', ' 409)'),
    (', 400, 401, 402, 403]', ', 404, 405, 406, 407, 408]'),
    ('all_cases[:402]', 'all_cases[:407]'),
    ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:407]'),
    ('!= 402', '!= 407'),
    ('kreeg 402', 'kreeg 407'),
    (' 402)', ' 407)'),
    (', 398, 399, 400, 401]', ', 402, 403, 404, 405, 406]'),
]
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)
