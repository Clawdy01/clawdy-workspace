#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-four-assets.py',
    'create-four-hundred-eighty-four-bootstrap.py',
    'create-four-hundred-eighty-four-minimal.py',
    'make-four-hundred-eighty-four.py',
    'create-four-hundred-eighty-four-files.py',
    'create-four-hundred-eighty-four.py',
    'generate-validate-four-hundred-eighty-four.py',
    'validate-four-hundred-eighty-four-valid-list-cases.py',
    'validate-four-hundred-eighty-four-valid-mixed.py',
    'verify-four-hundred-eighty-four.py',
]
base_repls = [
    ('four-hundred-eighty-four', 'four-hundred-eighty-five'),
    ('vierhonderdvierentachtig', 'vierhonderdvijfentachtig'),
]
per_file = {
    'create-four-hundred-eighty-four-assets.py': [
        ('[:469]', '[:470]'),
        ('!= 469', '!= 470'),
        ('kreeg 469', 'kreeg 470'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    ],
    'create-four-hundred-eighty-four-bootstrap.py': [
        ('all_cases[:469]', 'all_cases[:470]'),
        ('{UNKNOWN, TYPO}][:469]', '{UNKNOWN, TYPO}][:470]'),
        ('!= 469', '!= 470'),
        ('kreeg 469', 'kreeg 470'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]'),
    ],
    'create-four-hundred-eighty-four-minimal.py': [
        ('!= 469', '!= 470'),
        ('kreeg 469', 'kreeg 470'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]'),
    ],
    'make-four-hundred-eighty-four.py': [
        ('all_cases[:469]', 'all_cases[:470]'),
        ('{UNKNOWN, TYPO}][:469]', '{UNKNOWN, TYPO}][:470]'),
        ('!= 469', '!= 470'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]'),
    ],
    'create-four-hundred-eighty-four-files.py': [
        ('all_cases[:469]', 'all_cases[:470]'),
        ('{UNKNOWN, TYPO}][:469]', '{UNKNOWN, TYPO}][:470]'),
        ('!= 469', '!= 470'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]'),
    ],
    'create-four-hundred-eighty-four.py': [
        ('all_cases[:469]', 'all_cases[:470]'),
        ('{UNKNOWN, TYPO}][:469]', '{UNKNOWN, TYPO}][:470]'),
        ('!= 469', '!= 470'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    ],
    'generate-validate-four-hundred-eighty-four.py': [
        ('all_cases[:469]', 'all_cases[:470]'),
        ('{UNKNOWN, TYPO}][:469]', '{UNKNOWN, TYPO}][:470]'),
        ('!= 469', '!= 470'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]'),
    ],
    'validate-four-hundred-eighty-four-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]'),
        ('all_cases[:469]', 'all_cases[:470]'),
        ('len(valid_cases) != 469', 'len(valid_cases) != 470'),
    ],
    'validate-four-hundred-eighty-four-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]'),
        ('[:469]', '[:470]'),
        ('len(valid_cases) != 469', 'len(valid_cases) != 470'),
    ],
    'verify-four-hundred-eighty-four.py': [],
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
    out = root / name.replace('four-hundred-eighty-four', 'four-hundred-eighty-five')
    out.write_text(text)
    print(out.name)
