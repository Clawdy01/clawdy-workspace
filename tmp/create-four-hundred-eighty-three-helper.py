#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-two-assets.py',
    'create-four-hundred-eighty-two-bootstrap.py',
    'create-four-hundred-eighty-two-minimal.py',
    'make-four-hundred-eighty-two.py',
    'create-four-hundred-eighty-two-files.py',
    'create-four-hundred-eighty-two.py',
    'generate-validate-four-hundred-eighty-two.py',
    'validate-four-hundred-eighty-two-valid-list-cases.py',
    'validate-four-hundred-eighty-two-valid-mixed.py',
    'verify-four-hundred-eighty-two.py',
]
base_repls = [
    ('four-hundred-eighty-two', 'four-hundred-eighty-three'),
    ('vierhonderdtweeentachtig', 'vierhonderddrieentachtig'),
]
per_file = {
    'create-four-hundred-eighty-two-assets.py': [
        ('[:467]', '[:468]'),
        ('!= 467', '!= 468'),
        ('kreeg 467', 'kreeg 468'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]'),
    ],
    'create-four-hundred-eighty-two-bootstrap.py': [
        ('all_cases[:467]', 'all_cases[:468]'),
        ('{UNKNOWN, TYPO}][:467]', '{UNKNOWN, TYPO}][:468]'),
        ('!= 467', '!= 468'),
        ('kreeg 467', 'kreeg 468'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]'),
    ],
    'create-four-hundred-eighty-two-minimal.py': [
        ('!= 467', '!= 468'),
        ('kreeg 467', 'kreeg 468'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]'),
    ],
    'make-four-hundred-eighty-two.py': [
        ('all_cases[:467]', 'all_cases[:468]'),
        ('{UNKNOWN, TYPO}][:467]', '{UNKNOWN, TYPO}][:468]'),
        ('!= 467', '!= 468'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]'),
    ],
    'create-four-hundred-eighty-two-files.py': [
        ('all_cases[:467]', 'all_cases[:468]'),
        ('{UNKNOWN, TYPO}][:467]', '{UNKNOWN, TYPO}][:468]'),
        ('!= 467', '!= 468'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]'),
    ],
    'create-four-hundred-eighty-two.py': [
        ('all_cases[:467]', 'all_cases[:468]'),
        ('{UNKNOWN, TYPO}][:467]', '{UNKNOWN, TYPO}][:468]'),
        ('!= 467', '!= 468'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]'),
    ],
    'generate-validate-four-hundred-eighty-two.py': [
        ('all_cases[:467]', 'all_cases[:468]'),
        ('{UNKNOWN, TYPO}][:467]', '{UNKNOWN, TYPO}][:468]'),
        ('!= 467', '!= 468'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396]'),
    ],
    'validate-four-hundred-eighty-two-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]'),
        ('all_cases[:467]', 'all_cases[:468]'),
        ('len(valid_cases) != 467', 'len(valid_cases) != 468'),
    ],
    'validate-four-hundred-eighty-two-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457]'),
        ('[:467]', '[:468]'),
        ('len(valid_cases) != 467', 'len(valid_cases) != 468'),
    ],
    'verify-four-hundred-eighty-two.py': [],
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
    out = root / name.replace('four-hundred-eighty-two', 'four-hundred-eighty-three')
    out.write_text(text)
    print(out.name)
