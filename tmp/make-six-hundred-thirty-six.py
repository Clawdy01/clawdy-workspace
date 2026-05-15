#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-eighty-four', 'six-hundred-thirty-six'),
    ('driehonderdvierentachtig', 'zeshonderdzesendertig'),
    ('all_cases[:379]', 'all_cases[:621]'),
    ('{UNKNOWN, TYPO}][:379]', '{UNKNOWN, TYPO}][:621]'),
    ('!= 379', '!= 621'),
    ('373, 374, 375, 376, 377, 378]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 544, 545, 546, 547, 548]'),
]
for name in (
    'create-three-hundred-eighty-four-files.py',
    'create-three-hundred-eighty-four.py',
    'generate-validate-three-hundred-eighty-four.py',
    'validate-three-hundred-eighty-four-valid-list-cases.py',
    'validate-three-hundred-eighty-four-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-eighty-four', 'four-hundred-ninety-three')).write_text(text)
