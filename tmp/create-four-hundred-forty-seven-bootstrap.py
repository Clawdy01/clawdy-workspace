#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-six', 'four-hundred-forty-seven'),
    ('vierhonderdzesenveertig', 'vierhonderdzevenenveertig'),
    ('all_cases[:431]', 'all_cases[:432]'),
    ('{UNKNOWN, TYPO}][:431]', '{UNKNOWN, TYPO}][:432]'),
    ('!= 431', '!= 432'),
    ('kreeg 431', 'kreeg 432'),
    (', 425, 426, 427, 428, 429, 430]', ', 425, 426, 427, 428, 429, 430, 431]'),
]
for src_name in [
    'create-four-hundred-forty-six-minimal.py',
    'make-four-hundred-forty-six.py',
    'create-four-hundred-forty-six-files.py',
    'create-four-hundred-forty-six.py',
    'generate-validate-four-hundred-forty-six.py',
    'validate-four-hundred-forty-six-valid-list-cases.py',
    'validate-four-hundred-forty-six-valid-mixed.py',
    'verify-four-hundred-forty-six.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-six', 'four-hundred-forty-seven')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
