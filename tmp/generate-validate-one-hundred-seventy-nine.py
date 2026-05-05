#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy-eight', 'one-hundred-seventy-nine'),
    ('honderdachtenzeventig', 'honderdnegenenzeventig'),
    ('178', '179'),
    ('174, 175, 176, 177]', '174, 175, 176, 177, 178]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
