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
    'create-six-hundred-thirty-two-assets.py',
    'create-six-hundred-thirty-three-assets.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('[:617]', '[:618]'),
        ('!= 617', '!= 618'),
        ('kreeg 617', 'kreeg 618'),
        ('604, 605, 606, 607, 608', '605, 606, 607, 608, 609'),
    ],
)

build(
    'create-six-hundred-thirty-two-bootstrap.py',
    'create-six-hundred-thirty-three-bootstrap.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('all_cases[:617]', 'all_cases[:618]'),
        ('{UNKNOWN, TYPO}][:617]', '{UNKNOWN, TYPO}][:618]'),
        ('!= 617', '!= 618'),
        ('kreeg 617', 'kreeg 618'),
        ('600, 601, 602, 603, 604', '601, 602, 603, 604, 605'),
    ],
)

build(
    'create-six-hundred-thirty-two-minimal.py',
    'create-six-hundred-thirty-three-minimal.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('!= 617', '!= 618'),
        ('kreeg 617', 'kreeg 618'),
        ('600, 601, 602, 603, 604', '601, 602, 603, 604, 605'),
    ],
)

build(
    'make-six-hundred-thirty-two.py',
    'make-six-hundred-thirty-three.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('all_cases[:617]', 'all_cases[:618]'),
        ('{UNKNOWN, TYPO}][:617]', '{UNKNOWN, TYPO}][:618]'),
        ('!= 617', '!= 618'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'create-six-hundred-thirty-two-files.py',
    'create-six-hundred-thirty-three-files.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('all_cases[:617]', 'all_cases[:618]'),
        ('{UNKNOWN, TYPO}][:617]', '{UNKNOWN, TYPO}][:618]'),
        ('!= 617', '!= 618'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'create-six-hundred-thirty-two.py',
    'create-six-hundred-thirty-three.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('all_cases[:617]', 'all_cases[:618]'),
        ('{UNKNOWN, TYPO}][:617]', '{UNKNOWN, TYPO}][:618]'),
        ('!= 617', '!= 618'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-two.py',
    'generate-validate-six-hundred-thirty-three.py',
    [
        ('six-hundred-thirty-two', 'six-hundred-thirty-three'),
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('all_cases[:617]', 'all_cases[:618]'),
        ('{UNKNOWN, TYPO}][:617]', '{UNKNOWN, TYPO}][:618]'),
        ('!= 617', '!= 618'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'validate-six-hundred-thirty-two-valid-list-cases.py',
    'validate-six-hundred-thirty-three-valid-list-cases.py',
    [
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('602, 603, 604, 605, 606', '603, 604, 605, 606, 607'),
        ('all_cases[:617]', 'all_cases[:618]'),
        ('len(valid_cases) != 617', 'len(valid_cases) != 618'),
    ],
)

build(
    'validate-six-hundred-thirty-two-valid-mixed.py',
    'validate-six-hundred-thirty-three-valid-mixed.py',
    [
        ('zeshonderdtweeëndertig', 'zeshonderddrieëndertig'),
        ('602, 603, 604, 605, 606', '603, 604, 605, 606, 607'),
        ('][:617]', '][:618]'),
        ('len(valid_cases) != 617', 'len(valid_cases) != 618'),
        ('plain stderr noemt niet alle zeshonderdzeventien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdachttien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-two.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-two', 'six-hundred-thirty-three')
(ROOT / 'verify-six-hundred-thirty-three.py').write_text(verify_text)
print('verify-six-hundred-thirty-three.py')
