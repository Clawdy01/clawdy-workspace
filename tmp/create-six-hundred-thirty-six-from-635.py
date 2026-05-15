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
    'create-six-hundred-thirty-five-assets.py',
    'create-six-hundred-thirty-six-assets.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('[:620]', '[:621]'),
        ('!= 620', '!= 621'),
        ('kreeg 620', 'kreeg 621'),
        ('607, 608, 609, 610, 611', '608, 609, 610, 611, 612'),
    ],
)

build(
    'create-six-hundred-thirty-five-bootstrap.py',
    'create-six-hundred-thirty-six-bootstrap.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('all_cases[:620]', 'all_cases[:621]'),
        ('{UNKNOWN, TYPO}][:620]', '{UNKNOWN, TYPO}][:621]'),
        ('!= 620', '!= 621'),
        ('kreeg 620', 'kreeg 621'),
        ('603, 604, 605, 606, 607', '604, 605, 606, 607, 608'),
    ],
)

build(
    'create-six-hundred-thirty-five-minimal.py',
    'create-six-hundred-thirty-six-minimal.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('!= 620', '!= 621'),
        ('kreeg 620', 'kreeg 621'),
        ('603, 604, 605, 606, 607', '604, 605, 606, 607, 608'),
    ],
)

build(
    'make-six-hundred-thirty-five.py',
    'make-six-hundred-thirty-six.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('all_cases[:620]', 'all_cases[:621]'),
        ('{UNKNOWN, TYPO}][:620]', '{UNKNOWN, TYPO}][:621]'),
        ('!= 620', '!= 621'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'create-six-hundred-thirty-five-files.py',
    'create-six-hundred-thirty-six-files.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('all_cases[:620]', 'all_cases[:621]'),
        ('{UNKNOWN, TYPO}][:620]', '{UNKNOWN, TYPO}][:621]'),
        ('!= 620', '!= 621'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'create-six-hundred-thirty-five.py',
    'create-six-hundred-thirty-six.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('all_cases[:620]', 'all_cases[:621]'),
        ('{UNKNOWN, TYPO}][:620]', '{UNKNOWN, TYPO}][:621]'),
        ('!= 620', '!= 621'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-five.py',
    'generate-validate-six-hundred-thirty-six.py',
    [
        ('six-hundred-thirty-five', 'six-hundred-thirty-six'),
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('all_cases[:620]', 'all_cases[:621]'),
        ('{UNKNOWN, TYPO}][:620]', '{UNKNOWN, TYPO}][:621]'),
        ('!= 620', '!= 621'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'validate-six-hundred-thirty-five-valid-list-cases.py',
    'validate-six-hundred-thirty-six-valid-list-cases.py',
    [
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('605, 606, 607, 608, 609', '606, 607, 608, 609, 610'),
        ('all_cases[:620]', 'all_cases[:621]'),
        ('len(valid_cases) != 620', 'len(valid_cases) != 621'),
    ],
)

build(
    'validate-six-hundred-thirty-five-valid-mixed.py',
    'validate-six-hundred-thirty-six-valid-mixed.py',
    [
        ('zeshonderdvijfendertig', 'zeshonderdzesendertig'),
        ('605, 606, 607, 608, 609', '606, 607, 608, 609, 610'),
        ('][:620]', '][:621]'),
        ('len(valid_cases) != 620', 'len(valid_cases) != 621'),
        ('plain stderr noemt niet alle zeshonderdtwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdeenentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-five.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-five', 'six-hundred-thirty-six')
(ROOT / 'verify-six-hundred-thirty-six.py').write_text(verify_text)
print('verify-six-hundred-thirty-six.py')
