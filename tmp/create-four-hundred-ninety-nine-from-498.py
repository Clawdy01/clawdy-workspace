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
    'create-four-hundred-ninety-eight-assets.py',
    'create-four-hundred-ninety-nine-assets.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('[:483]', '[:484]'),
        ('!= 483', '!= 484'),
        ('kreeg 483', 'kreeg 484'),
        (', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475]', ', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]'),
    ],
)

build(
    'create-four-hundred-ninety-eight-bootstrap.py',
    'create-four-hundred-ninety-nine-bootstrap.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('all_cases[:483]', 'all_cases[:484]'),
        ('{UNKNOWN, TYPO}][:483]', '{UNKNOWN, TYPO}][:484]'),
        ('!= 483', '!= 484'),
        ('kreeg 483', 'kreeg 484'),
        (', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]', ', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]'),
    ],
)

build(
    'create-four-hundred-ninety-eight-minimal.py',
    'create-four-hundred-ninety-nine-minimal.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('!= 483', '!= 484'),
        ('kreeg 483', 'kreeg 484'),
        (' 425)', ' 426)'),
        (', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]', ', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]'),
    ],
)

build(
    'make-four-hundred-ninety-eight.py',
    'make-four-hundred-ninety-nine.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('all_cases[:483]', 'all_cases[:484]'),
        ('{UNKNOWN, TYPO}][:483]', '{UNKNOWN, TYPO}][:484]'),
        ('!= 483', '!= 484'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]'),
    ],
)

build(
    'create-four-hundred-ninety-eight-files.py',
    'create-four-hundred-ninety-nine-files.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('all_cases[:483]', 'all_cases[:484]'),
        ('{UNKNOWN, TYPO}][:483]', '{UNKNOWN, TYPO}][:484]'),
        ('!= 483', '!= 484'),
        ('368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411]', '368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]'),
    ],
)

build(
    'create-four-hundred-ninety-eight.py',
    'create-four-hundred-ninety-nine.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('all_cases[:483]', 'all_cases[:484]'),
        ('{UNKNOWN, TYPO}][:483]', '{UNKNOWN, TYPO}][:484]'),
        ('!= 483', '!= 484'),
        ('358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414]', '358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415]'),
    ],
)

build(
    'generate-validate-four-hundred-ninety-eight.py',
    'generate-validate-four-hundred-ninety-nine.py',
    [
        ('four-hundred-ninety-eight', 'four-hundred-ninety-nine'),
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('all_cases[:483]', 'all_cases[:484]'),
        ('{UNKNOWN, TYPO}][:483]', '{UNKNOWN, TYPO}][:484]'),
        ('!= 483', '!= 484'),
        (' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411]', ' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]'),
    ],
)

build(
    'validate-four-hundred-ninety-eight-valid-list-cases.py',
    'validate-four-hundred-ninety-nine-valid-list-cases.py',
    [
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]', '450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]'),
        ('all_cases[:483]', 'all_cases[:484]'),
        ('len(valid_cases) != 483', 'len(valid_cases) != 484'),
    ],
)

build(
    'validate-four-hundred-ninety-eight-valid-mixed.py',
    'validate-four-hundred-ninety-nine-valid-mixed.py',
    [
        ('vierhonderdachtennegentig', 'vierhonderdnegenennegentig'),
        ('vierhonderddrieënnegentig', 'vierhonderdnegenennegentig'),
        ('450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]', '450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]'),
        ('[:483]', '[:484]'),
        ('len(valid_cases) != 483', 'len(valid_cases) != 484'),
    ],
)

verify_src = (ROOT / 'verify-four-hundred-ninety-eight.py').read_text()
verify_text = verify_src.replace('four-hundred-ninety-eight', 'four-hundred-ninety-nine')
(ROOT / 'verify-four-hundred-ninety-nine.py').write_text(verify_text)
print('verify-four-hundred-ninety-nine.py')
