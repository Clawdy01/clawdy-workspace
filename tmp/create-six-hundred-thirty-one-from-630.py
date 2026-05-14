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
    'create-six-hundred-thirty-assets.py',
    'create-six-hundred-thirty-one-assets.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('[:615]', '[:616]'),
        ('!= 615', '!= 616'),
        ('kreeg 615', 'kreeg 616'),
        ('602, 603, 604, 605, 606', '603, 604, 605, 606, 607'),
    ],
)

build(
    'create-six-hundred-thirty-bootstrap.py',
    'create-six-hundred-thirty-one-bootstrap.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('all_cases[:615]', 'all_cases[:616]'),
        ('{UNKNOWN, TYPO}][:615]', '{UNKNOWN, TYPO}][:616]'),
        ('!= 615', '!= 616'),
        ('kreeg 615', 'kreeg 616'),
        ('598, 599, 600, 601, 602', '599, 600, 601, 602, 603'),
    ],
)

build(
    'create-six-hundred-thirty-minimal.py',
    'create-six-hundred-thirty-one-minimal.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('!= 615', '!= 616'),
        ('kreeg 615', 'kreeg 616'),
        ('598, 599, 600, 601, 602', '599, 600, 601, 602, 603'),
    ],
)

build(
    'make-six-hundred-thirty.py',
    'make-six-hundred-thirty-one.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('all_cases[:615]', 'all_cases[:616]'),
        ('{UNKNOWN, TYPO}][:615]', '{UNKNOWN, TYPO}][:616]'),
        ('!= 615', '!= 616'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'create-six-hundred-thirty-files.py',
    'create-six-hundred-thirty-one-files.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('all_cases[:615]', 'all_cases[:616]'),
        ('{UNKNOWN, TYPO}][:615]', '{UNKNOWN, TYPO}][:616]'),
        ('!= 615', '!= 616'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'create-six-hundred-thirty.py',
    'create-six-hundred-thirty-one.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('all_cases[:615]', 'all_cases[:616]'),
        ('{UNKNOWN, TYPO}][:615]', '{UNKNOWN, TYPO}][:616]'),
        ('!= 615', '!= 616'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'generate-validate-six-hundred-thirty.py',
    'generate-validate-six-hundred-thirty-one.py',
    [
        ('six-hundred-thirty', 'six-hundred-thirty-one'),
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('all_cases[:615]', 'all_cases[:616]'),
        ('{UNKNOWN, TYPO}][:615]', '{UNKNOWN, TYPO}][:616]'),
        ('!= 615', '!= 616'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'validate-six-hundred-thirty-valid-list-cases.py',
    'validate-six-hundred-thirty-one-valid-list-cases.py',
    [
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('600, 601, 602, 603, 604', '601, 602, 603, 604, 605'),
        ('all_cases[:615]', 'all_cases[:616]'),
        ('len(valid_cases) != 615', 'len(valid_cases) != 616'),
    ],
)

build(
    'validate-six-hundred-thirty-valid-mixed.py',
    'validate-six-hundred-thirty-one-valid-mixed.py',
    [
        ('zeshonderddertig', 'zeshonderdeenendertig'),
        ('600, 601, 602, 603, 604', '601, 602, 603, 604, 605'),
        ('][:615]', '][:616]'),
        ('len(valid_cases) != 615', 'len(valid_cases) != 616'),
        ('plain stderr noemt niet alle zeshonderdvijftien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzestien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty', 'six-hundred-thirty-one')
(ROOT / 'verify-six-hundred-thirty-one.py').write_text(verify_text)
print('verify-six-hundred-thirty-one.py')
