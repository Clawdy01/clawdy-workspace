#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-thirteen-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-twelve.py', 'gen-four-hundred-thirteen.py', [
        ('four-hundred-twelve', 'four-hundred-thirteen'),
        ('vierhonderdtwaalf', 'vierhonderddertien'),
        ('four-hundred-nine', 'four-hundred-twelve'),
        ('vierhonderdnegen', 'vierhonderdtwaalf'),
        ('all_cases[:406]', 'all_cases[:406]'),
        ('{UNKNOWN, TYPO}][:406]', '{UNKNOWN, TYPO}][:406]'),
        ('!= 406', '!= 406'),
        ('kreeg 406', 'kreeg 406'),
        (' 406)', ' 406)'),
        (', 400, 401, 402]', ', 401, 402, 403, 404, 405]'),
    ]),
    ('verify-four-hundred-twelve.py', 'verify-four-hundred-thirteen.py', [
        ('four-hundred-twelve', 'four-hundred-thirteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-thirteen.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-twelve'
slug_new = 'four-hundred-thirteen'
word_old = 'vierhonderdtwaalf'
word_new = 'vierhonderddertien'
files = [
    'create-four-hundred-twelve-assets.py',
    'make-four-hundred-twelve.py',
    'create-four-hundred-twelve-files.py',
    'create-four-hundred-twelve.py',
    'generate-validate-four-hundred-twelve.py',
    'validate-four-hundred-twelve-valid-list-cases.py',
    'validate-four-hundred-twelve-valid-mixed.py',
    'verify-four-hundred-twelve.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:401]', 'all_cases[:406]')
    text = text.replace('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:406]')
    text = text.replace('!= 401', '!= 406')
    text = text.replace('kreeg 401', 'kreeg 406')
    text = text.replace(' 401)', ' 406)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400]', ', 399, 401, 402, 403, 404, 405]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
