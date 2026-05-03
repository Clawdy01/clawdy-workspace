#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('eighty-two', 'eighty-three'),
    ('tweeëntachtig', 'drieëntachtig'),
    ('82', '83'),
    ('81]', '81, 82]'),
]
for suffix in ('list-cases', 'mixed'):
    src = root / 'tmp' / f'validate-eighty-two-valid-{suffix}.py'
    dst = root / 'tmp' / f'validate-eighty-three-valid-{suffix}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
    print(dst)
