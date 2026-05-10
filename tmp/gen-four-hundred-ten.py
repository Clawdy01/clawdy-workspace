#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-nine'
slug_new = 'four-hundred-ten'
word_old = 'vierhonderdnegen'
word_new = 'vierhonderdtien'
files = [
    'create-four-hundred-nine-assets.py',
    'make-four-hundred-nine.py',
    'create-four-hundred-nine-files.py',
    'create-four-hundred-nine.py',
    'generate-validate-four-hundred-nine.py',
    'validate-four-hundred-nine-valid-list-cases.py',
    'validate-four-hundred-nine-valid-mixed.py',
    'verify-four-hundred-nine.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:400]', 'all_cases[:403]')
    text = text.replace('{UNKNOWN, TYPO}][:400]', '{UNKNOWN, TYPO}][:403]')
    text = text.replace('!= 400', '!= 403')
    text = text.replace('kreeg 400', 'kreeg 403')
    text = text.replace(' 400)', ' 403)')
    if 'ORDER =' in text:
        text = text.replace(', 397, 398, 399]', ', 397, 398, 399, 400, 401, 402]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
