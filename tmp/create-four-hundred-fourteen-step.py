#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-fourteen-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-thirteen.py', 'gen-four-hundred-fourteen.py', [
        ('four-hundred-thirteen', 'four-hundred-fourteen'),
        ('vierhonderddertien', 'vierhonderdveertien'),
        ('four-hundred-nine', 'four-hundred-thirteen'),
        ('vierhonderdnegen', 'vierhonderddertien'),
        ('all_cases[:407]', 'all_cases[:407]'),
        ('{UNKNOWN, TYPO}][:407]', '{UNKNOWN, TYPO}][:407]'),
        ('!= 407', '!= 407'),
        ('kreeg 407', 'kreeg 407'),
        (' 407)', ' 407)'),
        (', 400, 401, 402]', ', 402, 403, 404, 405, 406]'),
    ]),
    ('verify-four-hundred-thirteen.py', 'verify-four-hundred-fourteen.py', [
        ('four-hundred-thirteen', 'four-hundred-fourteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-fourteen.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-thirteen'
slug_new = 'four-hundred-fourteen'
word_old = 'vierhonderddertien'
word_new = 'vierhonderdveertien'
files = [
    'create-four-hundred-thirteen-assets.py',
    'make-four-hundred-thirteen.py',
    'create-four-hundred-thirteen-files.py',
    'create-four-hundred-thirteen.py',
    'generate-validate-four-hundred-thirteen.py',
    'validate-four-hundred-thirteen-valid-list-cases.py',
    'validate-four-hundred-thirteen-valid-mixed.py',
    'verify-four-hundred-thirteen.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:401]', 'all_cases[:407]')
    text = text.replace('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:407]')
    text = text.replace('!= 401', '!= 407')
    text = text.replace('kreeg 401', 'kreeg 407')
    text = text.replace(' 401)', ' 407)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400]', ', 399, 402, 403, 404, 405, 406]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
