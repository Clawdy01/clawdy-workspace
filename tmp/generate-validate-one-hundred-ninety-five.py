#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-ninety-four', 'one-hundred-ninety-five'),
    ('honderdvierennegentig', 'honderdvijfennegentig'),
    ('193', '194'),
    ('181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191]', '181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-ninety-four-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-ninety-five-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
