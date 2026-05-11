#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-seventy-seven-assets.py',
    'create-four-hundred-seventy-seven-bootstrap.py',
    'create-four-hundred-seventy-seven-minimal.py',
    'make-four-hundred-seventy-seven.py',
    'create-four-hundred-seventy-seven-files.py',
    'create-four-hundred-seventy-seven.py',
    'generate-validate-four-hundred-seventy-seven.py',
    'validate-four-hundred-seventy-seven-valid-list-cases.py',
    'validate-four-hundred-seventy-seven-valid-mixed.py',
    'verify-four-hundred-seventy-seven.py',
]
base_repls = [
    ('four-hundred-seventy-seven', 'four-hundred-seventy-eight'),
    ('vierhonderdzevenenzeventig', 'vierhonderdachtenzeventig'),
]
per_file = {
    'create-four-hundred-seventy-seven-assets.py': [
        ('[:462]', '[:463]'),
        ('!= 462', '!= 463'),
        ('kreeg 462', 'kreeg 463'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]'),
    ],
    'create-four-hundred-seventy-seven-bootstrap.py': [
        ('all_cases[:462]', 'all_cases[:463]'),
        ('{UNKNOWN, TYPO}][:462]', '{UNKNOWN, TYPO}][:463]'),
        ('!= 462', '!= 463'),
        ('kreeg 462', 'kreeg 463'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]'),
    ],
    'create-four-hundred-seventy-seven-minimal.py': [
        ('!= 462', '!= 463'),
        ('kreeg 462', 'kreeg 463'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452]'),
    ],
    'make-four-hundred-seventy-seven.py': [
        ('all_cases[:462]', 'all_cases[:463]'),
        ('{UNKNOWN, TYPO}][:462]', '{UNKNOWN, TYPO}][:463]'),
        ('!= 462', '!= 463'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]'),
    ],
    'create-four-hundred-seventy-seven-files.py': [
        ('all_cases[:462]', 'all_cases[:463]'),
        ('{UNKNOWN, TYPO}][:462]', '{UNKNOWN, TYPO}][:463]'),
        ('!= 462', '!= 463'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]'),
    ],
    'create-four-hundred-seventy-seven.py': [
        ('all_cases[:462]', 'all_cases[:463]'),
        ('{UNKNOWN, TYPO}][:462]', '{UNKNOWN, TYPO}][:463]'),
        ('!= 462', '!= 463'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]'),
    ],
    'generate-validate-four-hundred-seventy-seven.py': [
        ('all_cases[:462]', 'all_cases[:463]'),
        ('{UNKNOWN, TYPO}][:462]', '{UNKNOWN, TYPO}][:463]'),
        ('!= 462', '!= 463'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392]'),
    ],
    'validate-four-hundred-seventy-seven-valid-list-cases.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452]'),
        ('all_cases[:462]', 'all_cases[:463]'),
        ('len(valid_cases) != 462', 'len(valid_cases) != 463'),
    ],
    'validate-four-hundred-seventy-seven-valid-mixed.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452]'),
        ('[:462]', '[:463]'),
        ('len(valid_cases) != 462', 'len(valid_cases) != 463'),
    ],
    'verify-four-hundred-seventy-seven.py': [],
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
    out = root / name.replace('four-hundred-seventy-seven', 'four-hundred-seventy-eight')
    out.write_text(text)
    print(out.name)
