#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-twelve-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-eleven.py', 'gen-four-hundred-twelve.py', [
        ('four-hundred-eleven', 'four-hundred-twelve'),
        ('vierhonderdelf', 'vierhonderdtwaalf'),
        ('four-hundred-nine', 'four-hundred-eleven'),
        ('vierhonderdnegen', 'vierhonderdelf'),
        ('all_cases[:403]', 'all_cases[:405]'),
        ('{UNKNOWN, TYPO}][:403]', '{UNKNOWN, TYPO}][:405]'),
        ('!= 403', '!= 405'),
        ('kreeg 403', 'kreeg 405'),
        (' 403)', ' 405)'),
        (', 400, 401, 402]', ', 400, 401, 402, 403, 404]'),
    ]),
    ('verify-four-hundred-eleven.py', 'verify-four-hundred-twelve.py', [
        ('four-hundred-eleven', 'four-hundred-twelve'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-twelve.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-eleven'
slug_new = 'four-hundred-twelve'
word_old = 'vierhonderdelf'
word_new = 'vierhonderdtwaalf'
files = [
    'create-four-hundred-eleven-assets.py',
    'make-four-hundred-eleven.py',
    'create-four-hundred-eleven-files.py',
    'create-four-hundred-eleven.py',
    'generate-validate-four-hundred-eleven.py',
    'validate-four-hundred-eleven-valid-list-cases.py',
    'validate-four-hundred-eleven-valid-mixed.py',
    'verify-four-hundred-eleven.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:401]', 'all_cases[:403]')
    text = text.replace('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:403]')
    text = text.replace('!= 401', '!= 403')
    text = text.replace('kreeg 401', 'kreeg 403')
    text = text.replace(' 401)', ' 403)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400]', ', 398, 399, 400, 401, 402]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
