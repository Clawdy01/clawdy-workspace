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
    'create-four-hundred-ninety-six-assets.py',
    'create-four-hundred-ninety-seven-assets.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('[:481]', '[:482]'),
        ('!= 481', '!= 482'),
        ('kreeg 481', 'kreeg 482'),
        (', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]', ', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474]'),
    ],
)

build(
    'create-four-hundred-ninety-six-bootstrap.py',
    'create-four-hundred-ninety-seven-bootstrap.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('all_cases[:481]', 'all_cases[:482]'),
        ('{UNKNOWN, TYPO}][:481]', '{UNKNOWN, TYPO}][:482]'),
        ('!= 481', '!= 482'),
        ('kreeg 481', 'kreeg 482'),
        (', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469]', ', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]'),
    ],
)

build(
    'create-four-hundred-ninety-six-minimal.py',
    'create-four-hundred-ninety-seven-minimal.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('!= 481', '!= 482'),
        ('kreeg 481', 'kreeg 482'),
        (' 423)', ' 424)'),
        (', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469]', ', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]'),
    ],
)

build(
    'make-four-hundred-ninety-six.py',
    'make-four-hundred-ninety-seven.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('all_cases[:481]', 'all_cases[:482]'),
        ('{UNKNOWN, TYPO}][:481]', '{UNKNOWN, TYPO}][:482]'),
        ('!= 481', '!= 482'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]'),
    ],
)

build(
    'create-four-hundred-ninety-six-files.py',
    'create-four-hundred-ninety-seven-files.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('all_cases[:481]', 'all_cases[:482]'),
        ('{UNKNOWN, TYPO}][:481]', '{UNKNOWN, TYPO}][:482]'),
        ('!= 481', '!= 482'),
        ('368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409]', '368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]'),
    ],
)

build(
    'create-four-hundred-ninety-six.py',
    'create-four-hundred-ninety-seven.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('all_cases[:481]', 'all_cases[:482]'),
        ('{UNKNOWN, TYPO}][:481]', '{UNKNOWN, TYPO}][:482]'),
        ('!= 481', '!= 482'),
        ('358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]', '358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413]'),
    ],
)

build(
    'generate-validate-four-hundred-ninety-six.py',
    'generate-validate-four-hundred-ninety-seven.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('all_cases[:481]', 'all_cases[:482]'),
        ('{UNKNOWN, TYPO}][:481]', '{UNKNOWN, TYPO}][:482]'),
        ('!= 481', '!= 482'),
        (' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409]', ' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]'),
    ],
)

build(
    'validate-four-hundred-ninety-six-valid-list-cases.py',
    'validate-four-hundred-ninety-seven-valid-list-cases.py',
    [
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]', '450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]'),
        ('all_cases[:481]', 'all_cases[:482]'),
        ('len(valid_cases) != 481', 'len(valid_cases) != 482'),
    ],
)

build(
    'validate-four-hundred-ninety-six-valid-mixed.py',
    'validate-four-hundred-ninety-seven-valid-mixed.py',
    [
        ('vierhonderdzesennegentig', 'vierhonderdzevenennegentig'),
        ('450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]', '450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]'),
        ('[:481]', '[:482]'),
        ('len(valid_cases) != 481', 'len(valid_cases) != 482'),
    ],
)

build(
    'verify-four-hundred-ninety-six.py',
    'verify-four-hundred-ninety-seven.py',
    [
        ('four-hundred-ninety-six', 'four-hundred-ninety-seven'),
        ('four-hundred-ninety-three', 'four-hundred-ninety-seven'),
    ],
)
