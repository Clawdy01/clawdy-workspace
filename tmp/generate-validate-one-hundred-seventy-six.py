#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy-five', 'one-hundred-seventy-six'),
    ('honderdvijfenzeventig', 'honderdzesenzeventig'),
    ('175', '176'),
    ('171, 172, 173, 174]', '171, 172, 173, 174, 175]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-five-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
