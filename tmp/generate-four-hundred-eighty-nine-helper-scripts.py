#!/usr/bin/env python3
from pathlib import Path
root = Path('/home/clawdy/.openclaw/workspace')
tmp = root / 'tmp'

src = tmp / 'create-four-hundred-eighty-eight-helper.py'
text = src.read_text()
repls = [
    ('create-four-hundred-eighty-seven-assets.py', 'create-four-hundred-eighty-eight-assets.py'),
    ('create-four-hundred-eighty-seven-bootstrap.py', 'create-four-hundred-eighty-eight-bootstrap.py'),
    ('create-four-hundred-eighty-seven-minimal.py', 'create-four-hundred-eighty-eight-minimal.py'),
    ('make-four-hundred-eighty-seven.py', 'make-four-hundred-eighty-eight.py'),
    ('create-four-hundred-eighty-seven-files.py', 'create-four-hundred-eighty-eight-files.py'),
    ('create-four-hundred-eighty-seven.py', 'create-four-hundred-eighty-eight.py'),
    ('generate-validate-four-hundred-eighty-seven.py', 'generate-validate-four-hundred-eighty-eight.py'),
    ('validate-four-hundred-eighty-seven-valid-list-cases.py', 'validate-four-hundred-eighty-eight-valid-list-cases.py'),
    ('validate-four-hundred-eighty-seven-valid-mixed.py', 'validate-four-hundred-eighty-eight-valid-mixed.py'),
    ('verify-four-hundred-eighty-seven.py', 'verify-four-hundred-eighty-eight.py'),
    ('four-hundred-eighty-eight', 'four-hundred-eighty-nine'),
    ('vierhonderdachtentachtig', 'vierhonderdnegenentachtig'),
    ('[:473]', '[:474]'),
    ('!= 473', '!= 474'),
    ('kreeg 473', 'kreeg 474'),
    (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]'),
    (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405]'),
    (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463]'),
]
for old, new in repls:
    if old not in text:
        raise SystemExit(f'missing replacement: {old}')
    text = text.replace(old, new)
(tmp / 'create-four-hundred-eighty-nine-helper.py').write_text(text)

src = tmp / 'create-four-hundred-eighty-eight-helper-bootstrap.py'
text = src.read_text()
repls = [
    ('create-four-hundred-eighty-seven-helper.py', 'create-four-hundred-eighty-eight-helper.py'),
    ('create-four-hundred-eighty-eight-helper.py', 'create-four-hundred-eighty-nine-helper.py'),
    ('create-four-hundred-eighty-six-assets.py', 'create-four-hundred-eighty-seven-assets.py'),
    ('create-four-hundred-eighty-seven-assets.py', 'create-four-hundred-eighty-eight-assets.py'),
    ('create-four-hundred-eighty-six-bootstrap.py', 'create-four-hundred-eighty-seven-bootstrap.py'),
    ('create-four-hundred-eighty-seven-bootstrap.py', 'create-four-hundred-eighty-eight-bootstrap.py'),
    ('create-four-hundred-eighty-six-minimal.py', 'create-four-hundred-eighty-seven-minimal.py'),
    ('create-four-hundred-eighty-seven-minimal.py', 'create-four-hundred-eighty-eight-minimal.py'),
    ('make-four-hundred-eighty-six.py', 'make-four-hundred-eighty-seven.py'),
    ('make-four-hundred-eighty-seven.py', 'make-four-hundred-eighty-eight.py'),
    ('create-four-hundred-eighty-six-files.py', 'create-four-hundred-eighty-seven-files.py'),
    ('create-four-hundred-eighty-seven-files.py', 'create-four-hundred-eighty-eight-files.py'),
    ('create-four-hundred-eighty-six.py', 'create-four-hundred-eighty-seven.py'),
    ('create-four-hundred-eighty-seven.py', 'create-four-hundred-eighty-eight.py'),
    ('generate-validate-four-hundred-eighty-six.py', 'generate-validate-four-hundred-eighty-seven.py'),
    ('generate-validate-four-hundred-eighty-seven.py', 'generate-validate-four-hundred-eighty-eight.py'),
    ('validate-four-hundred-eighty-six-valid-list-cases.py', 'validate-four-hundred-eighty-seven-valid-list-cases.py'),
    ('validate-four-hundred-eighty-seven-valid-list-cases.py', 'validate-four-hundred-eighty-eight-valid-list-cases.py'),
    ('validate-four-hundred-eighty-six-valid-mixed.py', 'validate-four-hundred-eighty-seven-valid-mixed.py'),
    ('validate-four-hundred-eighty-seven-valid-mixed.py', 'validate-four-hundred-eighty-eight-valid-mixed.py'),
    ('verify-four-hundred-eighty-six.py', 'verify-four-hundred-eighty-seven.py'),
    ('verify-four-hundred-eighty-seven.py', 'verify-four-hundred-eighty-eight.py'),
    ('four-hundred-eighty-eight', 'four-hundred-eighty-nine'),
    ('vierhonderdachtentachtig', 'vierhonderdnegenentachtig'),
    ('[:473]', '[:474]'),
    ('all_cases[:473]', 'all_cases[:474]'),
    ('{UNKNOWN, TYPO}][:473]', '{UNKNOWN, TYPO}][:474]'),
    ('!= 473', '!= 474'),
    ('kreeg 473', 'kreeg 474'),
    ('len(valid_cases) != 473', 'len(valid_cases) != 474'),
    (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]'),
    (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]'),
    ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405]'),
    (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402]'),
    (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463]'),
]
for old, new in repls:
    if old not in text:
        raise SystemExit(f'missing bootstrap replacement: {old}')
    text = text.replace(old, new)
(tmp / 'create-four-hundred-eighty-nine-helper-bootstrap.py').write_text(text)
print('generated helper scripts')
