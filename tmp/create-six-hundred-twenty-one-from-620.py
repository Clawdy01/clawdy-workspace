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
    'create-six-hundred-twenty-assets.py',
    'create-six-hundred-twenty-one-assets.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('[:605]', '[:606]'),
        ('!= 605', '!= 606'),
        ('kreeg 605', 'kreeg 606'),
        ('592, 593, 594, 595, 596', '593, 594, 595, 596, 597'),
    ],
)

build(
    'create-six-hundred-twenty-bootstrap.py',
    'create-six-hundred-twenty-one-bootstrap.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('all_cases[:605]', 'all_cases[:606]'),
        ('{UNKNOWN, TYPO}][:605]', '{UNKNOWN, TYPO}][:606]'),
        ('!= 605', '!= 606'),
        ('kreeg 605', 'kreeg 606'),
        ('588, 589, 590, 591, 592', '589, 590, 591, 592, 593'),
    ],
)

build(
    'create-six-hundred-twenty-minimal.py',
    'create-six-hundred-twenty-one-minimal.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('!= 605', '!= 606'),
        ('kreeg 605', 'kreeg 606'),
        ('588, 589, 590, 591, 592', '589, 590, 591, 592, 593'),
    ],
)

build(
    'make-six-hundred-twenty.py',
    'make-six-hundred-twenty-one.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('all_cases[:605]', 'all_cases[:606]'),
        ('{UNKNOWN, TYPO}][:605]', '{UNKNOWN, TYPO}][:606]'),
        ('!= 605', '!= 606'),
        ('528, 529, 530, 531, 532', '529, 530, 531, 532, 533'),
    ],
)

build(
    'create-six-hundred-twenty-files.py',
    'create-six-hundred-twenty-one-files.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('all_cases[:605]', 'all_cases[:606]'),
        ('{UNKNOWN, TYPO}][:605]', '{UNKNOWN, TYPO}][:606]'),
        ('!= 605', '!= 606'),
        ('528, 529, 530, 531, 532', '529, 530, 531, 532, 533'),
    ],
)

build(
    'create-six-hundred-twenty.py',
    'create-six-hundred-twenty-one.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('all_cases[:605]', 'all_cases[:606]'),
        ('{UNKNOWN, TYPO}][:605]', '{UNKNOWN, TYPO}][:606]'),
        ('!= 605', '!= 606'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
    ],
)

build(
    'generate-validate-six-hundred-twenty.py',
    'generate-validate-six-hundred-twenty-one.py',
    [
        ('six-hundred-twenty', 'six-hundred-twenty-one'),
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('all_cases[:605]', 'all_cases[:606]'),
        ('{UNKNOWN, TYPO}][:605]', '{UNKNOWN, TYPO}][:606]'),
        ('!= 605', '!= 606'),
        ('528, 529, 530, 531, 532', '529, 530, 531, 532, 533'),
    ],
)

build(
    'validate-six-hundred-twenty-valid-list-cases.py',
    'validate-six-hundred-twenty-one-valid-list-cases.py',
    [
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('590, 591, 592, 593, 594', '591, 592, 593, 594, 595'),
        ('all_cases[:605]', 'all_cases[:606]'),
        ('len(valid_cases) != 605', 'len(valid_cases) != 606'),
    ],
)

build(
    'validate-six-hundred-twenty-valid-mixed.py',
    'validate-six-hundred-twenty-one-valid-mixed.py',
    [
        ('zeshonderdtwintig', 'zeshonderdeenentwintig'),
        ('590, 591, 592, 593, 594', '591, 592, 593, 594, 595'),
        ('][:605]', '][:606]'),
        ('len(valid_cases) != 605', 'len(valid_cases) != 606'),
        ('plain stderr noemt niet alle zeshonderdvijf geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzes geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty', 'six-hundred-twenty-one')
(ROOT / 'verify-six-hundred-twenty-one.py').write_text(verify_text)
print('verify-six-hundred-twenty-one.py')
