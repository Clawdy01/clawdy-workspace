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


(ROOT / 'make-four-hundred-ninety-four-helper.py').write_text("""#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-ninety-three-helper.py'
dst = root / 'create-four-hundred-ninety-four-helper.py'
text = src.read_text()
text = text.replace('four-hundred-ninety-three', '__SRC_SLUG__')
text = text.replace('four-hundred-ninety-four', '__DST_SLUG__')
text = text.replace('vierhonderddrieënnegentig', '__SRC_DUTCH__')
text = text.replace('vierhonderdvierennegentig', '__DST_DUTCH__')
text = re.sub(r'\\d+', lambda m: str(int(m.group()) + 1), text)
text = text.replace('__SRC_SLUG__', 'four-hundred-ninety-three')
text = text.replace('__DST_SLUG__', 'four-hundred-ninety-four')
text = text.replace('__SRC_DUTCH__', 'vierhonderddrieënnegentig')
text = text.replace('__DST_DUTCH__', 'vierhonderdvierennegentig')
dst.write_text(text)
print(dst)
""")
print('make-four-hundred-ninety-four-helper.py')

(ROOT / 'create-four-hundred-ninety-four-helper.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
files = [
    'create-four-hundred-ninety-three-assets.py',
    'create-four-hundred-ninety-three-bootstrap.py',
    'create-four-hundred-ninety-three-minimal.py',
    'make-four-hundred-ninety-three.py',
    'create-four-hundred-ninety-three-files.py',
    'create-four-hundred-ninety-three.py',
    'generate-validate-four-hundred-ninety-three.py',
    'validate-four-hundred-ninety-three-valid-list-cases.py',
    'validate-four-hundred-ninety-three-valid-mixed.py',
    'verify-four-hundred-ninety-three.py',
]
base_repls = [
    ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
    ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
]
per_file = {
    'create-four-hundred-ninety-three-assets.py': [
        ('[:478]', '[:479]'),
        ('!= 478', '!= 479'),
        ('kreeg 478', 'kreeg 479'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]'),
    ],
    'create-four-hundred-ninety-three-bootstrap.py': [
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('kreeg 478', 'kreeg 479'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]'),
    ],
    'create-four-hundred-ninety-three-minimal.py': [
        ('!= 478', '!= 479'),
        ('kreeg 478', 'kreeg 479'),
        (' 420)', ' 421)'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]'),
    ],
    'make-four-hundred-ninety-three.py': [
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]'),
    ],
    'create-four-hundred-ninety-three-files.py': [
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]'),
    ],
    'create-four-hundred-ninety-three.py': [
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]'),
    ],
    'generate-validate-four-hundred-ninety-three.py': [
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]'),
    ],
    'validate-four-hundred-ninety-three-valid-list-cases.py': [
        ('448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', '448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('len(valid_cases) != 478', 'len(valid_cases) != 479'),
    ],
    'validate-four-hundred-ninety-three-valid-mixed.py': [
        ('448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', '448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
        ('[:478]', '[:479]'),
        ('len(valid_cases) != 478', 'len(valid_cases) != 479'),
    ],
    'verify-four-hundred-ninety-three.py': [],
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
    out = root / name.replace('four-hundred-ninety-three', 'four-hundred-ninety-four')
    out.write_text(text)
    print(out.name)
""")
print('create-four-hundred-ninety-four-helper.py')

build(
    'create-four-hundred-ninety-three-assets.py',
    'create-four-hundred-ninety-four-assets.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('[:478]', '[:479]'),
        ('!= 478', '!= 479'),
        ('kreeg 478', 'kreeg 479'),
        (', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]', ', 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471]'),
    ],
)

build(
    'create-four-hundred-ninety-three-bootstrap.py',
    'create-four-hundred-ninety-four-bootstrap.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('kreeg 478', 'kreeg 479'),
        (', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]', ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]'),
    ],
)

build(
    'create-four-hundred-ninety-three-minimal.py',
    'create-four-hundred-ninety-four-minimal.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('!= 478', '!= 479'),
        ('kreeg 478', 'kreeg 479'),
        (' 420)', ' 421)'),
        (', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466]', ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]'),
    ],
)

build(
    'make-four-hundred-ninety-three.py',
    'make-four-hundred-ninety-four.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406]', '373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]'),
    ],
)

build(
    'create-four-hundred-ninety-three-files.py',
    'create-four-hundred-ninety-four-files.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406]', '366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]'),
    ],
)

build(
    'create-four-hundred-ninety-three.py',
    'create-four-hundred-ninety-four.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        ('356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409]', '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410]'),
    ],
)

build(
    'generate-validate-four-hundred-ninety-three.py',
    'generate-validate-four-hundred-ninety-four.py',
    [
        ('four-hundred-ninety-three', 'four-hundred-ninety-four'),
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('{UNKNOWN, TYPO}][:478]', '{UNKNOWN, TYPO}][:479]'),
        ('!= 478', '!= 479'),
        (' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407]'),
    ],
)

build(
    'validate-four-hundred-ninety-three-valid-list-cases.py',
    'validate-four-hundred-ninety-four-valid-list-cases.py',
    [
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', '448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
        ('all_cases[:478]', 'all_cases[:479]'),
        ('len(valid_cases) != 478', 'len(valid_cases) != 479'),
    ],
)

build(
    'validate-four-hundred-ninety-three-valid-mixed.py',
    'validate-four-hundred-ninety-four-valid-mixed.py',
    [
        ('vierhonderddrieënnegentig', 'vierhonderdvierennegentig'),
        ('448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467]', '448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468]'),
        ('[:478]', '[:479]'),
        ('len(valid_cases) != 478', 'len(valid_cases) != 479'),
    ],
)

build(
    'verify-four-hundred-ninety-three.py',
    'verify-four-hundred-ninety-four.py',
    [('four-hundred-ninety-three', 'four-hundred-ninety-four')],
)
