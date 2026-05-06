#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-six', 'two-hundred-seven'),
    ('tweehonderdzes', 'tweehonderdzeven'),
    ('205', '206'),
    ('196, 197, 198, 199, 200, 201, 202, 203]', '196, 197, 198, 199, 200, 201, 202, 203, 204]'),
]
for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-six-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-seven-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
