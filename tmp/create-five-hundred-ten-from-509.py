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
    'create-five-hundred-nine-assets.py',
    'create-five-hundred-ten-assets.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('[:494]', '[:495]'),
        ('!= 494', '!= 495'),
        ('kreeg 494', 'kreeg 495'),
        (', 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485]', ', 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486]'),
    ],
)

build(
    'create-five-hundred-nine-bootstrap.py',
    'create-five-hundred-ten-bootstrap.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('all_cases[:494]', 'all_cases[:495]'),
        ('{UNKNOWN, TYPO}][:494]', '{UNKNOWN, TYPO}][:495]'),
        ('!= 494', '!= 495'),
        ('kreeg 494', 'kreeg 495'),
        (', 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481]', ', 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]'),
    ],
)

build(
    'create-five-hundred-nine-minimal.py',
    'create-five-hundred-ten-minimal.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('!= 494', '!= 495'),
        ('kreeg 494', 'kreeg 495'),
        (' 435)', ' 436)'),
        (', 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481]', ', 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]'),
    ],
)

build(
    'make-five-hundred-nine.py',
    'make-five-hundred-ten.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('all_cases[:494]', 'all_cases[:495]'),
        ('{UNKNOWN, TYPO}][:494]', '{UNKNOWN, TYPO}][:495]'),
        ('!= 494', '!= 495'),
        ('377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421]', '377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422]'),
    ],
)

build(
    'create-five-hundred-nine-files.py',
    'create-five-hundred-ten-files.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('all_cases[:494]', 'all_cases[:495]'),
        ('{UNKNOWN, TYPO}][:494]', '{UNKNOWN, TYPO}][:495]'),
        ('!= 494', '!= 495'),
        ('370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421]', '370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422]'),
    ],
)

build(
    'create-five-hundred-nine.py',
    'create-five-hundred-ten.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('all_cases[:494]', 'all_cases[:495]'),
        ('{UNKNOWN, TYPO}][:494]', '{UNKNOWN, TYPO}][:495]'),
        ('!= 494', '!= 495'),
        ('360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424]', '360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425]'),
    ],
)

build(
    'generate-validate-five-hundred-nine.py',
    'generate-validate-five-hundred-ten.py',
    [
        ('five-hundred-nine', 'five-hundred-ten'),
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('all_cases[:494]', 'all_cases[:495]'),
        ('{UNKNOWN, TYPO}][:494]', '{UNKNOWN, TYPO}][:495]'),
        ('!= 494', '!= 495'),
        (' 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421]', ' 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422]'),
    ],
)

build(
    'validate-five-hundred-nine-valid-list-cases.py',
    'validate-five-hundred-ten-valid-list-cases.py',
    [
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('479, 480, 481, 482]', '479, 480, 481, 482, 483, 484]'),
        ('all_cases[:494]', 'all_cases[:495]'),
        ('len(valid_cases) != 494', 'len(valid_cases) != 495'),
    ],
)

build(
    'validate-five-hundred-nine-valid-mixed.py',
    'validate-five-hundred-ten-valid-mixed.py',
    [
        ('vijfhonderdnegen', 'vijfhonderdtien'),
        ('479, 480, 481, 482]', '479, 480, 481, 482, 483, 484]'),
        ('[:494]', '[:495]'),
        ('len(valid_cases) != 494', 'len(valid_cases) != 495'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-nine', 'five-hundred-ten')
(ROOT / 'verify-five-hundred-ten.py').write_text(verify_text)
print('verify-five-hundred-ten.py')
