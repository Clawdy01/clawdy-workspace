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
    'create-six-hundred-nineteen-assets.py',
    'create-six-hundred-twenty-assets.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('[:604]', '[:605]'),
        ('!= 604', '!= 605'),
        ('kreeg 604', 'kreeg 605'),
        ('591, 592, 593, 594, 595', '592, 593, 594, 595, 596'),
    ],
)

build(
    'create-six-hundred-nineteen-bootstrap.py',
    'create-six-hundred-twenty-bootstrap.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('all_cases[:604]', 'all_cases[:605]'),
        ('{UNKNOWN, TYPO}][:604]', '{UNKNOWN, TYPO}][:605]'),
        ('!= 604', '!= 605'),
        ('kreeg 604', 'kreeg 605'),
        ('587, 588, 589, 590, 591', '588, 589, 590, 591, 592'),
    ],
)

build(
    'create-six-hundred-nineteen-minimal.py',
    'create-six-hundred-twenty-minimal.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('!= 604', '!= 605'),
        ('kreeg 604', 'kreeg 605'),
        ('587, 588, 589, 590, 591', '588, 589, 590, 591, 592'),
    ],
)

build(
    'make-six-hundred-nineteen.py',
    'make-six-hundred-twenty.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('all_cases[:604]', 'all_cases[:605]'),
        ('{UNKNOWN, TYPO}][:604]', '{UNKNOWN, TYPO}][:605]'),
        ('!= 604', '!= 605'),
        ('527, 528, 529, 530, 531', '528, 529, 530, 531, 532'),
    ],
)

build(
    'create-six-hundred-nineteen-files.py',
    'create-six-hundred-twenty-files.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('all_cases[:604]', 'all_cases[:605]'),
        ('{UNKNOWN, TYPO}][:604]', '{UNKNOWN, TYPO}][:605]'),
        ('!= 604', '!= 605'),
        ('527, 528, 529, 530, 531', '528, 529, 530, 531, 532'),
    ],
)

build(
    'create-six-hundred-nineteen.py',
    'create-six-hundred-twenty.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('all_cases[:604]', 'all_cases[:605]'),
        ('{UNKNOWN, TYPO}][:604]', '{UNKNOWN, TYPO}][:605]'),
        ('!= 604', '!= 605'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
    ],
)

build(
    'generate-validate-six-hundred-nineteen.py',
    'generate-validate-six-hundred-twenty.py',
    [
        ('six-hundred-nineteen', 'six-hundred-twenty'),
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('all_cases[:604]', 'all_cases[:605]'),
        ('{UNKNOWN, TYPO}][:604]', '{UNKNOWN, TYPO}][:605]'),
        ('!= 604', '!= 605'),
        ('527, 528, 529, 530, 531', '528, 529, 530, 531, 532'),
    ],
)

build(
    'validate-six-hundred-nineteen-valid-list-cases.py',
    'validate-six-hundred-twenty-valid-list-cases.py',
    [
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('589, 590, 591, 592, 593', '590, 591, 592, 593, 594'),
        ('all_cases[:604]', 'all_cases[:605]'),
        ('len(valid_cases) != 604', 'len(valid_cases) != 605'),
    ],
)

build(
    'validate-six-hundred-nineteen-valid-mixed.py',
    'validate-six-hundred-twenty-valid-mixed.py',
    [
        ('zeshonderdnegentien', 'zeshonderdtwintig'),
        ('589, 590, 591, 592, 593', '590, 591, 592, 593, 594'),
        ('][:604]', '][:605]'),
        ('len(valid_cases) != 604', 'len(valid_cases) != 605'),
        ('plain stderr noemt niet alle zeshonderdvier geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvijf geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-nineteen.py').read_text()
verify_text = verify_src.replace('six-hundred-nineteen', 'six-hundred-twenty')
(ROOT / 'verify-six-hundred-twenty.py').write_text(verify_text)
print('verify-six-hundred-twenty.py')
