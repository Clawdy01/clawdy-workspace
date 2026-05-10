#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-forty-two', 'four-hundred-forty-three'),
    ('vierhonderdtweeenveertig', 'vierhonderddrieenveertig'),
    ('all_cases[:427]', 'all_cases[:428]'),
    ('{UNKNOWN, TYPO}][:427]', '{UNKNOWN, TYPO}][:428]'),
    ('!= 427', '!= 428'),
    ('kreeg 427', 'kreeg 428'),
    (', 424, 425, 426]', ', 424, 425, 426, 427]'),
]
for src_name in [
    'create-four-hundred-forty-two-minimal.py',
    'make-four-hundred-forty-two.py',
    'create-four-hundred-forty-two-files.py',
    'create-four-hundred-forty-two.py',
    'generate-validate-four-hundred-forty-two.py',
    'validate-four-hundred-forty-two-valid-list-cases.py',
    'validate-four-hundred-forty-two-valid-mixed.py',
    'verify-four-hundred-forty-two.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-forty-two', 'four-hundred-forty-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
