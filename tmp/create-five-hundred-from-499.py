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
    'create-four-hundred-ninety-nine-assets.py',
    'create-five-hundred-assets.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('[:484]', '[:485]'),
        ('!= 484', '!= 485'),
        ('kreeg 484', 'kreeg 485'),
        (', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]', ', 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]'),
    ],
)

build(
    'create-four-hundred-ninety-nine-bootstrap.py',
    'create-five-hundred-bootstrap.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('all_cases[:484]', 'all_cases[:485]'),
        ('{UNKNOWN, TYPO}][:484]', '{UNKNOWN, TYPO}][:485]'),
        ('!= 484', '!= 485'),
        ('kreeg 484', 'kreeg 485'),
        (', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]', ', 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]'),
    ],
)

build(
    'create-four-hundred-ninety-nine-minimal.py',
    'create-five-hundred-minimal.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('!= 484', '!= 485'),
        ('kreeg 484', 'kreeg 485'),
        (' 426)', ' 427)'),
        (', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]', ', 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]'),
    ],
)

build(
    'make-four-hundred-ninety-nine.py',
    'make-five-hundred.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('all_cases[:484]', 'all_cases[:485]'),
        ('{UNKNOWN, TYPO}][:484]', '{UNKNOWN, TYPO}][:485]'),
        ('!= 484', '!= 485'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413]'),
    ],
)

build(
    'create-four-hundred-ninety-nine-files.py',
    'create-five-hundred-files.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('all_cases[:484]', 'all_cases[:485]'),
        ('{UNKNOWN, TYPO}][:484]', '{UNKNOWN, TYPO}][:485]'),
        ('!= 484', '!= 485'),
        ('368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]', '368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413]'),
    ],
)

build(
    'create-four-hundred-ninety-nine.py',
    'create-five-hundred.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('all_cases[:484]', 'all_cases[:485]'),
        ('{UNKNOWN, TYPO}][:484]', '{UNKNOWN, TYPO}][:485]'),
        ('!= 484', '!= 485'),
        ('358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415]', '358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]'),
    ],
)

build(
    'generate-validate-four-hundred-ninety-nine.py',
    'generate-validate-five-hundred.py',
    [
        ('four-hundred-ninety-nine', 'five-hundred'),
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('all_cases[:484]', 'all_cases[:485]'),
        ('{UNKNOWN, TYPO}][:484]', '{UNKNOWN, TYPO}][:485]'),
        ('!= 484', '!= 485'),
        (' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412]', ' 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413]'),
    ],
)

build(
    'validate-four-hundred-ninety-nine-valid-list-cases.py',
    'validate-five-hundred-valid-list-cases.py',
    [
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]', '450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474]'),
        ('all_cases[:484]', 'all_cases[:485]'),
        ('len(valid_cases) != 484', 'len(valid_cases) != 485'),
    ],
)

build(
    'validate-four-hundred-ninety-nine-valid-mixed.py',
    'validate-five-hundred-valid-mixed.py',
    [
        ('vierhonderdnegenennegentig', 'vijfhonderd'),
        ('450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]', '450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474]'),
        ('[:484]', '[:485]'),
        ('len(valid_cases) != 484', 'len(valid_cases) != 485'),
    ],
)

verify_src = (ROOT / 'verify-four-hundred-ninety-nine.py').read_text()
verify_text = verify_src.replace('four-hundred-ninety-nine', 'five-hundred')
(ROOT / 'verify-five-hundred.py').write_text(verify_text)
print('verify-five-hundred.py')
