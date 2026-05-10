#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')

(root / 'make-four-hundred-sixteen-chain.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
for src, dst, repls in [
    ('gen-four-hundred-fifteen.py', 'gen-four-hundred-sixteen.py', [
        ('four-hundred-fifteen', 'four-hundred-sixteen'),
        ('vierhonderdvijftien', 'vierhonderdzestien'),
        ('four-hundred-nine', 'four-hundred-fifteen'),
        ('vierhonderdnegen', 'vierhonderdvijftien'),
        ('all_cases[:409]', 'all_cases[:409]'),
        ('{UNKNOWN, TYPO}][:409]', '{UNKNOWN, TYPO}][:409]'),
        ('!= 409', '!= 409'),
        ('kreeg 409', 'kreeg 409'),
        (' 409)', ' 409)'),
        (', 400, 401, 402]', ', 404, 405, 406, 407, 408]'),
    ]),
    ('verify-four-hundred-fifteen.py', 'verify-four-hundred-sixteen.py', [
        ('four-hundred-fifteen', 'four-hundred-sixteen'),
    ]),
]:
    text = (root / src).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / dst).write_text(text)
""")

(root / 'gen-four-hundred-sixteen.py').write_text("""#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-fifteen'
slug_new = 'four-hundred-sixteen'
word_old = 'vierhonderdvijftien'
word_new = 'vierhonderdzestien'
files = [
    'create-four-hundred-fifteen-assets.py',
    'make-four-hundred-fifteen.py',
    'create-four-hundred-fifteen-files.py',
    'create-four-hundred-fifteen.py',
    'generate-validate-four-hundred-fifteen.py',
    'validate-four-hundred-fifteen-valid-list-cases.py',
    'validate-four-hundred-fifteen-valid-mixed.py',
    'verify-four-hundred-fifteen.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:401]', 'all_cases[:409]')
    text = text.replace('{UNKNOWN, TYPO}][:401]', '{UNKNOWN, TYPO}][:409]')
    text = text.replace('!= 401', '!= 409')
    text = text.replace('kreeg 401', 'kreeg 409')
    text = text.replace(' 401)', ' 409)')
    if 'ORDER =' in text:
        text = text.replace(', 398, 399, 400]', ', 399, 404, 405, 406, 407, 408]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
""")
