#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'four-hundred-twelve'),
    ('driehonderdeenenzestig', 'vierhonderdtwaalf'),
    ('all_cases[:356]', 'all_cases[:401]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:401]'),
    ('!= 356', '!= 401'),
    (' 353, 354, 355]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-four-hundred-twelve-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
