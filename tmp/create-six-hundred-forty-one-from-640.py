#!/usr/bin/env python3
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace/tmp')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f'missing in {label}: {old}')
    return text.replace(old, new, 1)


def build(src: str, dst: str, replacements: list[tuple[str, str]]) -> None:
    text = (ROOT / src).read_text()
    for old, new in replacements:
        text = replace_once(text, old, new, src)
    (ROOT / dst).write_text(text)
    print(dst)


build(
    'create-six-hundred-forty-assets.py',
    'create-six-hundred-forty-one-assets.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('[:625]', '[:626]'),
        ('!= 625', '!= 626'),
        ('kreeg 625', 'kreeg 626'),
        ('612, 613, 614, 615, 616', '613, 614, 615, 616, 617'),
    ],
)

build(
    'create-six-hundred-forty-bootstrap.py',
    'create-six-hundred-forty-one-bootstrap.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('all_cases[:625]', 'all_cases[:626]'),
        ('{UNKNOWN, TYPO}][:625]', '{UNKNOWN, TYPO}][:626]'),
        ('!= 625', '!= 626'),
        ('kreeg 625', 'kreeg 626'),
        ('608, 609, 610, 611, 612', '609, 610, 611, 612, 613'),
    ],
)

build(
    'create-six-hundred-forty-minimal.py',
    'create-six-hundred-forty-one-minimal.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('!= 625', '!= 626'),
        ('kreeg 625', 'kreeg 626'),
        ('608, 609, 610, 611, 612', '609, 610, 611, 612, 613'),
    ],
)

build(
    'make-six-hundred-forty.py',
    'make-six-hundred-forty-one.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('all_cases[:625]', 'all_cases[:626]'),
        ('{UNKNOWN, TYPO}][:625]', '{UNKNOWN, TYPO}][:626]'),
        ('!= 625', '!= 626'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'create-six-hundred-forty-files.py',
    'create-six-hundred-forty-one-files.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('all_cases[:625]', 'all_cases[:626]'),
        ('{UNKNOWN, TYPO}][:625]', '{UNKNOWN, TYPO}][:626]'),
        ('!= 625', '!= 626'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'create-six-hundred-forty.py',
    'create-six-hundred-forty-one.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('all_cases[:625]', 'all_cases[:626]'),
        ('{UNKNOWN, TYPO}][:625]', '{UNKNOWN, TYPO}][:626]'),
        ('!= 625', '!= 626'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'generate-validate-six-hundred-forty.py',
    'generate-validate-six-hundred-forty-one.py',
    [
        ('six-hundred-forty', 'six-hundred-forty-one'),
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('all_cases[:625]', 'all_cases[:626]'),
        ('{UNKNOWN, TYPO}][:625]', '{UNKNOWN, TYPO}][:626]'),
        ('!= 625', '!= 626'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'validate-six-hundred-forty-valid-list-cases.py',
    'validate-six-hundred-forty-one-valid-list-cases.py',
    [
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('610, 611, 612, 613, 614', '611, 612, 613, 614, 615'),
        ('all_cases[:625]', 'all_cases[:626]'),
        ('len(valid_cases) != 625', 'len(valid_cases) != 626'),
    ],
)

build(
    'validate-six-hundred-forty-valid-mixed.py',
    'validate-six-hundred-forty-one-valid-mixed.py',
    [
        ('zeshonderdveertig', 'zeshonderdeenenveertig'),
        ('610, 611, 612, 613, 614', '611, 612, 613, 614, 615'),
        ('][:625]', '][:626]'),
        ('len(valid_cases) != 625', 'len(valid_cases) != 626'),
        ('plain stderr noemt niet alle zeshonderdvijfentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzesentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty.py').read_text()
verify_text = verify_src.replace('six-hundred-forty', 'six-hundred-forty-one')
(ROOT / 'verify-six-hundred-forty-one.py').write_text(verify_text)
print('verify-six-hundred-forty-one.py')
