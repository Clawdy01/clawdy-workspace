#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-fifty-two', 'one-hundred-fifty-three'),
    ('honderdtweeënvijftig', 'honderddrieënvijftig'),
    ('152', '153'),
    ('149, 150, 151]', '149, 150, 151, 152]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-fifty-two-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
