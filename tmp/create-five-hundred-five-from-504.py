#!/usr/bin/env python3
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace/tmp')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f'missing in {label}: {old}')
    return text.replace(old, new, 1)


def build(src: str, dst: str, replacements: list[tuple[str, str]]) -> None:
    text = (ROOT / src).read_text()
    for old, new in replacements:
        text = replace_once(text, old, new, src)
    (ROOT / dst).write_text(text)
    print(dst)


build(
    'create-five-hundred-four-assets.py',
    'create-five-hundred-five-assets.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('[:489]', '[:490]'),
        ('!= 489', '!= 490'),
        ('kreeg 489', 'kreeg 490'),
        (', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481]', ', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]'),
    ],
)

build(
    'create-five-hundred-four-bootstrap.py',
    'create-five-hundred-five-bootstrap.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('all_cases[:489]', 'all_cases[:490]'),
        ('{UNKNOWN, TYPO}][:489]', '{UNKNOWN, TYPO}][:490]'),
        ('!= 489', '!= 490'),
        ('kreeg 489', 'kreeg 490'),
        (', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]', ', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478]'),
    ],
)

build(
    'create-five-hundred-four-minimal.py',
    'create-five-hundred-five-minimal.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('!= 489', '!= 490'),
        ('kreeg 489', 'kreeg 490'),
        (' 431)', ' 432)'),
        (', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]', ', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478]'),
    ],
)

build(
    'make-five-hundred-four.py',
    'make-five-hundred-five.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('all_cases[:489]', 'all_cases[:490]'),
        ('{UNKNOWN, TYPO}][:489]', '{UNKNOWN, TYPO}][:490]'),
        ('!= 489', '!= 490'),
        ('375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]', '375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]'),
    ],
)

build(
    'create-five-hundred-four-files.py',
    'create-five-hundred-five-files.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('all_cases[:489]', 'all_cases[:490]'),
        ('{UNKNOWN, TYPO}][:489]', '{UNKNOWN, TYPO}][:490]'),
        ('!= 489', '!= 490'),
        ('368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]', '368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]'),
    ],
)

build(
    'create-five-hundred-four.py',
    'create-five-hundred-five.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('all_cases[:489]', 'all_cases[:490]'),
        ('{UNKNOWN, TYPO}][:489]', '{UNKNOWN, TYPO}][:490]'),
        ('!= 489', '!= 490'),
        ('358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420]', '358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421]'),
    ],
)

build(
    'generate-validate-five-hundred-four.py',
    'generate-validate-five-hundred-five.py',
    [
        ('five-hundred-four', 'five-hundred-five'),
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('all_cases[:489]', 'all_cases[:490]'),
        ('{UNKNOWN, TYPO}][:489]', '{UNKNOWN, TYPO}][:490]'),
        ('!= 489', '!= 490'),
        (' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]', ' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]'),
    ],
)

build(
    'validate-five-hundred-four-valid-list-cases.py',
    'validate-five-hundred-five-valid-list-cases.py',
    [
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('477, 478]', '477, 478, 479]'),
        ('all_cases[:489]', 'all_cases[:490]'),
        ('len(valid_cases) != 489', 'len(valid_cases) != 490'),
    ],
)

build(
    'validate-five-hundred-four-valid-mixed.py',
    'validate-five-hundred-five-valid-mixed.py',
    [
        ('vijfhonderdvier', 'vijfhonderdvijf'),
        ('477, 478]', '477, 478, 479]'),
        ('[:489]', '[:490]'),
        ('len(valid_cases) != 489', 'len(valid_cases) != 490'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-four.py').read_text()
verify_text = verify_src.replace('five-hundred-four', 'five-hundred-five')
(ROOT / 'verify-five-hundred-five.py').write_text(verify_text)
print('verify-five-hundred-five.py')
