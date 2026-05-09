#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-nine'
slug_new = 'four-hundred'
word_old = 'driehonderdnegenennegentig'
word_new = 'vierhonderd'
files = [
    'create-three-hundred-ninety-nine-assets.py',
    'make-three-hundred-ninety-nine.py',
    'create-three-hundred-ninety-nine-files.py',
    'create-three-hundred-ninety-nine.py',
    'generate-validate-three-hundred-ninety-nine.py',
    'validate-three-hundred-ninety-nine-valid-list-cases.py',
    'validate-three-hundred-ninety-nine-valid-mixed.py',
    'verify-three-hundred-ninety-nine.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:394]', 'all_cases[:395]')
    text = text.replace('{UNKNOWN, TYPO}][:394]', '{UNKNOWN, TYPO}][:395]')
    text = text.replace('!= 394', '!= 395')
    text = text.replace('kreeg 394', 'kreeg 395')
    text = text.replace(' 394)', ' 395)')
    if 'ORDER =' in text:
        text = text.replace(', 392, 393]', ', 392, 393, 394]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
