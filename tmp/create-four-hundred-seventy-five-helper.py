#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-seventy-four-assets.py',
    'create-four-hundred-seventy-four-bootstrap.py',
    'create-four-hundred-seventy-four-minimal.py',
    'make-four-hundred-seventy-four.py',
    'create-four-hundred-seventy-four-files.py',
    'create-four-hundred-seventy-four.py',
    'generate-validate-four-hundred-seventy-four.py',
    'validate-four-hundred-seventy-four-valid-list-cases.py',
    'validate-four-hundred-seventy-four-valid-mixed.py',
    'verify-four-hundred-seventy-four.py',
]
base_repls = [
    ('four-hundred-seventy-four', 'four-hundred-seventy-five'),
    ('vierhonderdvierenzeventig', 'vierhonderdvijfenzeventig'),
]
per_file = {
    'create-four-hundred-seventy-four-assets.py': [
        ('[:459]', '[:460]'),
        ('!= 459', '!= 460'),
        ('kreeg 459', 'kreeg 460'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]'),
    ],
    'create-four-hundred-seventy-four-bootstrap.py': [
        ('all_cases[:459]', 'all_cases[:460]'),
        ('{UNKNOWN, TYPO}][:459]', '{UNKNOWN, TYPO}][:460]'),
        ('!= 459', '!= 460'),
        ('kreeg 459', 'kreeg 460'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449]'),
    ],
    'create-four-hundred-seventy-four-minimal.py': [
        ('!= 459', '!= 460'),
        ('kreeg 459', 'kreeg 460'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449]'),
    ],
    'make-four-hundred-seventy-four.py': [
        ('all_cases[:459]', 'all_cases[:460]'),
        ('{UNKNOWN, TYPO}][:459]', '{UNKNOWN, TYPO}][:460]'),
        ('!= 459', '!= 460'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389]'),
    ],
    'create-four-hundred-seventy-four-files.py': [
        ('all_cases[:459]', 'all_cases[:460]'),
        ('{UNKNOWN, TYPO}][:459]', '{UNKNOWN, TYPO}][:460]'),
        ('!= 459', '!= 460'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389]'),
    ],
    'create-four-hundred-seventy-four.py': [
        ('all_cases[:459]', 'all_cases[:460]'),
        ('{UNKNOWN, TYPO}][:459]', '{UNKNOWN, TYPO}][:460]'),
        ('!= 459', '!= 460'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]'),
    ],
    'generate-validate-four-hundred-seventy-four.py': [
        ('all_cases[:459]', 'all_cases[:460]'),
        ('{UNKNOWN, TYPO}][:459]', '{UNKNOWN, TYPO}][:460]'),
        ('!= 459', '!= 460'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389]'),
    ],
    'validate-four-hundred-seventy-four-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448]', ', 443, 444, 445, 446, 447, 448, 449]'),
        ('all_cases[:459]', 'all_cases[:460]'),
        ('len(valid_cases) != 459', 'len(valid_cases) != 460'),
    ],
    'validate-four-hundred-seventy-four-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448]', ', 443, 444, 445, 446, 447, 448, 449]'),
        ('[:459]', '[:460]'),
        ('len(valid_cases) != 459', 'len(valid_cases) != 460'),
    ],
    'verify-four-hundred-seventy-four.py': [],
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
    out = root / name.replace('four-hundred-seventy-four', 'four-hundred-seventy-five')
    out.write_text(text)
    print(out.name)
