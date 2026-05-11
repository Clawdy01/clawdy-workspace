#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-seventy-three-step.py'
dst = root / 'create-four-hundred-seventy-four-step.py'
text = src.read_text()
repls = [
    ('four-hundred-seventy-three', 'four-hundred-seventy-four'),
    ('four-hundred-seventy-two', 'four-hundred-seventy-three'),
    ('vierhonderddrieënzeventig', 'vierhonderdvierenzeventig'),
    ('vierhonderdtweeënzeventig', 'vierhonderddrieënzeventig'),
    ('[:458]', '[:459]'),
    ('!= 458', '!= 459'),
    ('kreeg 458', 'kreeg 459'),
    (', 443, 444, 445, 446, 447, 448, 449, 450, 451]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]'),
    (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448]'),
    (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447]'),
    ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391'),
    (', 443, 444, 445, 446, 447]', ', 443, 444, 445, 446, 447, 448]'),
]
for old, new in repls:
    if old not in text:
        raise SystemExit(f'missing: {old}')
    text = text.replace(old, new)
dst.write_text(text)
print(dst)
