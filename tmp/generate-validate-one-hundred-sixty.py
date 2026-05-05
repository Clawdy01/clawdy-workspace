#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-nine', 'one-hundred-sixty'),
    ('honderdnegenenvijftig', 'honderdzestig'),
    ('159', '160'),
    ('154, 155, 156, 157, 158]', '154, 155, 156, 157, 158, 159]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
