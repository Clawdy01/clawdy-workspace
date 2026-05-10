#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-two'
slug_new = 'four-hundred-three'
word_old = 'vierhonderdtwee'
word_new = 'vierhonderddrie'
files = [
    'create-four-hundred-two-assets.py',
    'make-four-hundred-two.py',
    'create-four-hundred-two-files.py',
    'create-four-hundred-two.py',
    'generate-validate-four-hundred-two.py',
    'validate-four-hundred-two-valid-list-cases.py',
    'validate-four-hundred-two-valid-mixed.py',
    'verify-four-hundred-two.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:397]', 'all_cases[:398]')
    text = text.replace('{UNKNOWN, TYPO}][:397]', '{UNKNOWN, TYPO}][:398]')
    text = text.replace('!= 397', '!= 398')
    text = text.replace('kreeg 397', 'kreeg 398')
    text = text.replace(' 397)', ' 398)')
    if 'ORDER =' in text:
        text = text.replace(', 395, 396]', ', 395, 396, 397]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
