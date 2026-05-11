#!/usr/bin/env python3
from pathlib import Path
root = Path('/home/clawdy/.openclaw/workspace')
helper = root / 'tmp' / 'create-four-hundred-eighty-seven-helper.py'
text = helper.read_text()
text = text.replace('create-four-hundred-eighty-six-assets.py', 'create-four-hundred-eighty-seven-assets.py')
text = text.replace('create-four-hundred-eighty-six-bootstrap.py', 'create-four-hundred-eighty-seven-bootstrap.py')
text = text.replace('create-four-hundred-eighty-six-minimal.py', 'create-four-hundred-eighty-seven-minimal.py')
text = text.replace('make-four-hundred-eighty-six.py', 'make-four-hundred-eighty-seven.py')
text = text.replace('create-four-hundred-eighty-six-files.py', 'create-four-hundred-eighty-seven-files.py')
text = text.replace('create-four-hundred-eighty-six.py', 'create-four-hundred-eighty-seven.py')
text = text.replace('generate-validate-four-hundred-eighty-six.py', 'generate-validate-four-hundred-eighty-seven.py')
text = text.replace('validate-four-hundred-eighty-six-valid-list-cases.py', 'validate-four-hundred-eighty-seven-valid-list-cases.py')
text = text.replace('validate-four-hundred-eighty-six-valid-mixed.py', 'validate-four-hundred-eighty-seven-valid-mixed.py')
text = text.replace('verify-four-hundred-eighty-six.py', 'verify-four-hundred-eighty-seven.py')
text = text.replace('four-hundred-eighty-seven', 'four-hundred-eighty-eight')
text = text.replace('vierhonderdzevenentachtig', 'vierhonderdachtentachtig')
for old, new in [
    ('[:472]', '[:473]'),
    ('all_cases[:472]', 'all_cases[:473]'),
    ('{UNKNOWN, TYPO}][:472]', '{UNKNOWN, TYPO}][:473]'),
    ('!= 472', '!= 473'),
    ('kreeg 472', 'kreeg 473'),
    ('len(valid_cases) != 472', 'len(valid_cases) != 473'),
]:
    text = text.replace(old, new)
sequence_repls = [
    (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465]'),
    (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
    (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]'),
    ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404]'),
    (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]'),
    (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
]
for old, new in sequence_repls:
    if old not in text:
        raise SystemExit(f'missing sequence: {old}')
    text = text.replace(old, new)
out = root / 'tmp' / 'create-four-hundred-eighty-eight-helper.py'
out.write_text(text)
print(out)
