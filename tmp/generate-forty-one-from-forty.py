#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-six-hundred-forty-from-639.py'
dst = root / 'create-six-hundred-forty-one-from-640.py'
text = src.read_text()
replacements = [
    ("'create-six-hundred-thirty-nine-assets.py'", "'create-six-hundred-forty-assets.py'"),
    ("'create-six-hundred-forty-assets.py'", "'create-six-hundred-forty-one-assets.py'"),
    ("'create-six-hundred-thirty-nine-bootstrap.py'", "'create-six-hundred-forty-bootstrap.py'"),
    ("'create-six-hundred-forty-bootstrap.py'", "'create-six-hundred-forty-one-bootstrap.py'"),
    ("'create-six-hundred-thirty-nine-minimal.py'", "'create-six-hundred-forty-minimal.py'"),
    ("'create-six-hundred-forty-minimal.py'", "'create-six-hundred-forty-one-minimal.py'"),
    ("'make-six-hundred-thirty-nine.py'", "'make-six-hundred-forty.py'"),
    ("'make-six-hundred-forty.py'", "'make-six-hundred-forty-one.py'"),
    ("'create-six-hundred-thirty-nine-files.py'", "'create-six-hundred-forty-files.py'"),
    ("'create-six-hundred-forty-files.py'", "'create-six-hundred-forty-one-files.py'"),
    ("'create-six-hundred-thirty-nine.py'", "'create-six-hundred-forty.py'"),
    ("'create-six-hundred-forty.py'", "'create-six-hundred-forty-one.py'"),
    ("'generate-validate-six-hundred-thirty-nine.py'", "'generate-validate-six-hundred-forty.py'"),
    ("'generate-validate-six-hundred-forty.py'", "'generate-validate-six-hundred-forty-one.py'"),
    ("'validate-six-hundred-thirty-nine-valid-list-cases.py'", "'validate-six-hundred-forty-valid-list-cases.py'"),
    ("'validate-six-hundred-forty-valid-list-cases.py'", "'validate-six-hundred-forty-one-valid-list-cases.py'"),
    ("'validate-six-hundred-thirty-nine-valid-mixed.py'", "'validate-six-hundred-forty-valid-mixed.py'"),
    ("'validate-six-hundred-forty-valid-mixed.py'", "'validate-six-hundred-forty-one-valid-mixed.py'"),
    ('six-hundred-forty', 'six-hundred-forty-one'),
    ('zeshonderdveertig', 'zeshonderdeenenveertig'),
    ('[:625]', '[:626]'),
    ('!= 625', '!= 626'),
    ('kreeg 625', 'kreeg 626'),
    ('612, 613, 614, 615, 616', '613, 614, 615, 616, 617'),
    ('608, 609, 610, 611, 612', '609, 610, 611, 612, 613'),
    ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ('610, 611, 612, 613, 614', '611, 612, 613, 614, 615'),
    ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
    ('verify-six-hundred-thirty-nine.py', 'verify-six-hundred-forty.py'),
    ('verify-six-hundred-forty.py', 'verify-six-hundred-forty-one.py'),
]
for old, new in replacements:
    if old not in text:
        raise SystemExit(f'missing: {old}')
    text = text.replace(old, new)
dst.write_text(text)
print(dst)
