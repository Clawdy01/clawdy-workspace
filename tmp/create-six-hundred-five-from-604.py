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
    'create-six-hundred-four-assets.py',
    'create-six-hundred-five-assets.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('[:589]', '[:590]'),
        ('!= 589', '!= 590'),
        ('kreeg 589', 'kreeg 590'),
        ('576, 577, 578, 579, 580', '577, 578, 579, 580, 581'),
    ],
)

build(
    'create-six-hundred-four-bootstrap.py',
    'create-six-hundred-five-bootstrap.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('all_cases[:589]', 'all_cases[:590]'),
        ('{UNKNOWN, TYPO}][:589]', '{UNKNOWN, TYPO}][:590]'),
        ('!= 589', '!= 590'),
        ('kreeg 589', 'kreeg 590'),
        ('572, 573, 574, 575, 576', '573, 574, 575, 576, 577'),
    ],
)

build(
    'create-six-hundred-four-minimal.py',
    'create-six-hundred-five-minimal.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('!= 589', '!= 590'),
        ('kreeg 589', 'kreeg 590'),
        ('572, 573, 574, 575, 576', '573, 574, 575, 576, 577'),
    ],
)

build(
    'make-six-hundred-four.py',
    'make-six-hundred-five.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('all_cases[:589]', 'all_cases[:590]'),
        ('{UNKNOWN, TYPO}][:589]', '{UNKNOWN, TYPO}][:590]'),
        ('!= 589', '!= 590'),
        ('512, 513, 514, 515, 516', '513, 514, 515, 516, 517'),
    ],
)

build(
    'create-six-hundred-four-files.py',
    'create-six-hundred-five-files.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('all_cases[:589]', 'all_cases[:590]'),
        ('{UNKNOWN, TYPO}][:589]', '{UNKNOWN, TYPO}][:590]'),
        ('!= 589', '!= 590'),
        ('512, 513, 514, 515, 516', '513, 514, 515, 516, 517'),
    ],
)

build(
    'create-six-hundred-four.py',
    'create-six-hundred-five.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('all_cases[:589]', 'all_cases[:590]'),
        ('{UNKNOWN, TYPO}][:589]', '{UNKNOWN, TYPO}][:590]'),
        ('!= 589', '!= 590'),
        ('515, 516, 517, 518, 519', '516, 517, 518, 519, 520'),
    ],
)

build(
    'generate-validate-six-hundred-four.py',
    'generate-validate-six-hundred-five.py',
    [
        ('six-hundred-four', 'six-hundred-five'),
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('all_cases[:589]', 'all_cases[:590]'),
        ('{UNKNOWN, TYPO}][:589]', '{UNKNOWN, TYPO}][:590]'),
        ('!= 589', '!= 590'),
        ('512, 513, 514, 515, 516', '513, 514, 515, 516, 517'),
    ],
)

build(
    'validate-six-hundred-four-valid-list-cases.py',
    'validate-six-hundred-five-valid-list-cases.py',
    [
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('574, 575, 576, 577, 578', '575, 576, 577, 578, 579'),
        ('all_cases[:589]', 'all_cases[:590]'),
        ('len(valid_cases) != 589', 'len(valid_cases) != 590'),
    ],
)

build(
    'validate-six-hundred-four-valid-mixed.py',
    'validate-six-hundred-five-valid-mixed.py',
    [
        ('zeshonderdvier', 'zeshonderdvijf'),
        ('574, 575, 576, 577, 578', '575, 576, 577, 578, 579'),
        ('][:589]', '][:590]'),
        ('len(valid_cases) != 589', 'len(valid_cases) != 590'),
        ('plain stderr noemt niet alle vijfhonderdnegenentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdnegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-four.py').read_text()
verify_text = verify_src.replace('six-hundred-four', 'six-hundred-five')
(ROOT / 'verify-six-hundred-five.py').write_text(verify_text)
print('verify-six-hundred-five.py')
