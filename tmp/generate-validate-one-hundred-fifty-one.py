#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty', 'one-hundred-fifty-one'),
    ('honderdvijftig', 'honderdeenenvijftig'),
    ('150', '151'),
    ('147, 148, 149]', '147, 148, 149, 150]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
