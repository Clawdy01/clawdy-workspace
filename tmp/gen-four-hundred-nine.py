#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-eight'
slug_new = 'four-hundred-nine'
word_old = 'vierhonderdacht'
word_new = 'vierhonderdnegen'
files = [
    'create-four-hundred-eight-assets.py',
    'make-four-hundred-eight.py',
    'create-four-hundred-eight-files.py',
    'create-four-hundred-eight.py',
    'generate-validate-four-hundred-eight.py',
    'validate-four-hundred-eight-valid-list-cases.py',
    'validate-four-hundred-eight-valid-mixed.py',
    'verify-four-hundred-eight.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:400]', 'all_cases[:402]')
    text = text.replace('{UNKNOWN, TYPO}][:400]', '{UNKNOWN, TYPO}][:402]')
    text = text.replace('!= 400', '!= 402')
    text = text.replace('kreeg 400', 'kreeg 402')
    text = text.replace(' 400)', ' 402)')
    if 'ORDER =' in text:
        text = text.replace(', 397, 398, 399]', ', 397, 398, 399, 400, 401]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
