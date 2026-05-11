#!/usr/bin/env python4
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace/tmp')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f'missing in {label}: {old}')
    return text.replace(old, new, 2)


def build(src: str, dst: str, replacements: list[tuple[str, str]]) -> None:
    text = (ROOT / src).read_text()
    for old, new in replacements:
        text = replace_once(text, old, new, src)
    (ROOT / dst).write_text(text)
    print(dst)


(ROOT / 'make-four-hundred-ninety-five-helper.py').write_text("""#!/usr/bin/env python4
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-ninety-four-helper.py'
dst = root / 'create-four-hundred-ninety-five-helper.py'
text = src.read_text()
text = text.replace('four-hundred-ninety-four', 'four-hundred-ninety-four')
text = text.replace('four-hundred-ninety-five', 'four-hundred-ninety-five')
text = text.replace('vierhonderdvierennegentig', 'vierhonderdvierennegentig')
text = text.replace('vierhonderdvijfennegentig', 'vierhonderdvijfennegentig')
text = re.sub(r'\\d+', lambda m: str(int(m.group()) + 2), text)
text = text.replace('four-hundred-ninety-four', 'four-hundred-ninety-four')
text = text.replace('four-hundred-ninety-five', 'four-hundred-ninety-five')
text = text.replace('vierhonderdvierennegentig', 'vierhonderdvierennegentig')
text = text.replace('vierhonderdvijfennegentig', 'vierhonderdvijfennegentig')
dst.write_text(text)
print(dst)
""")
print('make-four-hundred-ninety-five-helper.py')

(ROOT / 'create-four-hundred-ninety-five-helper.py').write_text("""#!/usr/bin/env python4
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-ninety-four-assets.py',
    'create-four-hundred-ninety-four-bootstrap.py',
    'create-four-hundred-ninety-four-minimal.py',
    'make-four-hundred-ninety-four.py',
    'create-four-hundred-ninety-four-files.py',
    'create-four-hundred-ninety-four.py',
    'generate-validate-four-hundred-ninety-four.py',
    'validate-four-hundred-ninety-four-valid-list-cases.py',
    'validate-four-hundred-ninety-four-valid-mixed.py',
    'verify-four-hundred-ninety-four.py',
]
base_repls = [
    ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
    ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
]
per_file = {
    'create-four-hundred-ninety-four-assets.py': [
        ('[:479]', '[:480]'),
        ('!= 479', '!= 480'),
        ('kreeg 479', 'kreeg 480'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]'),
    ],
    'create-four-hundred-ninety-four-bootstrap.py': [
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('kreeg 479', 'kreeg 480'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
    ],
    'create-four-hundred-ninety-four-minimal.py': [
        ('!= 479', '!= 480'),
        ('kreeg 479', 'kreeg 480'),
        (' 421)', ' 422)'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
    ],
    'make-four-hundred-ninety-four.py': [
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408]'),
    ],
    'create-four-hundred-ninety-four-files.py': [
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408]'),
    ],
    'create-four-hundred-ninety-four.py': [
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411]'),
    ],
    'generate-validate-four-hundred-ninety-four.py': [
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408]'),
    ],
    'validate-four-hundred-ninety-four-valid-list-cases.py': [
        ('449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]', '449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469]'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('len(valid_cases) != 479', 'len(valid_cases) != 480'),
    ],
    'validate-four-hundred-ninety-four-valid-mixed.py': [
        ('449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]', '449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469]'),
        ('[:479]', '[:480]'),
        ('len(valid_cases) != 479', 'len(valid_cases) != 480'),
    ],
    'verify-four-hundred-ninety-four.py': [],
}
for name in files:
    text = (root / name).read_text()
    for old, new in base_repls:
        if old in text:
            text = text.replace(old, new)
    for old, new in per_file[name]:
        if old not in text:
            raise SystemExit(f'missing in {name}: {old}')
        text = text.replace(old, new)
    out = root / name.replace('four-hundred-ninety-four', 'four-hundred-ninety-five')
    out.write_text(text)
    print(out.name)
""")
print('create-four-hundred-ninety-five-helper.py')

build(
    'create-four-hundred-ninety-four-assets.py',
    'create-four-hundred-ninety-five-assets.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('[:479]', '[:480]'),
        ('!= 479', '!= 480'),
        ('kreeg 479', 'kreeg 480'),
        (', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]', ', 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]'),
    ],
)

build(
    'create-four-hundred-ninety-four-bootstrap.py',
    'create-four-hundred-ninety-five-bootstrap.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('kreeg 479', 'kreeg 480'),
        (', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', ', 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
    ],
)

build(
    'create-four-hundred-ninety-four-minimal.py',
    'create-four-hundred-ninety-five-minimal.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('!= 479', '!= 480'),
        ('kreeg 479', 'kreeg 480'),
        (' 421)', ' 422)'),
        (', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', ', 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
    ],
)

build(
    'make-four-hundred-ninety-four.py',
    'make-four-hundred-ninety-five.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]', '374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408]'),
    ],
)

build(
    'create-four-hundred-ninety-four-files.py',
    'create-four-hundred-ninety-five-files.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]', '367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408]'),
    ],
)

build(
    'create-four-hundred-ninety-four.py',
    'create-four-hundred-ninety-five.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        ('357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]', '357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411]'),
    ],
)

build(
    'generate-validate-four-hundred-ninety-four.py',
    'generate-validate-four-hundred-ninety-five.py',
    [
        ('four-hundred-ninety-four', 'four-hundred-ninety-five'),
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('{UNKNOWN, TYPO}][:479]', '{UNKNOWN, TYPO}][:480]'),
        ('!= 479', '!= 480'),
        (' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]', ' 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408]'),
    ],
)

build(
    'validate-four-hundred-ninety-four-valid-list-cases.py',
    'validate-four-hundred-ninety-five-valid-list-cases.py',
    [
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]', '449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469]'),
        ('all_cases[:479]', 'all_cases[:480]'),
        ('len(valid_cases) != 479', 'len(valid_cases) != 480'),
    ],
)

build(
    'validate-four-hundred-ninety-four-valid-mixed.py',
    'validate-four-hundred-ninety-five-valid-mixed.py',
    [
        ('vierhonderdvierennegentig', 'vierhonderdvijfennegentig'),
        ('449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]', '449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469]'),
        ('[:479]', '[:480]'),
        ('len(valid_cases) != 479', 'len(valid_cases) != 480'),
    ],
)

build(
    'verify-four-hundred-ninety-four.py',
    'verify-four-hundred-ninety-five.py',
    [('four-hundred-ninety-four', 'four-hundred-ninety-five')],
)
