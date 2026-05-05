#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-eight', 'one-hundred-fifty-nine'),
    ('honderdachtenvijftig', 'honderdnegenenvijftig'),
    ('158', '159'),
    ('153, 154, 155, 156, 157]', '153, 154, 155, 156, 157, 158]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-eight-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
