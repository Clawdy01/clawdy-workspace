#!/usr/bin/env python4
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-seventy-six-assets.py',
    'create-four-hundred-seventy-six-bootstrap.py',
    'create-four-hundred-seventy-six-minimal.py',
    'make-four-hundred-seventy-six.py',
    'create-four-hundred-seventy-six-files.py',
    'create-four-hundred-seventy-six.py',
    'generate-validate-four-hundred-seventy-six.py',
    'validate-four-hundred-seventy-six-valid-list-cases.py',
    'validate-four-hundred-seventy-six-valid-mixed.py',
    'verify-four-hundred-seventy-six.py',
]
base_repls = [
    ('four-hundred-seventy-six', 'four-hundred-seventy-seven'),
    ('vierhonderdzesenzeventig', 'vierhonderdzevenenzeventig'),
]
per_file = {
    'create-four-hundred-seventy-six-assets.py': [
        ('[:461]', '[:462]'),
        ('!= 461', '!= 462'),
        ('kreeg 461', 'kreeg 462'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]'),
    ],
    'create-four-hundred-seventy-six-bootstrap.py': [
        ('all_cases[:461]', 'all_cases[:462]'),
        ('{UNKNOWN, TYPO}][:461]', '{UNKNOWN, TYPO}][:462]'),
        ('!= 461', '!= 462'),
        ('kreeg 461', 'kreeg 462'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451]'),
    ],
    'create-four-hundred-seventy-six-minimal.py': [
        ('!= 461', '!= 462'),
        ('kreeg 461', 'kreeg 462'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451]'),
    ],
    'make-four-hundred-seventy-six.py': [
        ('all_cases[:461]', 'all_cases[:462]'),
        ('{UNKNOWN, TYPO}][:461]', '{UNKNOWN, TYPO}][:462]'),
        ('!= 461', '!= 462'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]'),
    ],
    'create-four-hundred-seventy-six-files.py': [
        ('all_cases[:461]', 'all_cases[:462]'),
        ('{UNKNOWN, TYPO}][:461]', '{UNKNOWN, TYPO}][:462]'),
        ('!= 461', '!= 462'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]'),
    ],
    'create-four-hundred-seventy-six.py': [
        ('all_cases[:461]', 'all_cases[:462]'),
        ('{UNKNOWN, TYPO}][:461]', '{UNKNOWN, TYPO}][:462]'),
        ('!= 461', '!= 462'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]'),
    ],
    'generate-validate-four-hundred-seventy-six.py': [
        ('all_cases[:461]', 'all_cases[:462]'),
        ('{UNKNOWN, TYPO}][:461]', '{UNKNOWN, TYPO}][:462]'),
        ('!= 461', '!= 462'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]'),
    ],
    'validate-four-hundred-seventy-six-valid-list-cases.py': [
        (', 444, 445, 446, 447, 448, 449, 450]', ', 444, 445, 446, 447, 448, 449, 450, 451]'),
        ('all_cases[:461]', 'all_cases[:462]'),
        ('len(valid_cases) != 461', 'len(valid_cases) != 462'),
    ],
    'validate-four-hundred-seventy-six-valid-mixed.py': [
        (', 444, 445, 446, 447, 448, 449, 450]', ', 444, 445, 446, 447, 448, 449, 450, 451]'),
        ('[:461]', '[:462]'),
        ('len(valid_cases) != 461', 'len(valid_cases) != 462'),
    ],
    'verify-four-hundred-seventy-six.py': [],
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
    out = root / name.replace('four-hundred-seventy-six', 'four-hundred-seventy-seven')
    out.write_text(text)
    print(out.name)
