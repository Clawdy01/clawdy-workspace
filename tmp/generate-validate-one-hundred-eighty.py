#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy-nine', 'one-hundred-eighty'),
    ('honderdnegenenzeventig', 'honderdtachtig'),
    ('179', '180'),
    ('175, 176, 177, 178]', '175, 176, 177, 178, 179]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-eighty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
