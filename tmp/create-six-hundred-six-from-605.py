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
    'create-six-hundred-five-assets.py',
    'create-six-hundred-six-assets.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('[:590]', '[:591]'),
        ('!= 590', '!= 591'),
        ('kreeg 590', 'kreeg 591'),
        ('577, 578, 579, 580, 581', '578, 579, 580, 581, 582'),
    ],
)

build(
    'create-six-hundred-five-bootstrap.py',
    'create-six-hundred-six-bootstrap.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('all_cases[:590]', 'all_cases[:591]'),
        ('{UNKNOWN, TYPO}][:590]', '{UNKNOWN, TYPO}][:591]'),
        ('!= 590', '!= 591'),
        ('kreeg 590', 'kreeg 591'),
        ('573, 574, 575, 576, 577', '574, 575, 576, 577, 578'),
    ],
)

build(
    'create-six-hundred-five-minimal.py',
    'create-six-hundred-six-minimal.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('!= 590', '!= 591'),
        ('kreeg 590', 'kreeg 591'),
        ('573, 574, 575, 576, 577', '574, 575, 576, 577, 578'),
    ],
)

build(
    'make-six-hundred-five.py',
    'make-six-hundred-six.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('all_cases[:590]', 'all_cases[:591]'),
        ('{UNKNOWN, TYPO}][:590]', '{UNKNOWN, TYPO}][:591]'),
        ('!= 590', '!= 591'),
        ('513, 514, 515, 516, 517', '514, 515, 516, 517, 518'),
    ],
)

build(
    'create-six-hundred-five-files.py',
    'create-six-hundred-six-files.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('all_cases[:590]', 'all_cases[:591]'),
        ('{UNKNOWN, TYPO}][:590]', '{UNKNOWN, TYPO}][:591]'),
        ('!= 590', '!= 591'),
        ('513, 514, 515, 516, 517', '514, 515, 516, 517, 518'),
    ],
)

build(
    'create-six-hundred-five.py',
    'create-six-hundred-six.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('all_cases[:590]', 'all_cases[:591]'),
        ('{UNKNOWN, TYPO}][:590]', '{UNKNOWN, TYPO}][:591]'),
        ('!= 590', '!= 591'),
        ('516, 517, 518, 519, 520', '517, 518, 519, 520, 521'),
    ],
)

build(
    'generate-validate-six-hundred-five.py',
    'generate-validate-six-hundred-six.py',
    [
        ('six-hundred-five', 'six-hundred-six'),
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('all_cases[:590]', 'all_cases[:591]'),
        ('{UNKNOWN, TYPO}][:590]', '{UNKNOWN, TYPO}][:591]'),
        ('!= 590', '!= 591'),
        ('513, 514, 515, 516, 517', '514, 515, 516, 517, 518'),
    ],
)

build(
    'validate-six-hundred-five-valid-list-cases.py',
    'validate-six-hundred-six-valid-list-cases.py',
    [
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('575, 576, 577, 578, 579', '576, 577, 578, 579, 580'),
        ('all_cases[:590]', 'all_cases[:591]'),
        ('len(valid_cases) != 590', 'len(valid_cases) != 591'),
    ],
)

build(
    'validate-six-hundred-five-valid-mixed.py',
    'validate-six-hundred-six-valid-mixed.py',
    [
        ('zeshonderdvijf', 'zeshonderdzes'),
        ('575, 576, 577, 578, 579', '576, 577, 578, 579, 580'),
        ('][:590]', '][:591]'),
        ('len(valid_cases) != 590', 'len(valid_cases) != 591'),
        ('plain stderr noemt niet alle vijfhonderdnegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdeenennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-five.py').read_text()
verify_text = verify_src.replace('six-hundred-five', 'six-hundred-six')
(ROOT / 'verify-six-hundred-six.py').write_text(verify_text)
print('verify-six-hundred-six.py')
