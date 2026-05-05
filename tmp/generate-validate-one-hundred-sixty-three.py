#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-sixty-two', 'one-hundred-sixty-three'),
    ('honderdtweeënzestig', 'honderddrieënzestig'),
    ('162', '163'),
    ('156, 157, 158, 159, 160, 161]', '156, 157, 158, 159, 160, 161, 162]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-sixty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-sixty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
