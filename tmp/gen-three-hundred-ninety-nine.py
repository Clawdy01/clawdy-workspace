#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-eight'
slug_new = 'three-hundred-ninety-nine'
word_old = 'driehonderdachtennegentig'
word_new = 'driehonderdnegenennegentig'
files = [
    'create-three-hundred-ninety-eight-assets.py',
    'make-three-hundred-ninety-eight.py',
    'create-three-hundred-ninety-eight-files.py',
    'create-three-hundred-ninety-eight.py',
    'generate-validate-three-hundred-ninety-eight.py',
    'validate-three-hundred-ninety-eight-valid-list-cases.py',
    'validate-three-hundred-ninety-eight-valid-mixed.py',
    'verify-three-hundred-ninety-eight.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:393]', 'all_cases[:394]')
    text = text.replace('{UNKNOWN, TYPO}][:393]', '{UNKNOWN, TYPO}][:394]')
    text = text.replace('!= 393', '!= 394')
    text = text.replace('kreeg 393', 'kreeg 394')
    text = text.replace(' 393)', ' 394)')
    if 'ORDER =' in text:
        text = text.replace(', 391, 392]', ', 391, 392, 393]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
