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
    'create-six-hundred-seven-assets.py',
    'create-six-hundred-eight-assets.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('[:592]', '[:593]'),
        ('!= 592', '!= 593'),
        ('kreeg 592', 'kreeg 593'),
        ('579, 580, 581, 582, 583', '580, 581, 582, 583, 584'),
    ],
)

build(
    'create-six-hundred-seven-bootstrap.py',
    'create-six-hundred-eight-bootstrap.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('all_cases[:592]', 'all_cases[:593]'),
        ('{UNKNOWN, TYPO}][:592]', '{UNKNOWN, TYPO}][:593]'),
        ('!= 592', '!= 593'),
        ('kreeg 592', 'kreeg 593'),
        ('575, 576, 577, 578, 579', '576, 577, 578, 579, 580'),
    ],
)

build(
    'create-six-hundred-seven-minimal.py',
    'create-six-hundred-eight-minimal.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('!= 592', '!= 593'),
        ('kreeg 592', 'kreeg 593'),
        ('575, 576, 577, 578, 579', '576, 577, 578, 579, 580'),
    ],
)

build(
    'make-six-hundred-seven.py',
    'make-six-hundred-eight.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('all_cases[:592]', 'all_cases[:593]'),
        ('{UNKNOWN, TYPO}][:592]', '{UNKNOWN, TYPO}][:593]'),
        ('!= 592', '!= 593'),
        ('515, 516, 517, 518, 519', '516, 517, 518, 519, 520'),
    ],
)

build(
    'create-six-hundred-seven-files.py',
    'create-six-hundred-eight-files.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('all_cases[:592]', 'all_cases[:593]'),
        ('{UNKNOWN, TYPO}][:592]', '{UNKNOWN, TYPO}][:593]'),
        ('!= 592', '!= 593'),
        ('515, 516, 517, 518, 519', '516, 517, 518, 519, 520'),
    ],
)

build(
    'create-six-hundred-seven.py',
    'create-six-hundred-eight.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('all_cases[:592]', 'all_cases[:593]'),
        ('{UNKNOWN, TYPO}][:592]', '{UNKNOWN, TYPO}][:593]'),
        ('!= 592', '!= 593'),
        ('518, 519, 520, 521, 522', '519, 520, 521, 522, 523'),
    ],
)

build(
    'generate-validate-six-hundred-seven.py',
    'generate-validate-six-hundred-eight.py',
    [
        ('six-hundred-seven', 'six-hundred-eight'),
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('all_cases[:592]', 'all_cases[:593]'),
        ('{UNKNOWN, TYPO}][:592]', '{UNKNOWN, TYPO}][:593]'),
        ('!= 592', '!= 593'),
        ('515, 516, 517, 518, 519', '516, 517, 518, 519, 520'),
    ],
)

build(
    'validate-six-hundred-seven-valid-list-cases.py',
    'validate-six-hundred-eight-valid-list-cases.py',
    [
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('577, 578, 579, 580, 581', '578, 579, 580, 581, 582'),
        ('all_cases[:592]', 'all_cases[:593]'),
        ('len(valid_cases) != 592', 'len(valid_cases) != 593'),
    ],
)

build(
    'validate-six-hundred-seven-valid-mixed.py',
    'validate-six-hundred-eight-valid-mixed.py',
    [
        ('zeshonderdzeven', 'zeshonderdacht'),
        ('577, 578, 579, 580, 581', '578, 579, 580, 581, 582'),
        ('][:592]', '][:593]'),
        ('len(valid_cases) != 592', 'len(valid_cases) != 593'),
        ('plain stderr noemt niet alle vijfhonderdtweeënnegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderddrieënnegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-seven.py').read_text()
verify_text = verify_src.replace('six-hundred-seven', 'six-hundred-eight')
(ROOT / 'verify-six-hundred-eight.py').write_text(verify_text)
print('verify-six-hundred-eight.py')
