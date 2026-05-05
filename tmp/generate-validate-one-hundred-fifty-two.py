#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-one', 'one-hundred-fifty-two'),
    ('honderdeenenvijftig', 'honderdtweeënvijftig'),
    ('151', '152'),
    ('148, 149, 150]', '148, 149, 150, 151]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
