#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-seven-assets.py',
    'create-four-hundred-eighty-seven-bootstrap.py',
    'create-four-hundred-eighty-seven-minimal.py',
    'make-four-hundred-eighty-seven.py',
    'create-four-hundred-eighty-seven-files.py',
    'create-four-hundred-eighty-seven.py',
    'generate-validate-four-hundred-eighty-seven.py',
    'validate-four-hundred-eighty-seven-valid-list-cases.py',
    'validate-four-hundred-eighty-seven-valid-mixed.py',
    'verify-four-hundred-eighty-seven.py',
]
base_repls = [
    ('four-hundred-eighty-seven', 'four-hundred-eighty-eight'),
    ('vierhonderdzevenentachtig', 'vierhonderdachtentachtig'),
]
per_file = {
    'create-four-hundred-eighty-seven-assets.py': [
        ('[:472]', '[:473]'),
        ('!= 472', '!= 473'),
        ('kreeg 472', 'kreeg 473'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465]'),
    ],
    'create-four-hundred-eighty-seven-bootstrap.py': [
        ('all_cases[:472]', 'all_cases[:473]'),
        ('{UNKNOWN, TYPO}][:472]', '{UNKNOWN, TYPO}][:473]'),
        ('!= 472', '!= 473'),
        ('kreeg 472', 'kreeg 473'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
    ],
    'create-four-hundred-eighty-seven-minimal.py': [
        ('!= 472', '!= 473'),
        ('kreeg 472', 'kreeg 473'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
    ],
    'make-four-hundred-eighty-seven.py': [
        ('all_cases[:472]', 'all_cases[:473]'),
        ('{UNKNOWN, TYPO}][:472]', '{UNKNOWN, TYPO}][:473]'),
        ('!= 472', '!= 473'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    ],
    'create-four-hundred-eighty-seven-files.py': [
        ('all_cases[:472]', 'all_cases[:473]'),
        ('{UNKNOWN, TYPO}][:472]', '{UNKNOWN, TYPO}][:473]'),
        ('!= 472', '!= 473'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    ],
    'create-four-hundred-eighty-seven.py': [
        ('all_cases[:472]', 'all_cases[:473]'),
        ('{UNKNOWN, TYPO}][:472]', '{UNKNOWN, TYPO}][:473]'),
        ('!= 472', '!= 473'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404]'),
    ],
    'generate-validate-four-hundred-eighty-seven.py': [
        ('all_cases[:472]', 'all_cases[:473]'),
        ('{UNKNOWN, TYPO}][:472]', '{UNKNOWN, TYPO}][:473]'),
        ('!= 472', '!= 473'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    ],
    'validate-four-hundred-eighty-seven-valid-list-cases.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
        ('all_cases[:472]', 'all_cases[:473]'),
        ('len(valid_cases) != 472', 'len(valid_cases) != 473'),
    ],
    'validate-four-hundred-eighty-seven-valid-mixed.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
        ('[:472]', '[:473]'),
        ('len(valid_cases) != 472', 'len(valid_cases) != 473'),
    ],
    'verify-four-hundred-eighty-seven.py': [],
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
    out = root / name.replace('four-hundred-eighty-seven', 'four-hundred-eighty-eight')
    out.write_text(text)
    print(out.name)
