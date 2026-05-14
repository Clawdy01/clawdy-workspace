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
    'create-six-hundred-thirty-three-assets.py',
    'create-six-hundred-thirty-four-assets.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('[:618]', '[:619]'),
        ('!= 618', '!= 619'),
        ('kreeg 618', 'kreeg 619'),
        ('605, 606, 607, 608, 609', '606, 607, 608, 609, 610'),
    ],
)

build(
    'create-six-hundred-thirty-three-bootstrap.py',
    'create-six-hundred-thirty-four-bootstrap.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('all_cases[:618]', 'all_cases[:619]'),
        ('{UNKNOWN, TYPO}][:618]', '{UNKNOWN, TYPO}][:619]'),
        ('!= 618', '!= 619'),
        ('kreeg 618', 'kreeg 619'),
        ('601, 602, 603, 604, 605', '602, 603, 604, 605, 606'),
    ],
)

build(
    'create-six-hundred-thirty-three-minimal.py',
    'create-six-hundred-thirty-four-minimal.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('!= 618', '!= 619'),
        ('kreeg 618', 'kreeg 619'),
        ('601, 602, 603, 604, 605', '602, 603, 604, 605, 606'),
    ],
)

build(
    'make-six-hundred-thirty-three.py',
    'make-six-hundred-thirty-four.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('all_cases[:618]', 'all_cases[:619]'),
        ('{UNKNOWN, TYPO}][:618]', '{UNKNOWN, TYPO}][:619]'),
        ('!= 618', '!= 619'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'create-six-hundred-thirty-three-files.py',
    'create-six-hundred-thirty-four-files.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('all_cases[:618]', 'all_cases[:619]'),
        ('{UNKNOWN, TYPO}][:618]', '{UNKNOWN, TYPO}][:619]'),
        ('!= 618', '!= 619'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'create-six-hundred-thirty-three.py',
    'create-six-hundred-thirty-four.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('all_cases[:618]', 'all_cases[:619]'),
        ('{UNKNOWN, TYPO}][:618]', '{UNKNOWN, TYPO}][:619]'),
        ('!= 618', '!= 619'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-three.py',
    'generate-validate-six-hundred-thirty-four.py',
    [
        ('six-hundred-thirty-three', 'six-hundred-thirty-four'),
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('all_cases[:618]', 'all_cases[:619]'),
        ('{UNKNOWN, TYPO}][:618]', '{UNKNOWN, TYPO}][:619]'),
        ('!= 618', '!= 619'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'validate-six-hundred-thirty-three-valid-list-cases.py',
    'validate-six-hundred-thirty-four-valid-list-cases.py',
    [
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('603, 604, 605, 606, 607', '604, 605, 606, 607, 608'),
        ('all_cases[:618]', 'all_cases[:619]'),
        ('len(valid_cases) != 618', 'len(valid_cases) != 619'),
    ],
)

build(
    'validate-six-hundred-thirty-three-valid-mixed.py',
    'validate-six-hundred-thirty-four-valid-mixed.py',
    [
        ('zeshonderddrieëndertig', 'zeshonderdvierendertig'),
        ('603, 604, 605, 606, 607', '604, 605, 606, 607, 608'),
        ('][:618]', '][:619]'),
        ('len(valid_cases) != 618', 'len(valid_cases) != 619'),
        ('plain stderr noemt niet alle zeshonderdachttien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdnegentien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-three.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-three', 'six-hundred-thirty-four')
(ROOT / 'verify-six-hundred-thirty-four.py').write_text(verify_text)
print('verify-six-hundred-thirty-four.py')
