#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-six'
slug_new = 'three-hundred-ninety-seven'
word_old = 'driehonderdzesennegentig'
word_new = 'driehonderdzevenennegentig'
files = [
    'gen-three-hundred-ninety-six.py',
    'create-three-hundred-ninety-six-assets.py',
    'make-three-hundred-ninety-six.py',
    'create-three-hundred-ninety-six-files.py',
    'create-three-hundred-ninety-six.py',
    'generate-validate-three-hundred-ninety-six.py',
    'validate-three-hundred-ninety-six-valid-list-cases.py',
    'validate-three-hundred-ninety-six-valid-mixed.py',
    'verify-three-hundred-ninety-six.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:391]', 'all_cases[:392]')
    text = text.replace('{UNKNOWN, TYPO}][:391]', '{UNKNOWN, TYPO}][:392]')
    text = text.replace('!= 391', '!= 392')
    text = text.replace('kreeg 391', 'kreeg 392')
    text = text.replace(' 391)', ' 392)')
    if 'ORDER =' in text:
        text = text.replace(', 389, 390]', ', 389, 390, 391]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
