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
    'create-five-hundred-five-assets.py',
    'create-five-hundred-six-assets.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('[:490]', '[:491]'),
        ('!= 490', '!= 491'),
        ('kreeg 490', 'kreeg 491'),
        (', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]', ', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483]'),
    ],
)

build(
    'create-five-hundred-five-bootstrap.py',
    'create-five-hundred-six-bootstrap.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('all_cases[:490]', 'all_cases[:491]'),
        ('{UNKNOWN, TYPO}][:490]', '{UNKNOWN, TYPO}][:491]'),
        ('!= 490', '!= 491'),
        ('kreeg 490', 'kreeg 491'),
        (', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478]', ', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479]'),
    ],
)

build(
    'create-five-hundred-five-minimal.py',
    'create-five-hundred-six-minimal.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('!= 490', '!= 491'),
        ('kreeg 490', 'kreeg 491'),
        (' 432)', ' 433)'),
        (', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478]', ', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479]'),
    ],
)

build(
    'make-five-hundred-five.py',
    'make-five-hundred-six.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('all_cases[:490]', 'all_cases[:491]'),
        ('{UNKNOWN, TYPO}][:490]', '{UNKNOWN, TYPO}][:491]'),
        ('!= 490', '!= 491'),
        ('375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]', '375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]'),
    ],
)

build(
    'create-five-hundred-five-files.py',
    'create-five-hundred-six-files.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('all_cases[:490]', 'all_cases[:491]'),
        ('{UNKNOWN, TYPO}][:490]', '{UNKNOWN, TYPO}][:491]'),
        ('!= 490', '!= 491'),
        ('368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]', '368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]'),
    ],
)

build(
    'create-five-hundred-five.py',
    'create-five-hundred-six.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('all_cases[:490]', 'all_cases[:491]'),
        ('{UNKNOWN, TYPO}][:490]', '{UNKNOWN, TYPO}][:491]'),
        ('!= 490', '!= 491'),
        ('358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421]', '358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422]'),
    ],
)

build(
    'generate-validate-five-hundred-five.py',
    'generate-validate-five-hundred-six.py',
    [
        ('five-hundred-five', 'five-hundred-six'),
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('all_cases[:490]', 'all_cases[:491]'),
        ('{UNKNOWN, TYPO}][:490]', '{UNKNOWN, TYPO}][:491]'),
        ('!= 490', '!= 491'),
        (' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]', ' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]'),
    ],
)

build(
    'validate-five-hundred-five-valid-list-cases.py',
    'validate-five-hundred-six-valid-list-cases.py',
    [
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('477, 478, 479]', '477, 478, 479, 480]'),
        ('all_cases[:490]', 'all_cases[:491]'),
        ('len(valid_cases) != 490', 'len(valid_cases) != 491'),
    ],
)

build(
    'validate-five-hundred-five-valid-mixed.py',
    'validate-five-hundred-six-valid-mixed.py',
    [
        ('vijfhonderdvijf', 'vijfhonderdzes'),
        ('477, 478, 479]', '477, 478, 479, 480]'),
        ('[:490]', '[:491]'),
        ('len(valid_cases) != 490', 'len(valid_cases) != 491'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-five.py').read_text()
verify_text = verify_src.replace('five-hundred-five', 'five-hundred-six')
(ROOT / 'verify-five-hundred-six.py').write_text(verify_text)
print('verify-five-hundred-six.py')
