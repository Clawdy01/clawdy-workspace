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
    'create-five-hundred-three-assets.py',
    'create-five-hundred-four-assets.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('[:488]', '[:489]'),
        ('!= 488', '!= 489'),
        ('kreeg 488', 'kreeg 489'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481]'),
    ],
)

build(
    'create-five-hundred-three-bootstrap.py',
    'create-five-hundred-four-bootstrap.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('all_cases[:488]', 'all_cases[:489]'),
        ('{UNKNOWN, TYPO}][:488]', '{UNKNOWN, TYPO}][:489]'),
        ('!= 488', '!= 489'),
        ('kreeg 488', 'kreeg 489'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]'),
    ],
)

build(
    'create-five-hundred-three-minimal.py',
    'create-five-hundred-four-minimal.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('!= 488', '!= 489'),
        ('kreeg 488', 'kreeg 489'),
        (' 430)', ' 431)'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]'),
    ],
)

build(
    'make-five-hundred-three.py',
    'make-five-hundred-four.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('all_cases[:488]', 'all_cases[:489]'),
        ('{UNKNOWN, TYPO}][:488]', '{UNKNOWN, TYPO}][:489]'),
        ('!= 488', '!= 489'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]'),
    ],
)

build(
    'create-five-hundred-three-files.py',
    'create-five-hundred-four-files.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('all_cases[:488]', 'all_cases[:489]'),
        ('{UNKNOWN, TYPO}][:488]', '{UNKNOWN, TYPO}][:489]'),
        ('!= 488', '!= 489'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]'),
    ],
)

build(
    'create-five-hundred-three.py',
    'create-five-hundred-four.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('all_cases[:488]', 'all_cases[:489]'),
        ('{UNKNOWN, TYPO}][:488]', '{UNKNOWN, TYPO}][:489]'),
        ('!= 488', '!= 489'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420]'),
    ],
)

build(
    'generate-validate-five-hundred-three.py',
    'generate-validate-five-hundred-four.py',
    [
        ('five-hundred-three', 'five-hundred-four'),
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('all_cases[:488]', 'all_cases[:489]'),
        ('{UNKNOWN, TYPO}][:488]', '{UNKNOWN, TYPO}][:489]'),
        ('!= 488', '!= 489'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417]'),
    ],
)

build(
    'validate-five-hundred-three-valid-list-cases.py',
    'validate-five-hundred-four-valid-list-cases.py',
    [
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('476, 477]', '476, 477, 478]'),
        ('all_cases[:488]', 'all_cases[:489]'),
        ('len(valid_cases) != 488', 'len(valid_cases) != 489'),
    ],
)

build(
    'validate-five-hundred-three-valid-mixed.py',
    'validate-five-hundred-four-valid-mixed.py',
    [
        ('vijfhonderddrie', 'vijfhonderdvier'),
        ('476, 477]', '476, 477, 478]'),
        ('[:488]', '[:489]'),
        ('len(valid_cases) != 488', 'len(valid_cases) != 489'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-three.py').read_text()
verify_text = verify_src.replace('five-hundred-three', 'five-hundred-four')
(ROOT / 'verify-five-hundred-four.py').write_text(verify_text)
print('verify-five-hundred-four.py')
