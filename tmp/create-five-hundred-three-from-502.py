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
    'create-five-hundred-two-assets.py',
    'create-five-hundred-three-assets.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('[:487]', '[:488]'),
        ('!= 487', '!= 488'),
        ('kreeg 487', 'kreeg 488'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480]'),
    ],
)

build(
    'create-five-hundred-two-bootstrap.py',
    'create-five-hundred-three-bootstrap.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('all_cases[:487]', 'all_cases[:488]'),
        ('{UNKNOWN, TYPO}][:487]', '{UNKNOWN, TYPO}][:488]'),
        ('!= 487', '!= 488'),
        ('kreeg 487', 'kreeg 488'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]'),
    ],
)

build(
    'create-five-hundred-two-minimal.py',
    'create-five-hundred-three-minimal.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('!= 487', '!= 488'),
        ('kreeg 487', 'kreeg 488'),
        (' 429)', ' 430)'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]'),
    ],
)

build(
    'make-five-hundred-two.py',
    'make-five-hundred-three.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('all_cases[:487]', 'all_cases[:488]'),
        ('{UNKNOWN, TYPO}][:487]', '{UNKNOWN, TYPO}][:488]'),
        ('!= 487', '!= 488'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]'),
    ],
)

build(
    'create-five-hundred-two-files.py',
    'create-five-hundred-three-files.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('all_cases[:487]', 'all_cases[:488]'),
        ('{UNKNOWN, TYPO}][:487]', '{UNKNOWN, TYPO}][:488]'),
        ('!= 487', '!= 488'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]'),
    ],
)

build(
    'create-five-hundred-two.py',
    'create-five-hundred-three.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('all_cases[:487]', 'all_cases[:488]'),
        ('{UNKNOWN, TYPO}][:487]', '{UNKNOWN, TYPO}][:488]'),
        ('!= 487', '!= 488'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]'),
    ],
)

build(
    'generate-validate-five-hundred-two.py',
    'generate-validate-five-hundred-three.py',
    [
        ('five-hundred-two', 'five-hundred-three'),
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('all_cases[:487]', 'all_cases[:488]'),
        ('{UNKNOWN, TYPO}][:487]', '{UNKNOWN, TYPO}][:488]'),
        ('!= 487', '!= 488'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]'),
    ],
)

build(
    'validate-five-hundred-two-valid-list-cases.py',
    'validate-five-hundred-three-valid-list-cases.py',
    [
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('475, 476]', '475, 476, 477]'),
        ('all_cases[:487]', 'all_cases[:488]'),
        ('len(valid_cases) != 487', 'len(valid_cases) != 488'),
    ],
)

build(
    'validate-five-hundred-two-valid-mixed.py',
    'validate-five-hundred-three-valid-mixed.py',
    [
        ('vijfhonderdtwee', 'vijfhonderddrie'),
        ('475, 476]', '475, 476, 477]'),
        ('[:487]', '[:488]'),
        ('len(valid_cases) != 487', 'len(valid_cases) != 488'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-two.py').read_text()
verify_text = verify_src.replace('five-hundred-two', 'five-hundred-three')
(ROOT / 'verify-five-hundred-three.py').write_text(verify_text)
print('verify-five-hundred-three.py')
