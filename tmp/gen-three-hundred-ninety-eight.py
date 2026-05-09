#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-seven'
slug_new = 'three-hundred-ninety-eight'
word_old = 'driehonderdzevenennegentig'
word_new = 'driehonderdachtennegentig'
files = [
    'create-three-hundred-ninety-seven-assets.py',
    'make-three-hundred-ninety-seven.py',
    'create-three-hundred-ninety-seven-files.py',
    'create-three-hundred-ninety-seven.py',
    'generate-validate-three-hundred-ninety-seven.py',
    'validate-three-hundred-ninety-seven-valid-list-cases.py',
    'validate-three-hundred-ninety-seven-valid-mixed.py',
    'verify-three-hundred-ninety-seven.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:392]', 'all_cases[:393]')
    text = text.replace('{UNKNOWN, TYPO}][:392]', '{UNKNOWN, TYPO}][:393]')
    text = text.replace('!= 392', '!= 393')
    text = text.replace('kreeg 392', 'kreeg 393')
    text = text.replace(' 392)', ' 393)')
    if 'ORDER =' in text:
        text = text.replace(', 390, 391]', ', 390, 391, 392]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
