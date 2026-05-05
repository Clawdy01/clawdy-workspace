#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-seventy', 'one-hundred-seventy-one'),
    ('honderdzeventig', 'honderdeenenzeventig'),
    ('170', '171'),
    ('162, 163, 164, 165, 166, 167, 168, 169]', '162, 163, 164, 165, 166, 167, 168, 169, 170]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-seventy-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-seventy-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
