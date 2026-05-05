#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy-seven', 'one-hundred-seventy-eight'),
    ('honderdzevenenzeventig', 'honderdachtenzeventig'),
    ('177', '178'),
    ('173, 174, 175, 176]', '173, 174, 175, 176, 177]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-seven-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-eight-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
