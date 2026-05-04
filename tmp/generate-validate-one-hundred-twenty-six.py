#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-twenty-five', 'one-hundred-twenty-six'),
    ('honderdvijfentwintig', 'honderdzesentwintig'),
    ('125', '126'),
    ('123, 124]', '123, 124, 125]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-twenty-five-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-twenty-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
