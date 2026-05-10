#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-eleven-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-ten.py', 'gen-four-hundred-eleven.py', [
        ('four-hundred-ten', 'four-hundred-eleven'),
        ('vierhonderdtien', 'vierhonderdelf'),
        ('four-hundred-nine', 'four-hundred-ten'),
        ('vierhonderdnegen', 'vierhonderdtien'),
        ('all_cases[:403]', 'all_cases[:404]'),
        ('{UNKNOWN, TYPO}][:403]', '{UNKNOWN, TYPO}][:404]'),
        ('!= 403', '!= 404'),
        ('kreeg 403', 'kreeg 404'),
        (' 403)', ' 404)'),
        (', 400, 401, 402]', ', 400, 401, 402, 403]'),
    ]),
    ('verify-four-hundred-ten.py', 'verify-four-hundred-eleven.py', [
        ('four-hundred-ten', 'four-hundred-eleven'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-eleven.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-ten'
slug_new = 'four-hundred-eleven'
word_old = 'vierhonderdtien'
word_new = 'vierhonderdelf'
files = [
    'create-four-hundred-ten-assets.py',
    'make-four-hundred-ten.py',
    'create-four-hundred-ten-files.py',
    'create-four-hundred-ten.py',
    'generate-validate-four-hundred-ten.py',
    'validate-four-hundred-ten-valid-list-cases.py',
    'validate-four-hundred-ten-valid-mixed.py',
    'verify-four-hundred-ten.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:401]', 'all_cases[:402]')
    text = text.replace('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:402]')
    text = text.replace('!= 401', '!= 402')
    text = text.replace('kreeg 401', 'kreeg 402')
    text = text.replace(' 401)', ' 402)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400]', ', 398, 399, 400, 401]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
