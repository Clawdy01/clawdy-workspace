#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-five-assets.py',
    'create-four-hundred-eighty-five-bootstrap.py',
    'create-four-hundred-eighty-five-minimal.py',
    'make-four-hundred-eighty-five.py',
    'create-four-hundred-eighty-five-files.py',
    'create-four-hundred-eighty-five.py',
    'generate-validate-four-hundred-eighty-five.py',
    'validate-four-hundred-eighty-five-valid-list-cases.py',
    'validate-four-hundred-eighty-five-valid-mixed.py',
    'verify-four-hundred-eighty-five.py',
]
base_repls = [
    ('four-hundred-eighty-five', 'four-hundred-eighty-six'),
    ('vierhonderdvijfentachtig', 'vierhonderdzesentachtig'),
]
per_file = {
    'create-four-hundred-eighty-five-assets.py': [
        ('[:470]', '[:471]'),
        ('!= 470', '!= 471'),
        ('kreeg 470', 'kreeg 471'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463]'),
    ],
    'create-four-hundred-eighty-five-bootstrap.py': [
        ('all_cases[:470]', 'all_cases[:471]'),
        ('{UNKNOWN, TYPO}][:470]', '{UNKNOWN, TYPO}][:471]'),
        ('!= 470', '!= 471'),
        ('kreeg 470', 'kreeg 471'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]'),
    ],
    'create-four-hundred-eighty-five-minimal.py': [
        ('!= 470', '!= 471'),
        ('kreeg 470', 'kreeg 471'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]'),
    ],
    'make-four-hundred-eighty-five.py': [
        ('all_cases[:470]', 'all_cases[:471]'),
        ('{UNKNOWN, TYPO}][:470]', '{UNKNOWN, TYPO}][:471]'),
        ('!= 470', '!= 471'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]'),
    ],
    'create-four-hundred-eighty-five-files.py': [
        ('all_cases[:470]', 'all_cases[:471]'),
        ('{UNKNOWN, TYPO}][:470]', '{UNKNOWN, TYPO}][:471]'),
        ('!= 470', '!= 471'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]'),
    ],
    'create-four-hundred-eighty-five.py': [
        ('all_cases[:470]', 'all_cases[:471]'),
        ('{UNKNOWN, TYPO}][:470]', '{UNKNOWN, TYPO}][:471]'),
        ('!= 470', '!= 471'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ],
    'generate-validate-four-hundred-eighty-five.py': [
        ('all_cases[:470]', 'all_cases[:471]'),
        ('{UNKNOWN, TYPO}][:470]', '{UNKNOWN, TYPO}][:471]'),
        ('!= 470', '!= 471'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]'),
    ],
    'validate-four-hundred-eighty-five-valid-list-cases.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]'),
        ('all_cases[:470]', 'all_cases[:471]'),
        ('len(valid_cases) != 470', 'len(valid_cases) != 471'),
    ],
    'validate-four-hundred-eighty-five-valid-mixed.py': [
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]'),
        ('[:470]', '[:471]'),
        ('len(valid_cases) != 470', 'len(valid_cases) != 471'),
    ],
    'verify-four-hundred-eighty-five.py': [],
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
    out = root / name.replace('four-hundred-eighty-five', 'four-hundred-eighty-six')
    out.write_text(text)
    print(out.name)
