#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-five'
slug_new = 'four-hundred-six'
word_old = 'vierhonderdvijf'
word_new = 'vierhonderdzes'
files = [
    'create-four-hundred-five-assets.py',
    'make-four-hundred-five.py',
    'create-four-hundred-five-files.py',
    'create-four-hundred-five.py',
    'generate-validate-four-hundred-five.py',
    'validate-four-hundred-five-valid-list-cases.py',
    'validate-four-hundred-five-valid-mixed.py',
    'verify-four-hundred-five.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:400]', 'all_cases[:401]')
    text = text.replace('{UNKNOWN, TYPO}][:400]', '{UNKNOWN, TYPO}][:401]')
    text = text.replace('!= 400', '!= 401')
    text = text.replace('kreeg 400', 'kreeg 401')
    text = text.replace(' 400)', ' 401)')
    if 'ORDER =' in text:
        text = text.replace(', 397, 398, 399]', ', 397, 398, 399, 400]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
