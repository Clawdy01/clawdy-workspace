#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-one', 'one-hundred-sixty-two'),
    ('honderdeenenzestig', 'honderdtweeënzestig'),
    ('161', '162'),
    ('156, 157, 158, 159, 160]', '156, 157, 158, 159, 160, 161]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
