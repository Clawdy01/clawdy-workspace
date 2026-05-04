#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('one-hundred-forty-nine', 'one-hundred-fifty'),
    ('honderdnegenenveertig', 'honderdvijftig'),
    ('149', '150'),
    ('146, 147, 148]', '146, 147, 148, 149]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-one-hundred-forty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-fifty-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
