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
    'create-six-hundred-thirty-one-assets.py',
    'create-six-hundred-thirty-two-assets.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('[:616]', '[:617]'),
        ('!= 616', '!= 617'),
        ('kreeg 616', 'kreeg 617'),
        ('603, 604, 605, 606, 607', '604, 605, 606, 607, 608'),
    ],
)

build(
    'create-six-hundred-thirty-one-bootstrap.py',
    'create-six-hundred-thirty-two-bootstrap.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('all_cases[:616]', 'all_cases[:617]'),
        ('{UNKNOWN, TYPO}][:616]', '{UNKNOWN, TYPO}][:617]'),
        ('!= 616', '!= 617'),
        ('kreeg 616', 'kreeg 617'),
        ('599, 600, 601, 602, 603', '600, 601, 602, 603, 604'),
    ],
)

build(
    'create-six-hundred-thirty-one-minimal.py',
    'create-six-hundred-thirty-two-minimal.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('!= 616', '!= 617'),
        ('kreeg 616', 'kreeg 617'),
        ('599, 600, 601, 602, 603', '600, 601, 602, 603, 604'),
    ],
)

build(
    'make-six-hundred-thirty-one.py',
    'make-six-hundred-thirty-two.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('all_cases[:616]', 'all_cases[:617]'),
        ('{UNKNOWN, TYPO}][:616]', '{UNKNOWN, TYPO}][:617]'),
        ('!= 616', '!= 617'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'create-six-hundred-thirty-one-files.py',
    'create-six-hundred-thirty-two-files.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('all_cases[:616]', 'all_cases[:617]'),
        ('{UNKNOWN, TYPO}][:616]', '{UNKNOWN, TYPO}][:617]'),
        ('!= 616', '!= 617'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'create-six-hundred-thirty-one.py',
    'create-six-hundred-thirty-two.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('all_cases[:616]', 'all_cases[:617]'),
        ('{UNKNOWN, TYPO}][:616]', '{UNKNOWN, TYPO}][:617]'),
        ('!= 616', '!= 617'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-one.py',
    'generate-validate-six-hundred-thirty-two.py',
    [
        ('six-hundred-thirty-one', 'six-hundred-thirty-two'),
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('all_cases[:616]', 'all_cases[:617]'),
        ('{UNKNOWN, TYPO}][:616]', '{UNKNOWN, TYPO}][:617]'),
        ('!= 616', '!= 617'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'validate-six-hundred-thirty-one-valid-list-cases.py',
    'validate-six-hundred-thirty-two-valid-list-cases.py',
    [
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('601, 602, 603, 604, 605', '602, 603, 604, 605, 606'),
        ('all_cases[:616]', 'all_cases[:617]'),
        ('len(valid_cases) != 616', 'len(valid_cases) != 617'),
    ],
)

build(
    'validate-six-hundred-thirty-one-valid-mixed.py',
    'validate-six-hundred-thirty-two-valid-mixed.py',
    [
        ('zeshonderdeenendertig', 'zeshonderdtweeëndertig'),
        ('601, 602, 603, 604, 605', '602, 603, 604, 605, 606'),
        ('][:616]', '][:617]'),
        ('len(valid_cases) != 616', 'len(valid_cases) != 617'),
        ('plain stderr noemt niet alle zeshonderdzestien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzeventien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-one.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-one', 'six-hundred-thirty-two')
(ROOT / 'verify-six-hundred-thirty-two.py').write_text(verify_text)
print('verify-six-hundred-thirty-two.py')
