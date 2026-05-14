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
    'create-six-hundred-thirty-four-assets.py',
    'create-six-hundred-thirty-five-assets.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('[:619]', '[:620]'),
        ('!= 619', '!= 620'),
        ('kreeg 619', 'kreeg 620'),
        ('606, 607, 608, 609, 610', '607, 608, 609, 610, 611'),
    ],
)

build(
    'create-six-hundred-thirty-four-bootstrap.py',
    'create-six-hundred-thirty-five-bootstrap.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('all_cases[:619]', 'all_cases[:620]'),
        ('{UNKNOWN, TYPO}][:619]', '{UNKNOWN, TYPO}][:620]'),
        ('!= 619', '!= 620'),
        ('kreeg 619', 'kreeg 620'),
        ('602, 603, 604, 605, 606', '603, 604, 605, 606, 607'),
    ],
)

build(
    'create-six-hundred-thirty-four-minimal.py',
    'create-six-hundred-thirty-five-minimal.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('!= 619', '!= 620'),
        ('kreeg 619', 'kreeg 620'),
        ('602, 603, 604, 605, 606', '603, 604, 605, 606, 607'),
    ],
)

build(
    'make-six-hundred-thirty-four.py',
    'make-six-hundred-thirty-five.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('all_cases[:619]', 'all_cases[:620]'),
        ('{UNKNOWN, TYPO}][:619]', '{UNKNOWN, TYPO}][:620]'),
        ('!= 619', '!= 620'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'create-six-hundred-thirty-four-files.py',
    'create-six-hundred-thirty-five-files.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('all_cases[:619]', 'all_cases[:620]'),
        ('{UNKNOWN, TYPO}][:619]', '{UNKNOWN, TYPO}][:620]'),
        ('!= 619', '!= 620'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'create-six-hundred-thirty-four.py',
    'create-six-hundred-thirty-five.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('all_cases[:619]', 'all_cases[:620]'),
        ('{UNKNOWN, TYPO}][:619]', '{UNKNOWN, TYPO}][:620]'),
        ('!= 619', '!= 620'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-four.py',
    'generate-validate-six-hundred-thirty-five.py',
    [
        ('six-hundred-thirty-four', 'six-hundred-thirty-five'),
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('all_cases[:619]', 'all_cases[:620]'),
        ('{UNKNOWN, TYPO}][:619]', '{UNKNOWN, TYPO}][:620]'),
        ('!= 619', '!= 620'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'validate-six-hundred-thirty-four-valid-list-cases.py',
    'validate-six-hundred-thirty-five-valid-list-cases.py',
    [
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('604, 605, 606, 607, 608', '605, 606, 607, 608, 609'),
        ('all_cases[:619]', 'all_cases[:620]'),
        ('len(valid_cases) != 619', 'len(valid_cases) != 620'),
    ],
)

build(
    'validate-six-hundred-thirty-four-valid-mixed.py',
    'validate-six-hundred-thirty-five-valid-mixed.py',
    [
        ('zeshonderdvierendertig', 'zeshonderdvijfendertig'),
        ('604, 605, 606, 607, 608', '605, 606, 607, 608, 609'),
        ('][:619]', '][:620]'),
        ('len(valid_cases) != 619', 'len(valid_cases) != 620'),
        ('plain stderr noemt niet alle zeshonderdnegentien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdtwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-four.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-four', 'six-hundred-thirty-five')
(ROOT / 'verify-six-hundred-thirty-five.py').write_text(verify_text)
print('verify-six-hundred-thirty-five.py')
