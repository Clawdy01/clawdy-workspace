#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-fifteen-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-fourteen.py', 'gen-four-hundred-fifteen.py', [
        ('four-hundred-fourteen', 'four-hundred-fifteen'),
        ('vierhonderdveertien', 'vierhonderdvijftien'),
        ('four-hundred-nine', 'four-hundred-fourteen'),
        ('vierhonderdnegen', 'vierhonderdveertien'),
        ('all_cases[:408]', 'all_cases[:408]'),
        ('{UNKNOWN, TYPO}][:408]', '{UNKNOWN, TYPO}][:408]'),
        ('!= 408', '!= 408'),
        ('kreeg 408', 'kreeg 408'),
        (' 408)', ' 408)'),
        (', 400, 401, 402]', ', 403, 404, 405, 406, 407]'),
    ]),
    ('verify-four-hundred-fourteen.py', 'verify-four-hundred-fifteen.py', [
        ('four-hundred-fourteen', 'four-hundred-fifteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-fifteen.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-fourteen'
slug_new = 'four-hundred-fifteen'
word_old = 'vierhonderdveertien'
word_new = 'vierhonderdvijftien'
files = [
    'create-four-hundred-fourteen-assets.py',
    'make-four-hundred-fourteen.py',
    'create-four-hundred-fourteen-files.py',
    'create-four-hundred-fourteen.py',
    'generate-validate-four-hundred-fourteen.py',
    'validate-four-hundred-fourteen-valid-list-cases.py',
    'validate-four-hundred-fourteen-valid-mixed.py',
    'verify-four-hundred-fourteen.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:401]', 'all_cases[:408]')
    text = text.replace('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:408]')
    text = text.replace('!= 401', '!= 408')
    text = text.replace('kreeg 401', 'kreeg 408')
    text = text.replace(' 401)', ' 408)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400]', ', 399, 403, 404, 405, 406, 407]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
