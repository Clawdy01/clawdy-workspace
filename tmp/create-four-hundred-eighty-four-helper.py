#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-three-assets.py',
    'create-four-hundred-eighty-three-bootstrap.py',
    'create-four-hundred-eighty-three-minimal.py',
    'make-four-hundred-eighty-three.py',
    'create-four-hundred-eighty-three-files.py',
    'create-four-hundred-eighty-three.py',
    'generate-validate-four-hundred-eighty-three.py',
    'validate-four-hundred-eighty-three-valid-list-cases.py',
    'validate-four-hundred-eighty-three-valid-mixed.py',
    'verify-four-hundred-eighty-three.py',
]
base_repls = [
    ('four-hundred-eighty-three', 'four-hundred-eighty-four'),
    ('vierhonderddrieentachtig', 'vierhonderdvierentachtig'),
]
per_file = {
    'create-four-hundred-eighty-three-assets.py': [
        ('[:468]', '[:469]'),
        ('!= 468', '!= 469'),
        ('kreeg 468', 'kreeg 469'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
    ],
    'create-four-hundred-eighty-three-bootstrap.py': [
        ('all_cases[:468]', 'all_cases[:469]'),
        ('{UNKNOWN, TYPO}][:468]', '{UNKNOWN, TYPO}][:469]'),
        ('!= 468', '!= 469'),
        ('kreeg 468', 'kreeg 469'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]'),
    ],
    'create-four-hundred-eighty-three-minimal.py': [
        ('!= 468', '!= 469'),
        ('kreeg 468', 'kreeg 469'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]'),
    ],
    'make-four-hundred-eighty-three.py': [
        ('all_cases[:468]', 'all_cases[:469]'),
        ('{UNKNOWN, TYPO}][:468]', '{UNKNOWN, TYPO}][:469]'),
        ('!= 468', '!= 469'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]'),
    ],
    'create-four-hundred-eighty-three-files.py': [
        ('all_cases[:468]', 'all_cases[:469]'),
        ('{UNKNOWN, TYPO}][:468]', '{UNKNOWN, TYPO}][:469]'),
        ('!= 468', '!= 469'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]'),
    ],
    'create-four-hundred-eighty-three.py': [
        ('all_cases[:468]', 'all_cases[:469]'),
        ('{UNKNOWN, TYPO}][:468]', '{UNKNOWN, TYPO}][:469]'),
        ('!= 468', '!= 469'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]'),
    ],
    'generate-validate-four-hundred-eighty-three.py': [
        ('all_cases[:468]', 'all_cases[:469]'),
        ('{UNKNOWN, TYPO}][:468]', '{UNKNOWN, TYPO}][:469]'),
        ('!= 468', '!= 469'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397]'),
    ],
    'validate-four-hundred-eighty-three-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]'),
        ('all_cases[:468]', 'all_cases[:469]'),
        ('len(valid_cases) != 468', 'len(valid_cases) != 469'),
    ],
    'validate-four-hundred-eighty-three-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]'),
        ('[:468]', '[:469]'),
        ('len(valid_cases) != 468', 'len(valid_cases) != 469'),
    ],
    'verify-four-hundred-eighty-three.py': [],
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
    out = root / name.replace('four-hundred-eighty-three', 'four-hundred-eighty-four')
    out.write_text(text)
    print(out.name)
