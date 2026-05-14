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
    'create-six-hundred-twenty-one-assets.py',
    'create-six-hundred-twenty-two-assets.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('[:606]', '[:607]'),
        ('!= 606', '!= 607'),
        ('kreeg 606', 'kreeg 607'),
        ('593, 594, 595, 596, 597', '594, 595, 596, 597, 598'),
    ],
)

build(
    'create-six-hundred-twenty-one-bootstrap.py',
    'create-six-hundred-twenty-two-bootstrap.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('all_cases[:606]', 'all_cases[:607]'),
        ('{UNKNOWN, TYPO}][:606]', '{UNKNOWN, TYPO}][:607]'),
        ('!= 606', '!= 607'),
        ('kreeg 606', 'kreeg 607'),
        ('589, 590, 591, 592, 593', '590, 591, 592, 593, 594'),
    ],
)

build(
    'create-six-hundred-twenty-one-minimal.py',
    'create-six-hundred-twenty-two-minimal.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('!= 606', '!= 607'),
        ('kreeg 606', 'kreeg 607'),
        ('589, 590, 591, 592, 593', '590, 591, 592, 593, 594'),
    ],
)

build(
    'make-six-hundred-twenty-one.py',
    'make-six-hundred-twenty-two.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('all_cases[:606]', 'all_cases[:607]'),
        ('{UNKNOWN, TYPO}][:606]', '{UNKNOWN, TYPO}][:607]'),
        ('!= 606', '!= 607'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
    ],
)

build(
    'create-six-hundred-twenty-one-files.py',
    'create-six-hundred-twenty-two-files.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('all_cases[:606]', 'all_cases[:607]'),
        ('{UNKNOWN, TYPO}][:606]', '{UNKNOWN, TYPO}][:607]'),
        ('!= 606', '!= 607'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
    ],
)

build(
    'create-six-hundred-twenty-one.py',
    'create-six-hundred-twenty-two.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('all_cases[:606]', 'all_cases[:607]'),
        ('{UNKNOWN, TYPO}][:606]', '{UNKNOWN, TYPO}][:607]'),
        ('!= 606', '!= 607'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-one.py',
    'generate-validate-six-hundred-twenty-two.py',
    [
        ('six-hundred-twenty-one', 'six-hundred-twenty-two'),
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('all_cases[:606]', 'all_cases[:607]'),
        ('{UNKNOWN, TYPO}][:606]', '{UNKNOWN, TYPO}][:607]'),
        ('!= 606', '!= 607'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
    ],
)

build(
    'validate-six-hundred-twenty-one-valid-list-cases.py',
    'validate-six-hundred-twenty-two-valid-list-cases.py',
    [
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('591, 592, 593, 594, 595', '592, 593, 594, 595, 596'),
        ('all_cases[:606]', 'all_cases[:607]'),
        ('len(valid_cases) != 606', 'len(valid_cases) != 607'),
    ],
)

build(
    'validate-six-hundred-twenty-one-valid-mixed.py',
    'validate-six-hundred-twenty-two-valid-mixed.py',
    [
        ('zeshonderdeenentwintig', 'zeshonderdtweeëntwintig'),
        ('591, 592, 593, 594, 595', '592, 593, 594, 595, 596'),
        ('][:606]', '][:607]'),
        ('len(valid_cases) != 606', 'len(valid_cases) != 607'),
        ('plain stderr noemt niet alle zeshonderdzes geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzeven geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-one.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-one', 'six-hundred-twenty-two')
(ROOT / 'verify-six-hundred-twenty-two.py').write_text(verify_text)
print('verify-six-hundred-twenty-two.py')
