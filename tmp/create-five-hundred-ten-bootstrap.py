#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('four-hundred-fifty-eight', 'five-hundred-ten'),
    ('vierhonderdachtenvijftig', 'vijfhonderdtien'),
    ('all_cases[:443]', 'all_cases[:495]'),
    ('{UNKNOWN, TYPO}][:443]', '{UNKNOWN, TYPO}][:495]'),
    ('!= 443', '!= 495'),
    ('kreeg 443', 'kreeg 495'),
    (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]'),
]
for src_name in [
    'create-four-hundred-fifty-eight-minimal.py',
    'make-four-hundred-fifty-eight.py',
    'create-four-hundred-fifty-eight-files.py',
    'create-four-hundred-fifty-eight.py',
    'generate-validate-four-hundred-fifty-eight.py',
    'validate-four-hundred-fifty-eight-valid-list-cases.py',
    'validate-four-hundred-fifty-eight-valid-mixed.py',
    'verify-four-hundred-fifty-eight.py',
]:
    src = root / src_name
    dst = root / src_name.replace('four-hundred-fifty-eight', 'four-hundred-ninety-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
print('created')
