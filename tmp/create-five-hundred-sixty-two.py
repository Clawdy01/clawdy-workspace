#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-nine', 'five-hundred-sixty-two'),
    ('driehonderdnegenenzestig', 'vijfhonderdtweeënzestig'),
    ('all_cases[:364]', 'all_cases[:547]'),
    ('{UNKNOWN, TYPO}][:364]', '{UNKNOWN, TYPO}][:547]'),
    ('!= 364', '!= 547'),
    ('356, 357, 358, 359, 360, 361, 362, 363]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 473, 474, 475, 476, 477]'),
]

for name in (
    'generate-validate-three-hundred-sixty-nine.py',
    'validate-three-hundred-sixty-nine-valid-list-cases.py',
    'validate-three-hundred-sixty-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-nine', 'four-hundred-ninety-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
