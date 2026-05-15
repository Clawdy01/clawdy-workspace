#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-four', 'six-hundred-thirty-eight'),
    ('driehonderdvierenzeventig', 'zeshonderdachtendertig'),
    ('all_cases[:369]', 'all_cases[:623]'),
    ('{UNKNOWN, TYPO}][:369]', '{UNKNOWN, TYPO}][:623]'),
    ('!= 369', '!= 623'),
    ('366, 367, 368]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 546, 547, 548, 549, 550]'),
]

for src_name, dst_name in (
    ('create-three-hundred-seventy-four.py', 'create-four-hundred-ninety-three.py'),
    ('generate-validate-three-hundred-seventy-four.py', 'generate-validate-four-hundred-ninety-three.py'),
    ('validate-three-hundred-seventy-four-valid-list-cases.py', 'validate-four-hundred-ninety-three-valid-list-cases.py'),
    ('validate-three-hundred-seventy-four-valid-mixed.py', 'validate-four-hundred-ninety-three-valid-mixed.py'),
):
    text = (root / src_name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst_name).write_text(text)
