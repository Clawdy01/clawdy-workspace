#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-five'
slug_new = 'three-hundred-ninety-six'
word_old = 'driehonderdvijfennegentig'
word_new = 'driehonderdzesennegentig'
files = [
    'create-three-hundred-ninety-five-assets.py',
    'make-three-hundred-ninety-five.py',
    'create-three-hundred-ninety-five-files.py',
    'create-three-hundred-ninety-five.py',
    'generate-validate-three-hundred-ninety-five.py',
    'validate-three-hundred-ninety-five-valid-list-cases.py',
    'validate-three-hundred-ninety-five-valid-mixed.py',
    'verify-three-hundred-ninety-five.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:390]', 'all_cases[:391]')
    text = text.replace('{UNKNOWN, TYPO}][:390]', '{UNKNOWN, TYPO}][:391]')
    text = text.replace('!= 390', '!= 391')
    text = text.replace('kreeg 390', 'kreeg 391')
    text = text.replace(' 390)', ' 391)')
    if 'ORDER =' in text:
        text = text.replace(', 388, 389]', ', 388, 389, 390]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
