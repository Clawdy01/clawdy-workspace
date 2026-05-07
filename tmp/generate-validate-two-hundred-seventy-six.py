#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('two-hundred-twenty-nine', 'two-hundred-seventy-six'),
    ('tweehonderdnegenentwintig', 'tweehonderdzesenzeventig'),
    ('[:227]', '[:272]'),
    ('!= 227', '!= 272'),
    (' 226]', ' 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-two-hundred-twenty-nine-{kind}.py'
    dst = root / 'tmp' / f'validate-two-hundred-seventy-six-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
