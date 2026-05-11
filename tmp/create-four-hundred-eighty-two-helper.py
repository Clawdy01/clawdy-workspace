#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-one-assets.py',
    'create-four-hundred-eighty-one-bootstrap.py',
    'create-four-hundred-eighty-one-minimal.py',
    'make-four-hundred-eighty-one.py',
    'create-four-hundred-eighty-one-files.py',
    'create-four-hundred-eighty-one.py',
    'generate-validate-four-hundred-eighty-one.py',
    'validate-four-hundred-eighty-one-valid-list-cases.py',
    'validate-four-hundred-eighty-one-valid-mixed.py',
    'verify-four-hundred-eighty-one.py',
]
base_repls = [
    ('four-hundred-eighty-one', 'four-hundred-eighty-two'),
    ('vierhonderdeenentachtig', 'vierhonderdtweeentachtig'),
]
per_file = {
    'create-four-hundred-eighty-one-assets.py': [
        ('[:466]', '[:467]'),
        ('!= 466', '!= 467'),
        ('kreeg 466', 'kreeg 467'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]'),
    ],
    'create-four-hundred-eighty-one-bootstrap.py': [
        ('all_cases[:466]', 'all_cases[:467]'),
        ('{UNKNOWN, TYPO}][:466]', '{UNKNOWN, TYPO}][:467]'),
        ('!= 466', '!= 467'),
        ('kreeg 466', 'kreeg 467'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]'),
    ],
    'create-four-hundred-eighty-one-minimal.py': [
        ('!= 466', '!= 467'),
        ('kreeg 466', 'kreeg 467'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]'),
    ],
    'make-four-hundred-eighty-one.py': [
        ('all_cases[:466]', 'all_cases[:467]'),
        ('{UNKNOWN, TYPO}][:466]', '{UNKNOWN, TYPO}][:467]'),
        ('!= 466', '!= 467'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]'),
    ],
    'create-four-hundred-eighty-one-files.py': [
        ('all_cases[:466]', 'all_cases[:467]'),
        ('{UNKNOWN, TYPO}][:466]', '{UNKNOWN, TYPO}][:467]'),
        ('!= 466', '!= 467'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]'),
    ],
    'create-four-hundred-eighty-one.py': [
        ('all_cases[:466]', 'all_cases[:467]'),
        ('{UNKNOWN, TYPO}][:466]', '{UNKNOWN, TYPO}][:467]'),
        ('!= 466', '!= 467'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]'),
    ],
    'generate-validate-four-hundred-eighty-one.py': [
        ('all_cases[:466]', 'all_cases[:467]'),
        ('{UNKNOWN, TYPO}][:466]', '{UNKNOWN, TYPO}][:467]'),
        ('!= 466', '!= 467'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]'),
    ],
    'validate-four-hundred-eighty-one-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]'),
        ('all_cases[:466]', 'all_cases[:467]'),
        ('len(valid_cases) != 466', 'len(valid_cases) != 467'),
    ],
    'validate-four-hundred-eighty-one-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]'),
        ('[:466]', '[:467]'),
        ('len(valid_cases) != 466', 'len(valid_cases) != 467'),
    ],
    'verify-four-hundred-eighty-one.py': [],
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
    out = root / name.replace('four-hundred-eighty-one', 'four-hundred-eighty-two')
    out.write_text(text)
    print(out.name)
