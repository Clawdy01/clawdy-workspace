#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-six', 'one-hundred-fifty-seven'),
    ('honderdzesenvijftig', 'honderdzevenenvijftig'),
    ('156', '157'),
    ('151, 152, 153, 154, 155]', '151, 152, 153, 154, 155, 156]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-six-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
