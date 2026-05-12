#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-sixty-three-bootstrap.py',
    'create-four-hundred-sixty-three-minimal.py',
    'make-four-hundred-sixty-three.py',
    'create-four-hundred-sixty-three-files.py',
    'create-four-hundred-sixty-three.py',
    'generate-validate-four-hundred-sixty-three.py',
    'validate-four-hundred-sixty-three-valid-list-cases.py',
    'validate-four-hundred-sixty-three-valid-mixed.py',
    'verify-four-hundred-sixty-three.py',
]
repls = [
    ('four-hundred-sixty-three', 'five-hundred-twenty'),
    ('vierhonderddrieënzestig', 'vijfhonderdtwintig'),
    ('[:448]', '[:505]'),
    ('!= 448', '!= 505'),
    ('kreeg 448', 'kreeg 505'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    if name in {
        'validate-four-hundred-sixty-three-valid-list-cases.py',
        'validate-four-hundred-sixty-three-valid-mixed.py',
    }:
        old = ', 443, 444, 445, 446, 447]'
        new = ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496]'
        if old not in text:
            raise SystemExit(f'mis expected ORDER tail in {name}')
        text = text.replace(old, new, 1)
    (root / name.replace('four-hundred-sixty-three', 'four-hundred-ninety-three')).write_text(text)
print('created')
