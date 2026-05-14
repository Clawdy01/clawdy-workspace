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
    'create-six-hundred-twenty-three-assets.py',
    'create-six-hundred-twenty-four-assets.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('[:608]', '[:609]'),
        ('!= 608', '!= 609'),
        ('kreeg 608', 'kreeg 609'),
        ('595, 596, 597, 598, 599', '596, 597, 598, 599, 600'),
    ],
)

build(
    'create-six-hundred-twenty-three-bootstrap.py',
    'create-six-hundred-twenty-four-bootstrap.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('all_cases[:608]', 'all_cases[:609]'),
        ('{UNKNOWN, TYPO}][:608]', '{UNKNOWN, TYPO}][:609]'),
        ('!= 608', '!= 609'),
        ('kreeg 608', 'kreeg 609'),
        ('591, 592, 593, 594, 595', '592, 593, 594, 595, 596'),
    ],
)

build(
    'create-six-hundred-twenty-three-minimal.py',
    'create-six-hundred-twenty-four-minimal.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('!= 608', '!= 609'),
        ('kreeg 608', 'kreeg 609'),
        ('591, 592, 593, 594, 595', '592, 593, 594, 595, 596'),
    ],
)

build(
    'make-six-hundred-twenty-three.py',
    'make-six-hundred-twenty-four.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('all_cases[:608]', 'all_cases[:609]'),
        ('{UNKNOWN, TYPO}][:608]', '{UNKNOWN, TYPO}][:609]'),
        ('!= 608', '!= 609'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
    ],
)

build(
    'create-six-hundred-twenty-three-files.py',
    'create-six-hundred-twenty-four-files.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('all_cases[:608]', 'all_cases[:609]'),
        ('{UNKNOWN, TYPO}][:608]', '{UNKNOWN, TYPO}][:609]'),
        ('!= 608', '!= 609'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
    ],
)

build(
    'create-six-hundred-twenty-three.py',
    'create-six-hundred-twenty-four.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('all_cases[:608]', 'all_cases[:609]'),
        ('{UNKNOWN, TYPO}][:608]', '{UNKNOWN, TYPO}][:609]'),
        ('!= 608', '!= 609'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-three.py',
    'generate-validate-six-hundred-twenty-four.py',
    [
        ('six-hundred-twenty-three', 'six-hundred-twenty-four'),
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('all_cases[:608]', 'all_cases[:609]'),
        ('{UNKNOWN, TYPO}][:608]', '{UNKNOWN, TYPO}][:609]'),
        ('!= 608', '!= 609'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
    ],
)

build(
    'validate-six-hundred-twenty-three-valid-list-cases.py',
    'validate-six-hundred-twenty-four-valid-list-cases.py',
    [
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('593, 594, 595, 596, 597', '594, 595, 596, 597, 598'),
        ('all_cases[:608]', 'all_cases[:609]'),
        ('len(valid_cases) != 608', 'len(valid_cases) != 609'),
    ],
)

build(
    'validate-six-hundred-twenty-three-valid-mixed.py',
    'validate-six-hundred-twenty-four-valid-mixed.py',
    [
        ('zeshonderddrieëntwintig', 'zeshonderdvierentwintig'),
        ('593, 594, 595, 596, 597', '594, 595, 596, 597, 598'),
        ('][:608]', '][:609]'),
        ('len(valid_cases) != 608', 'len(valid_cases) != 609'),
        ('plain stderr noemt niet alle zeshonderdacht geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdnegen geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-three.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-three', 'six-hundred-twenty-four')
(ROOT / 'verify-six-hundred-twenty-four.py').write_text(verify_text)
print('verify-six-hundred-twenty-four.py')
