#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'four-hundred-ten'
slug_new = 'four-hundred-sixteen'
word_old = 'vierhonderdtien'
word_new = 'vierhonderdzestien'
files = [
    'create-four-hundred-ten-assets.py',
    'make-four-hundred-ten.py',
    'create-four-hundred-ten-files.py',
    'create-four-hundred-ten.py',
    'generate-validate-four-hundred-ten.py',
    'validate-four-hundred-ten-valid-list-cases.py',
    'validate-four-hundred-ten-valid-mixed.py',
    'verify-four-hundred-ten.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:400]', 'all_cases[:404]')
    text = text.replace('{UNKNOWN, TYPO}][:400]', '{UNKNOWN, TYPO}][:404]')
    text = text.replace('!= 400', '!= 404')
    text = text.replace('kreeg 400', 'kreeg 404')
    text = text.replace(' 400)', ' 404)')
    if 'ORDER =' in text:
        text = text.replace(', 397, 398, 399]', ', 397, 398, 399, 400, 401, 402, 403]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
