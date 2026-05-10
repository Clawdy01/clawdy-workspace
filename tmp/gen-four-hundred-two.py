#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred'
slug_new = 'four-hundred-two'
word_old = 'vierhonderd'
word_new = 'vierhonderdtwee'
files = [
    'create-four-hundred-assets.py',
    'make-four-hundred.py',
    'create-four-hundred-files.py',
    'create-four-hundred.py',
    'generate-validate-four-hundred.py',
    'validate-four-hundred-valid-list-cases.py',
    'validate-four-hundred-valid-mixed.py',
    'verify-four-hundred.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:395]', 'all_cases[:397]')
    text = text.replace('{UNKNOWN, TYPO}][:395]', '{UNKNOWN, TYPO}][:397]')
    text = text.replace('!= 395', '!= 397')
    text = text.replace('kreeg 395', 'kreeg 397')
    text = text.replace(' 395)', ' 397)')
    if 'ORDER =' in text:
        text = text.replace(', 393, 394]', ', 393, 394, 395, 396]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
