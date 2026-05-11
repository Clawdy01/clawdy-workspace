#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src_slug = 'four-hundred-sixty-eight'
dst_slug = 'four-hundred-seventy'
src_nl = 'vierhonderdachtenzestig'
dst_nl = 'vierhonderdzeventig'
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
    ('[:453]', '[:455]'),
    ('!= 453', '!= 455'),
    ('kreeg 453', 'kreeg 455'),
    (', 448, 449, 450, 451, 452]', ', 448, 449, 450, 451, 452, 453, 454]'),
]
for name in files:
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    out = root / name.replace(src_slug, dst_slug)
    out.write_text(text)
    print(out.name)
