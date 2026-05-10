#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-three'
slug_new = 'four-hundred-four'
word_old = 'vierhonderddrie'
word_new = 'vierhonderdvier'
files = [
    'create-four-hundred-three-assets.py',
    'make-four-hundred-three.py',
    'create-four-hundred-three-files.py',
    'create-four-hundred-three.py',
    'generate-validate-four-hundred-three.py',
    'validate-four-hundred-three-valid-list-cases.py',
    'validate-four-hundred-three-valid-mixed.py',
    'verify-four-hundred-three.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:398]', 'all_cases[:399]')
    text = text.replace('{UNKNOWN, TYPO}][:398]', '{UNKNOWN, TYPO}][:399]')
    text = text.replace('!= 398', '!= 399')
    text = text.replace('kreeg 398', 'kreeg 399')
    text = text.replace(' 398)', ' 399)')
    if 'ORDER =' in text:
        text = text.replace(', 396, 397]', ', 396, 397, 398]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
