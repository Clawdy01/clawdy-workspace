#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src_slug = 'four-hundred-seventy'
dst_slug = 'four-hundred-seventy-one'
src_nl = 'vierhonderdzeventig'
dst_nl = 'vierhonderdeenenzeventig'
files = [
    f'create-{src_slug}-assets.py',
    f'create-{src_slug}-bootstrap.py',
    f'create-{src_slug}-minimal.py',
    f'make-{src_slug}.py',
    f'create-{src_slug}-files.py',
    f'create-{src_slug}.py',
    f'generate-validate-{src_slug}.py',
    f'validate-{src_slug}-valid-list-cases.py',
    f'validate-{src_slug}-valid-mixed.py',
    f'verify-{src_slug}.py',
]
repls = [
    (src_slug, dst_slug),
    (src_nl, dst_nl),
    ('[:455]', '[:456]'),
    ('!= 455', '!= 456'),
    ('kreeg 455', 'kreeg 456'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    if name == f'create-{src_slug}-assets.py':
        old = ', 443, 444, 445, 446, 447, 448]'
        new = ', 443, 444, 445, 446, 447, 448, 449]'
        if old not in text:
            raise SystemExit(f'mis expected ORDER tail in {name}')
        text = text.replace(old, new, 1)
    if name == f'create-{src_slug}-bootstrap.py':
        old = ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444]'
        new = ', 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445]'
        if old not in text:
            raise SystemExit(f'mis expected bootstrap tail in {name}')
        text = text.replace(old, new, 1)
    if name == f'create-{src_slug}-minimal.py':
        old = ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444]'
        new = ', 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445]'
        if old not in text:
            raise SystemExit(f'mis expected minimal tail in {name}')
        text = text.replace(old, new, 1)
    if name == f'create-{src_slug}.py':
        old = '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]'
        new = '356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388]'
        if old not in text:
            raise SystemExit(f'mis expected create tail in {name}')
        text = text.replace(old, new, 1)
    if name in {
        f'validate-{src_slug}-valid-list-cases.py',
        f'validate-{src_slug}-valid-mixed.py',
    }:
        old = ', 443, 444]'
        new = ', 443, 444, 445]'
        if old not in text:
            raise SystemExit(f'mis expected validate tail in {name}')
        text = text.replace(old, new, 1)
    out = root / name.replace(src_slug, dst_slug)
    out.write_text(text)
    print(out.name)
