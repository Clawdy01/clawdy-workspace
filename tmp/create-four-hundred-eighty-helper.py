#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-seventy-nine-assets.py',
    'create-four-hundred-seventy-nine-bootstrap.py',
    'create-four-hundred-seventy-nine-minimal.py',
    'make-four-hundred-seventy-nine.py',
    'create-four-hundred-seventy-nine-files.py',
    'create-four-hundred-seventy-nine.py',
    'generate-validate-four-hundred-seventy-nine.py',
    'validate-four-hundred-seventy-nine-valid-list-cases.py',
    'validate-four-hundred-seventy-nine-valid-mixed.py',
    'verify-four-hundred-seventy-nine.py',
]
base_repls = [
    ('four-hundred-seventy-nine', 'four-hundred-eighty'),
    ('vierhonderdnegenenzeventig', 'vierhonderdtachtig'),
]
per_file = {
    'create-four-hundred-seventy-nine-assets.py': [
        ('[:464]', '[:465]'),
        ('!= 464', '!= 465'),
        ('kreeg 464', 'kreeg 465'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]'),
    ],
    'create-four-hundred-seventy-nine-bootstrap.py': [
        ('all_cases[:464]', 'all_cases[:465]'),
        ('{UNKNOWN, TYPO}][:464]', '{UNKNOWN, TYPO}][:465]'),
        ('!= 464', '!= 465'),
        ('kreeg 464', 'kreeg 465'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]'),
    ],
    'create-four-hundred-seventy-nine-minimal.py': [
        ('!= 464', '!= 465'),
        ('kreeg 464', 'kreeg 465'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]'),
    ],
    'make-four-hundred-seventy-nine.py': [
        ('all_cases[:464]', 'all_cases[:465]'),
        ('{UNKNOWN, TYPO}][:464]', '{UNKNOWN, TYPO}][:465]'),
        ('!= 464', '!= 465'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]'),
    ],
    'create-four-hundred-seventy-nine-files.py': [
        ('all_cases[:464]', 'all_cases[:465]'),
        ('{UNKNOWN, TYPO}][:464]', '{UNKNOWN, TYPO}][:465]'),
        ('!= 464', '!= 465'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]'),
    ],
    'create-four-hundred-seventy-nine.py': [
        ('all_cases[:464]', 'all_cases[:465]'),
        ('{UNKNOWN, TYPO}][:464]', '{UNKNOWN, TYPO}][:465]'),
        ('!= 464', '!= 465'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]'),
    ],
    'generate-validate-four-hundred-seventy-nine.py': [
        ('all_cases[:464]', 'all_cases[:465]'),
        ('{UNKNOWN, TYPO}][:464]', '{UNKNOWN, TYPO}][:465]'),
        ('!= 464', '!= 465'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]'),
    ],
    'validate-four-hundred-seventy-nine-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]'),
        ('all_cases[:464]', 'all_cases[:465]'),
        ('len(valid_cases) != 464', 'len(valid_cases) != 465'),
    ],
    'validate-four-hundred-seventy-nine-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]'),
        ('[:464]', '[:465]'),
        ('len(valid_cases) != 464', 'len(valid_cases) != 465'),
    ],
    'verify-four-hundred-seventy-nine.py': [],
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
    out = root / name.replace('four-hundred-seventy-nine', 'four-hundred-eighty')
    out.write_text(text)
    print(out.name)
