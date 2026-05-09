#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-three'
slug_new = 'three-hundred-ninety-four'
word_old = 'driehonderddrieënnegentig'
word_new = 'driehonderdvierennegentig'
files = [
    'create-three-hundred-ninety-three-assets.py',
    'make-three-hundred-ninety-three.py',
    'create-three-hundred-ninety-three-files.py',
    'create-three-hundred-ninety-three.py',
    'generate-validate-three-hundred-ninety-three.py',
    'validate-three-hundred-ninety-three-valid-list-cases.py',
    'validate-three-hundred-ninety-three-valid-mixed.py',
    'verify-three-hundred-ninety-three.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:388]', 'all_cases[:389]')
    text = text.replace('{UNKNOWN, TYPO}][:388]', '{UNKNOWN, TYPO}][:389]')
    text = text.replace('!= 388', '!= 389')
    text = text.replace('kreeg 388', 'kreeg 389')
    text = text.replace(' 388)', ' 389)')
    if 'ORDER =' in text:
        text = text.replace(', 386, 387]', ', 386, 387, 388]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
