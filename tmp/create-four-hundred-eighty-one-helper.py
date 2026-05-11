#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-assets.py',
    'create-four-hundred-eighty-bootstrap.py',
    'create-four-hundred-eighty-minimal.py',
    'make-four-hundred-eighty.py',
    'create-four-hundred-eighty-files.py',
    'create-four-hundred-eighty.py',
    'generate-validate-four-hundred-eighty.py',
    'validate-four-hundred-eighty-valid-list-cases.py',
    'validate-four-hundred-eighty-valid-mixed.py',
    'verify-four-hundred-eighty.py',
]
base_repls = [
    ('four-hundred-eighty', 'four-hundred-eighty-one'),
    ('vierhonderdtachtig', 'vierhonderdeenentachtig'),
]
per_file = {
    'create-four-hundred-eighty-assets.py': [
        ('[:465]', '[:466]'),
        ('!= 465', '!= 466'),
        ('kreeg 465', 'kreeg 466'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]'),
    ],
    'create-four-hundred-eighty-bootstrap.py': [
        ('all_cases[:465]', 'all_cases[:466]'),
        ('{UNKNOWN, TYPO}][:465]', '{UNKNOWN, TYPO}][:466]'),
        ('!= 465', '!= 466'),
        ('kreeg 465', 'kreeg 466'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]'),
    ],
    'create-four-hundred-eighty-minimal.py': [
        ('!= 465', '!= 466'),
        ('kreeg 465', 'kreeg 466'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]'),
    ],
    'make-four-hundred-eighty.py': [
        ('all_cases[:465]', 'all_cases[:466]'),
        ('{UNKNOWN, TYPO}][:465]', '{UNKNOWN, TYPO}][:466]'),
        ('!= 465', '!= 466'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]'),
    ],
    'create-four-hundred-eighty-files.py': [
        ('all_cases[:465]', 'all_cases[:466]'),
        ('{UNKNOWN, TYPO}][:465]', '{UNKNOWN, TYPO}][:466]'),
        ('!= 465', '!= 466'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]'),
    ],
    'create-four-hundred-eighty.py': [
        ('all_cases[:465]', 'all_cases[:466]'),
        ('{UNKNOWN, TYPO}][:465]', '{UNKNOWN, TYPO}][:466]'),
        ('!= 465', '!= 466'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]'),
    ],
    'generate-validate-four-hundred-eighty.py': [
        ('all_cases[:465]', 'all_cases[:466]'),
        ('{UNKNOWN, TYPO}][:465]', '{UNKNOWN, TYPO}][:466]'),
        ('!= 465', '!= 466'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]'),
    ],
    'validate-four-hundred-eighty-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]'),
        ('all_cases[:465]', 'all_cases[:466]'),
        ('len(valid_cases) != 465', 'len(valid_cases) != 466'),
    ],
    'validate-four-hundred-eighty-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]'),
        ('[:465]', '[:466]'),
        ('len(valid_cases) != 465', 'len(valid_cases) != 466'),
    ],
    'verify-four-hundred-eighty.py': [],
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
    out = root / name.replace('four-hundred-eighty', 'four-hundred-eighty-one')
    out.write_text(text)
    print(out.name)
