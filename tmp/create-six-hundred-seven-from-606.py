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
    'create-six-hundred-six-assets.py',
    'create-six-hundred-seven-assets.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('[:591]', '[:592]'),
        ('!= 591', '!= 592'),
        ('kreeg 591', 'kreeg 592'),
        ('578, 579, 580, 581, 582', '579, 580, 581, 582, 583'),
    ],
)

build(
    'create-six-hundred-six-bootstrap.py',
    'create-six-hundred-seven-bootstrap.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('all_cases[:591]', 'all_cases[:592]'),
        ('{UNKNOWN, TYPO}][:591]', '{UNKNOWN, TYPO}][:592]'),
        ('!= 591', '!= 592'),
        ('kreeg 591', 'kreeg 592'),
        ('574, 575, 576, 577, 578', '575, 576, 577, 578, 579'),
    ],
)

build(
    'create-six-hundred-six-minimal.py',
    'create-six-hundred-seven-minimal.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('!= 591', '!= 592'),
        ('kreeg 591', 'kreeg 592'),
        ('574, 575, 576, 577, 578', '575, 576, 577, 578, 579'),
    ],
)

build(
    'make-six-hundred-six.py',
    'make-six-hundred-seven.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('all_cases[:591]', 'all_cases[:592]'),
        ('{UNKNOWN, TYPO}][:591]', '{UNKNOWN, TYPO}][:592]'),
        ('!= 591', '!= 592'),
        ('514, 515, 516, 517, 518', '515, 516, 517, 518, 519'),
    ],
)

build(
    'create-six-hundred-six-files.py',
    'create-six-hundred-seven-files.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('all_cases[:591]', 'all_cases[:592]'),
        ('{UNKNOWN, TYPO}][:591]', '{UNKNOWN, TYPO}][:592]'),
        ('!= 591', '!= 592'),
        ('514, 515, 516, 517, 518', '515, 516, 517, 518, 519'),
    ],
)

build(
    'create-six-hundred-six.py',
    'create-six-hundred-seven.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('all_cases[:591]', 'all_cases[:592]'),
        ('{UNKNOWN, TYPO}][:591]', '{UNKNOWN, TYPO}][:592]'),
        ('!= 591', '!= 592'),
        ('517, 518, 519, 520, 521', '518, 519, 520, 521, 522'),
    ],
)

build(
    'generate-validate-six-hundred-six.py',
    'generate-validate-six-hundred-seven.py',
    [
        ('six-hundred-six', 'six-hundred-seven'),
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('all_cases[:591]', 'all_cases[:592]'),
        ('{UNKNOWN, TYPO}][:591]', '{UNKNOWN, TYPO}][:592]'),
        ('!= 591', '!= 592'),
        ('514, 515, 516, 517, 518', '515, 516, 517, 518, 519'),
    ],
)

build(
    'validate-six-hundred-six-valid-list-cases.py',
    'validate-six-hundred-seven-valid-list-cases.py',
    [
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('576, 577, 578, 579, 580', '577, 578, 579, 580, 581'),
        ('all_cases[:591]', 'all_cases[:592]'),
        ('len(valid_cases) != 591', 'len(valid_cases) != 592'),
    ],
)

build(
    'validate-six-hundred-six-valid-mixed.py',
    'validate-six-hundred-seven-valid-mixed.py',
    [
        ('zeshonderdzes', 'zeshonderdzeven'),
        ('576, 577, 578, 579, 580', '577, 578, 579, 580, 581'),
        ('][:591]', '][:592]'),
        ('len(valid_cases) != 591', 'len(valid_cases) != 592'),
        ('plain stderr noemt niet alle vijfhonderdeenennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdtweeënnegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-six.py').read_text()
verify_text = verify_src.replace('six-hundred-six', 'six-hundred-seven')
(ROOT / 'verify-six-hundred-seven.py').write_text(verify_text)
print('verify-six-hundred-seven.py')
