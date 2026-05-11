#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-seventy-five-assets.py',
    'create-four-hundred-seventy-five-bootstrap.py',
    'create-four-hundred-seventy-five-minimal.py',
    'make-four-hundred-seventy-five.py',
    'create-four-hundred-seventy-five-files.py',
    'create-four-hundred-seventy-five.py',
    'generate-validate-four-hundred-seventy-five.py',
    'validate-four-hundred-seventy-five-valid-list-cases.py',
    'validate-four-hundred-seventy-five-valid-mixed.py',
    'verify-four-hundred-seventy-five.py',
]
base_repls = [
    ('four-hundred-seventy-five', 'four-hundred-seventy-six'),
    ('vierhonderdvijfenzeventig', 'vierhonderdzesenzeventig'),
]
per_file = {
    'create-four-hundred-seventy-five-assets.py': [
        ('[:460]', '[:461]'),
        ('!= 460', '!= 461'),
        ('kreeg 460', 'kreeg 461'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]'),
    ],
    'create-four-hundred-seventy-five-bootstrap.py': [
        ('all_cases[:460]', 'all_cases[:461]'),
        ('{UNKNOWN, TYPO}][:460]', '{UNKNOWN, TYPO}][:461]'),
        ('!= 460', '!= 461'),
        ('kreeg 460', 'kreeg 461'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450]'),
    ],
    'create-four-hundred-seventy-five-minimal.py': [
        ('!= 460', '!= 461'),
        ('kreeg 460', 'kreeg 461'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450]'),
    ],
    'make-four-hundred-seventy-five.py': [
        ('all_cases[:460]', 'all_cases[:461]'),
        ('{UNKNOWN, TYPO}][:460]', '{UNKNOWN, TYPO}][:461]'),
        ('!= 460', '!= 461'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]'),
    ],
    'create-four-hundred-seventy-five-files.py': [
        ('all_cases[:460]', 'all_cases[:461]'),
        ('{UNKNOWN, TYPO}][:460]', '{UNKNOWN, TYPO}][:461]'),
        ('!= 460', '!= 461'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]'),
    ],
    'create-four-hundred-seventy-five.py': [
        ('all_cases[:460]', 'all_cases[:461]'),
        ('{UNKNOWN, TYPO}][:460]', '{UNKNOWN, TYPO}][:461]'),
        ('!= 460', '!= 461'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]'),
    ],
    'generate-validate-four-hundred-seventy-five.py': [
        ('all_cases[:460]', 'all_cases[:461]'),
        ('{UNKNOWN, TYPO}][:460]', '{UNKNOWN, TYPO}][:461]'),
        ('!= 460', '!= 461'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]'),
    ],
    'validate-four-hundred-seventy-five-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449]', ', 443, 444, 445, 446, 447, 448, 449, 450]'),
        ('all_cases[:460]', 'all_cases[:461]'),
        ('len(valid_cases) != 460', 'len(valid_cases) != 461'),
    ],
    'validate-four-hundred-seventy-five-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449]', ', 443, 444, 445, 446, 447, 448, 449, 450]'),
        ('[:460]', '[:461]'),
        ('len(valid_cases) != 460', 'len(valid_cases) != 461'),
    ],
    'verify-four-hundred-seventy-five.py': [],
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
    out = root / name.replace('four-hundred-seventy-five', 'four-hundred-seventy-six')
    out.write_text(text)
    print(out.name)
