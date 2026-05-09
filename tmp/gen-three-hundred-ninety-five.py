#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
slug_old = 'three-hundred-ninety-four'
slug_new = 'three-hundred-ninety-five'
word_old = 'driehonderdvierennegentig'
word_new = 'driehonderdvijfennegentig'
files = [
    'create-three-hundred-ninety-four-assets.py',
    'make-three-hundred-ninety-four.py',
    'create-three-hundred-ninety-four-files.py',
    'create-three-hundred-ninety-four.py',
    'generate-validate-three-hundred-ninety-four.py',
    'validate-three-hundred-ninety-four-valid-list-cases.py',
    'validate-three-hundred-ninety-four-valid-mixed.py',
    'verify-three-hundred-ninety-four.py',
]
for name in files:
    text = (root / name).read_text()
    text = text.replace(slug_old, slug_new).replace(word_old, word_new)
    text = text.replace('all_cases[:389]', 'all_cases[:390]')
    text = text.replace('{UNKNOWN, TYPO}][:389]', '{UNKNOWN, TYPO}][:390]')
    text = text.replace('!= 389', '!= 390')
    text = text.replace('kreeg 389', 'kreeg 390')
    text = text.replace(' 389)', ' 390)')
    if 'ORDER =' in text:
        text = text.replace(', 387, 388]', ', 387, 388, 389]')
    (root / name.replace(slug_old, slug_new)).write_text(text)
