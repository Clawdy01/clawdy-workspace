#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-eighty-eight-assets.py',
    'create-four-hundred-eighty-eight-bootstrap.py',
    'create-four-hundred-eighty-eight-minimal.py',
    'make-four-hundred-eighty-eight.py',
    'create-four-hundred-eighty-eight-files.py',
    'create-four-hundred-eighty-eight.py',
    'generate-validate-four-hundred-eighty-eight.py',
    'validate-four-hundred-eighty-eight-valid-list-cases.py',
    'validate-four-hundred-eighty-eight-valid-mixed.py',
    'verify-four-hundred-eighty-eight.py',
]
base_repls = [
    ('four-hundred-eighty-eight', 'four-hundred-eighty-nine'),
    ('vierhonderdachtentachtig', 'vierhonderdnegenentachtig'),
]
per_file = {
    'create-four-hundred-eighty-eight-assets.py': [
        ('[:473]', '[:474]'),
        ('!= 473', '!= 474'),
        ('kreeg 473', 'kreeg 474'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]'),
    ],
    'create-four-hundred-eighty-eight-bootstrap.py': [
        ('all_cases[:473]', 'all_cases[:474]'),
        ('{UNKNOWN, TYPO}][:473]', '{UNKNOWN, TYPO}][:474]'),
        ('!= 473', '!= 474'),
        ('kreeg 473', 'kreeg 474'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    ],
    'create-four-hundred-eighty-eight-minimal.py': [
        ('!= 473', '!= 474'),
        ('kreeg 473', 'kreeg 474'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    ],
    'make-four-hundred-eighty-eight.py': [
        ('all_cases[:473]', 'all_cases[:474]'),
        ('{UNKNOWN, TYPO}][:473]', '{UNKNOWN, TYPO}][:474]'),
        ('!= 473', '!= 474'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ],
    'create-four-hundred-eighty-eight-files.py': [
        ('all_cases[:473]', 'all_cases[:474]'),
        ('{UNKNOWN, TYPO}][:473]', '{UNKNOWN, TYPO}][:474]'),
        ('!= 473', '!= 474'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ],
    'create-four-hundred-eighty-eight.py': [
        ('all_cases[:473]', 'all_cases[:474]'),
        ('{UNKNOWN, TYPO}][:473]', '{UNKNOWN, TYPO}][:474]'),
        ('!= 473', '!= 474'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405]'),
    ],
    'generate-validate-four-hundred-eighty-eight.py': [
        ('all_cases[:473]', 'all_cases[:474]'),
        ('{UNKNOWN, TYPO}][:473]', '{UNKNOWN, TYPO}][:474]'),
        ('!= 473', '!= 474'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ],
    'validate-four-hundred-eighty-eight-valid-list-cases.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463]'),
        ('all_cases[:473]', 'all_cases[:474]'),
        ('len(valid_cases) != 473', 'len(valid_cases) != 474'),
    ],
    'validate-four-hundred-eighty-eight-valid-mixed.py': [
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463]'),
        ('[:473]', '[:474]'),
        ('len(valid_cases) != 473', 'len(valid_cases) != 474'),
    ],
    'verify-four-hundred-eighty-eight.py': [],
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
    out = root / name.replace('four-hundred-eighty-eight', 'four-hundred-eighty-nine')
    out.write_text(text)
    print(out.name)
