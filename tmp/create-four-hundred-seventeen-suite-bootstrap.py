#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-sixteen-suite.py'
dst = root / 'create-four-hundred-seventeen-suite.py'
text = src.read_text()
repls = [
    ('create-four-hundred-fifteen-step-bootstrap.py', 'create-four-hundred-sixteen-step-bootstrap.py'),
    ('create-four-hundred-sixteen-step-bootstrap.py', 'create-four-hundred-seventeen-step-bootstrap.py'),
    ('four-hundred-fourteen', 'four-hundred-fifteen'),
    ('four-hundred-fifteen', 'four-hundred-sixteen'),
    ('four-hundred-sixteen', 'four-hundred-seventeen'),
    ('vierhonderdveertien', 'vierhonderdvijftien'),
    ('vierhonderdvijftien', 'vierhonderdzestien'),
    ('vierhonderdzestien', 'vierhonderdzeventien'),
    ('all_cases[:409]', 'all_cases[:410]'),
    ('{UNKNOWN, TYPO}][:409]', '{UNKNOWN, TYPO}][:410]'),
    ('!= 409', '!= 410'),
    ('kreeg 409', 'kreeg 410'),
    (' 409)', ' 410)'),
    (', 404, 405, 406, 407, 408]', ', 405, 406, 407, 408, 409]'),
    ('all_cases[:407]', 'all_cases[:408]'),
    ('{UNKNOWN, TYPO}][:407]', '{UNKNOWN, TYPO}][:408]'),
    ('!= 407', '!= 408'),
    ('kreeg 407', 'kreeg 408'),
    (' 407)', ' 408)'),
    (', 402, 403, 404, 405, 406]', ', 403, 404, 405, 406, 407]'),
]
for old, new in repls:
    text = text.replace(old, new)
dst.write_text(text)
