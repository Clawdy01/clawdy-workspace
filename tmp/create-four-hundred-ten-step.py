#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-ten-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-nine.py', 'gen-four-hundred-ten.py', [
        ('four-hundred-nine', 'four-hundred-ten'),
        ('vierhonderdnegen', 'vierhonderdtien'),
        ('four-hundred-eight', 'four-hundred-nine'),
        ('vierhonderdacht', 'vierhonderdnegen'),
        ('all_cases[:402]', 'all_cases[:403]'),
        ('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:403]'),
        ('!= 402', '!= 403'),
        ('kreeg 402', 'kreeg 403'),
        (' 402)', ' 403)'),
        (', 399, 400, 401]', ', 399, 400, 401, 402]'),
    ]),
    ('verify-four-hundred-nine.py', 'verify-four-hundred-ten.py', [
        ('four-hundred-nine', 'four-hundred-ten'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-ten.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-nine'
slug_new = 'four-hundred-ten'
word_old = 'vierhonderdnegen'
word_new = 'vierhonderdtien'
files = [
    'create-four-hundred-nine-assets.py',
    'make-four-hundred-nine.py',
    'create-four-hundred-nine-files.py',
    'create-four-hundred-nine.py',
    'generate-validate-four-hundred-nine.py',
    'validate-four-hundred-nine-valid-list-cases.py',
    'validate-four-hundred-nine-valid-mixed.py',
    'verify-four-hundred-nine.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:402]', 'all_cases[:403]')
    text = text.replace('{UNKNOWN, TYPO}][:402]', '{UNKNOWN, TYPO}][:403]')
    text = text.replace('!= 402', '!= 403')
    text = text.replace('kreeg 402', 'kreeg 403')
    text = text.replace(' 402)', ' 403)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400, 401]', ', 398, 399, 400, 401, 402]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
