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
    'create-six-hundred-thirty-six-assets.py',
    'create-six-hundred-thirty-seven-assets.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('[:621]', '[:622]'),
        ('!= 621', '!= 622'),
        ('kreeg 621', 'kreeg 622'),
        ('608, 609, 610, 611, 612', '609, 610, 611, 612, 613'),
    ],
)

build(
    'create-six-hundred-thirty-six-bootstrap.py',
    'create-six-hundred-thirty-seven-bootstrap.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('all_cases[:621]', 'all_cases[:622]'),
        ('{UNKNOWN, TYPO}][:621]', '{UNKNOWN, TYPO}][:622]'),
        ('!= 621', '!= 622'),
        ('kreeg 621', 'kreeg 622'),
        ('604, 605, 606, 607, 608', '605, 606, 607, 608, 609'),
    ],
)

build(
    'create-six-hundred-thirty-six-minimal.py',
    'create-six-hundred-thirty-seven-minimal.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('!= 621', '!= 622'),
        ('kreeg 621', 'kreeg 622'),
        ('604, 605, 606, 607, 608', '605, 606, 607, 608, 609'),
    ],
)

build(
    'make-six-hundred-thirty-six.py',
    'make-six-hundred-thirty-seven.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('all_cases[:621]', 'all_cases[:622]'),
        ('{UNKNOWN, TYPO}][:621]', '{UNKNOWN, TYPO}][:622]'),
        ('!= 621', '!= 622'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'create-six-hundred-thirty-six-files.py',
    'create-six-hundred-thirty-seven-files.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('all_cases[:621]', 'all_cases[:622]'),
        ('{UNKNOWN, TYPO}][:621]', '{UNKNOWN, TYPO}][:622]'),
        ('!= 621', '!= 622'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'create-six-hundred-thirty-six.py',
    'create-six-hundred-thirty-seven.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('all_cases[:621]', 'all_cases[:622]'),
        ('{UNKNOWN, TYPO}][:621]', '{UNKNOWN, TYPO}][:622]'),
        ('!= 621', '!= 622'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-six.py',
    'generate-validate-six-hundred-thirty-seven.py',
    [
        ('six-hundred-thirty-six', 'six-hundred-thirty-seven'),
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('all_cases[:621]', 'all_cases[:622]'),
        ('{UNKNOWN, TYPO}][:621]', '{UNKNOWN, TYPO}][:622]'),
        ('!= 621', '!= 622'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'validate-six-hundred-thirty-six-valid-list-cases.py',
    'validate-six-hundred-thirty-seven-valid-list-cases.py',
    [
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('606, 607, 608, 609, 610', '607, 608, 609, 610, 611'),
        ('all_cases[:621]', 'all_cases[:622]'),
        ('len(valid_cases) != 621', 'len(valid_cases) != 622'),
    ],
)

build(
    'validate-six-hundred-thirty-six-valid-mixed.py',
    'validate-six-hundred-thirty-seven-valid-mixed.py',
    [
        ('zeshonderdzesendertig', 'zeshonderdzevenendertig'),
        ('606, 607, 608, 609, 610', '607, 608, 609, 610, 611'),
        ('][:621]', '][:622]'),
        ('len(valid_cases) != 621', 'len(valid_cases) != 622'),
        ('plain stderr noemt niet alle zeshonderdeenentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdtweeëntwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-six.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-six', 'six-hundred-thirty-seven')
(ROOT / 'verify-six-hundred-thirty-seven.py').write_text(verify_text)
print('verify-six-hundred-thirty-seven.py')
