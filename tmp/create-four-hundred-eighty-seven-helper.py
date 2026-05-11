#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-six-assets.py',
    'create-four-hundred-eighty-six-bootstrap.py',
    'create-four-hundred-eighty-six-minimal.py',
    'make-four-hundred-eighty-six.py',
    'create-four-hundred-eighty-six-files.py',
    'create-four-hundred-eighty-six.py',
    'generate-validate-four-hundred-eighty-six.py',
    'validate-four-hundred-eighty-six-valid-list-cases.py',
    'validate-four-hundred-eighty-six-valid-mixed.py',
    'verify-four-hundred-eighty-six.py',
]
base_repls = [
    ('four-hundred-eighty-six', 'four-hundred-eighty-seven'),
    ('vierhonderdzesentachtig', 'vierhonderdzevenentachtig'),
]
per_file = {
    'create-four-hundred-eighty-six-assets.py': [
        ('[:471]', '[:472]'),
        ('!= 471', '!= 472'),
        ('kreeg 471', 'kreeg 472'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464]'),
    ],
    'create-four-hundred-eighty-six-bootstrap.py': [
        ('all_cases[:471]', 'all_cases[:472]'),
        ('{UNKNOWN, TYPO}][:471]', '{UNKNOWN, TYPO}][:472]'),
        ('!= 471', '!= 472'),
        ('kreeg 471', 'kreeg 472'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]'),
    ],
    'create-four-hundred-eighty-six-minimal.py': [
        ('!= 471', '!= 472'),
        ('kreeg 471', 'kreeg 472'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]'),
    ],
    'make-four-hundred-eighty-six.py': [
        ('all_cases[:471]', 'all_cases[:472]'),
        ('{UNKNOWN, TYPO}][:471]', '{UNKNOWN, TYPO}][:472]'),
        ('!= 471', '!= 472'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]'),
    ],
    'create-four-hundred-eighty-six-files.py': [
        ('all_cases[:471]', 'all_cases[:472]'),
        ('{UNKNOWN, TYPO}][:471]', '{UNKNOWN, TYPO}][:472]'),
        ('!= 471', '!= 472'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]'),
    ],
    'create-four-hundred-eighty-six.py': [
        ('all_cases[:471]', 'all_cases[:472]'),
        ('{UNKNOWN, TYPO}][:471]', '{UNKNOWN, TYPO}][:472]'),
        ('!= 471', '!= 472'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403]'),
    ],
    'generate-validate-four-hundred-eighty-six.py': [
        ('all_cases[:471]', 'all_cases[:472]'),
        ('{UNKNOWN, TYPO}][:471]', '{UNKNOWN, TYPO}][:472]'),
        ('!= 471', '!= 472'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]'),
    ],
    'validate-four-hundred-eighty-six-valid-list-cases.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
        ('all_cases[:471]', 'all_cases[:472]'),
        ('len(valid_cases) != 471', 'len(valid_cases) != 472'),
    ],
    'validate-four-hundred-eighty-six-valid-mixed.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
        ('[:471]', '[:472]'),
        ('len(valid_cases) != 471', 'len(valid_cases) != 472'),
    ],
    'verify-four-hundred-eighty-six.py': [],
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
    out = root / name.replace('four-hundred-eighty-six', 'four-hundred-eighty-seven')
    out.write_text(text)
    print(out.name)
