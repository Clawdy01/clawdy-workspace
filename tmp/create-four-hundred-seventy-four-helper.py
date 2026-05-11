#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-seventy-three-assets.py',
    'create-four-hundred-seventy-three-bootstrap.py',
    'create-four-hundred-seventy-three-minimal.py',
    'make-four-hundred-seventy-three.py',
    'create-four-hundred-seventy-three-files.py',
    'create-four-hundred-seventy-three.py',
    'generate-validate-four-hundred-seventy-three.py',
    'validate-four-hundred-seventy-three-valid-list-cases.py',
    'validate-four-hundred-seventy-three-valid-mixed.py',
    'verify-four-hundred-seventy-three.py',
]
base_repls = [
    ('four-hundred-seventy-three', 'four-hundred-seventy-four'),
    ('vierhonderddrieënzeventig', 'vierhonderdvierenzeventig'),
]
per_file = {
    'create-four-hundred-seventy-three-assets.py': [
        ('[:458]', '[:459]'),
        ('!= 458', '!= 459'),
        ('kreeg 458', 'kreeg 459'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]'),
    ],
    'create-four-hundred-seventy-three-bootstrap.py': [
        ('all_cases[:458]', 'all_cases[:459]'),
        ('{UNKNOWN, TYPO}][:458]', '{UNKNOWN, TYPO}][:459]'),
        ('!= 458', '!= 459'),
        ('kreeg 458', 'kreeg 459'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448]'),
    ],
    'create-four-hundred-seventy-three-minimal.py': [
        ('!= 458', '!= 459'),
        ('kreeg 458', 'kreeg 459'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448]'),
    ],
    'make-four-hundred-seventy-three.py': [
        ('all_cases[:458]', 'all_cases[:459]'),
        ('{UNKNOWN, TYPO}][:458]', '{UNKNOWN, TYPO}][:459]'),
        ('!= 458', '!= 459'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]'),
    ],
    'create-four-hundred-seventy-three-files.py': [
        ('all_cases[:458]', 'all_cases[:459]'),
        ('{UNKNOWN, TYPO}][:458]', '{UNKNOWN, TYPO}][:459]'),
        ('!= 458', '!= 459'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]'),
    ],
    'create-four-hundred-seventy-three.py': [
        ('all_cases[:458]', 'all_cases[:459]'),
        ('{UNKNOWN, TYPO}][:458]', '{UNKNOWN, TYPO}][:459]'),
        ('!= 458', '!= 459'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]'),
    ],
    'generate-validate-four-hundred-seventy-three.py': [
        ('all_cases[:458]', 'all_cases[:459]'),
        ('{UNKNOWN, TYPO}][:458]', '{UNKNOWN, TYPO}][:459]'),
        ('!= 458', '!= 459'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]'),
    ],
    'validate-four-hundred-seventy-three-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447]', ', 443, 444, 445, 446, 447, 448]'),
        ('all_cases[:458]', 'all_cases[:459]'),
        ('len(valid_cases) != 458', 'len(valid_cases) != 459'),
    ],
    'validate-four-hundred-seventy-three-valid-mixed.py': [
        (', 443, 444, 445, 446, 447]', ', 443, 444, 445, 446, 447, 448]'),
        ('[:458]', '[:459]'),
        ('len(valid_cases) != 458', 'len(valid_cases) != 459'),
    ],
    'verify-four-hundred-seventy-three.py': [],
}
for name in files:
    text = (root / name).read_text()
    for old, new in base_repls:
        if old in text:
            text = text.replace(old, new)
    for old, new in per_file[name]:
        if old not in text:
            raise SystemExit(f'missing in {name}: {old}')
        text = text.replace(old, new)
    out = root / name.replace('four-hundred-seventy-three', 'four-hundred-seventy-four')
    out.write_text(text)
    print(out.name)
