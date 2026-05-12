#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'make-four-hundred-thirty-four.py',
    'create-four-hundred-thirty-four-files.py',
    'create-four-hundred-thirty-four.py',
    'generate-validate-four-hundred-thirty-four.py',
    'validate-four-hundred-thirty-four-valid-list-cases.py',
    'validate-four-hundred-thirty-four-valid-mixed.py',
    'verify-four-hundred-thirty-four.py',
]
repls = [
    ('four-hundred-thirty-four', 'four-hundred-ninety-eight'),
    ('vierhonderdvierendertig', 'vierhonderdachtennegentig'),
    ('[:424]', '[:424]'),
    ('!= 422', '!= 483'),
    ('kreeg 422', 'kreeg 483'),
    (' 419)', ' 425)'),
    (', 413, 414, 415, 416, 417, 418]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('four-hundred-thirty-four', 'four-hundred-ninety-three')).write_text(text)
