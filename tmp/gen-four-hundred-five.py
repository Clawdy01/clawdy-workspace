#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-four'
slug_new = 'four-hundred-five'
word_old = 'vierhonderdvier'
word_new = 'vierhonderdvijf'
files = [
    'create-four-hundred-four-assets.py',
    'make-four-hundred-four.py',
    'create-four-hundred-four-files.py',
    'create-four-hundred-four.py',
    'generate-validate-four-hundred-four.py',
    'validate-four-hundred-four-valid-list-cases.py',
    'validate-four-hundred-four-valid-mixed.py',
    'verify-four-hundred-four.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:399]', 'all_cases[:400]')
    text = text.replace('{UNKNOWN, TYPO}][:399]', '{UNKNOWN, TYPO}][:400]')
    text = text.replace('!= 399', '!= 400')
    text = text.replace('kreeg 399', 'kreeg 400')
    text = text.replace(' 399)', ' 400)')
    if 'ORDER =' in text:
        text = text.replace(', 396, 397, 398]', ', 396, 397, 398, 399]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
