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
    'create-six-hundred-twenty-two-assets.py',
    'create-six-hundred-twenty-three-assets.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('[:607]', '[:608]'),
        ('!= 607', '!= 608'),
        ('kreeg 607', 'kreeg 608'),
        ('594, 595, 596, 597, 598', '595, 596, 597, 598, 599'),
    ],
)

build(
    'create-six-hundred-twenty-two-bootstrap.py',
    'create-six-hundred-twenty-three-bootstrap.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('all_cases[:607]', 'all_cases[:608]'),
        ('{UNKNOWN, TYPO}][:607]', '{UNKNOWN, TYPO}][:608]'),
        ('!= 607', '!= 608'),
        ('kreeg 607', 'kreeg 608'),
        ('590, 591, 592, 593, 594', '591, 592, 593, 594, 595'),
    ],
)

build(
    'create-six-hundred-twenty-two-minimal.py',
    'create-six-hundred-twenty-three-minimal.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('!= 607', '!= 608'),
        ('kreeg 607', 'kreeg 608'),
        ('590, 591, 592, 593, 594', '591, 592, 593, 594, 595'),
    ],
)

build(
    'make-six-hundred-twenty-two.py',
    'make-six-hundred-twenty-three.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('all_cases[:607]', 'all_cases[:608]'),
        ('{UNKNOWN, TYPO}][:607]', '{UNKNOWN, TYPO}][:608]'),
        ('!= 607', '!= 608'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
    ],
)

build(
    'create-six-hundred-twenty-two-files.py',
    'create-six-hundred-twenty-three-files.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('all_cases[:607]', 'all_cases[:608]'),
        ('{UNKNOWN, TYPO}][:607]', '{UNKNOWN, TYPO}][:608]'),
        ('!= 607', '!= 608'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
    ],
)

build(
    'create-six-hundred-twenty-two.py',
    'create-six-hundred-twenty-three.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('all_cases[:607]', 'all_cases[:608]'),
        ('{UNKNOWN, TYPO}][:607]', '{UNKNOWN, TYPO}][:608]'),
        ('!= 607', '!= 608'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-two.py',
    'generate-validate-six-hundred-twenty-three.py',
    [
        ('six-hundred-twenty-two', 'six-hundred-twenty-three'),
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('all_cases[:607]', 'all_cases[:608]'),
        ('{UNKNOWN, TYPO}][:607]', '{UNKNOWN, TYPO}][:608]'),
        ('!= 607', '!= 608'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
    ],
)

build(
    'validate-six-hundred-twenty-two-valid-list-cases.py',
    'validate-six-hundred-twenty-three-valid-list-cases.py',
    [
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('592, 593, 594, 595, 596', '593, 594, 595, 596, 597'),
        ('all_cases[:607]', 'all_cases[:608]'),
        ('len(valid_cases) != 607', 'len(valid_cases) != 608'),
    ],
)

build(
    'validate-six-hundred-twenty-two-valid-mixed.py',
    'validate-six-hundred-twenty-three-valid-mixed.py',
    [
        ('zeshonderdtweeëntwintig', 'zeshonderddrieëntwintig'),
        ('592, 593, 594, 595, 596', '593, 594, 595, 596, 597'),
        ('][:607]', '][:608]'),
        ('len(valid_cases) != 607', 'len(valid_cases) != 608'),
        ('plain stderr noemt niet alle zeshonderdzeven geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdacht geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-two.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-two', 'six-hundred-twenty-three')
(ROOT / 'verify-six-hundred-twenty-three.py').write_text(verify_text)
print('verify-six-hundred-twenty-three.py')
