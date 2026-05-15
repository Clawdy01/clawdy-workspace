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
    'create-six-hundred-forty-three-assets.py',
    'create-six-hundred-forty-four-assets.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('[:628]', '[:629]'),
        ('!= 628', '!= 629'),
        ('kreeg 628', 'kreeg 629'),
        ('615, 616, 617, 618, 619', '616, 617, 618, 619, 620'),
    ],
)

build(
    'create-six-hundred-forty-three-bootstrap.py',
    'create-six-hundred-forty-four-bootstrap.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('all_cases[:628]', 'all_cases[:629]'),
        ('{UNKNOWN, TYPO}][:628]', '{UNKNOWN, TYPO}][:629]'),
        ('!= 628', '!= 629'),
        ('kreeg 628', 'kreeg 629'),
        ('611, 612, 613, 614, 615', '612, 613, 614, 615, 616'),
    ],
)

build(
    'create-six-hundred-forty-three-minimal.py',
    'create-six-hundred-forty-four-minimal.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('!= 628', '!= 629'),
        ('kreeg 628', 'kreeg 629'),
        ('611, 612, 613, 614, 615', '612, 613, 614, 615, 616'),
    ],
)

build(
    'make-six-hundred-forty-three.py',
    'make-six-hundred-forty-four.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('all_cases[:628]', 'all_cases[:629]'),
        ('{UNKNOWN, TYPO}][:628]', '{UNKNOWN, TYPO}][:629]'),
        ('!= 628', '!= 629'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'create-six-hundred-forty-three-files.py',
    'create-six-hundred-forty-four-files.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('all_cases[:628]', 'all_cases[:629]'),
        ('{UNKNOWN, TYPO}][:628]', '{UNKNOWN, TYPO}][:629]'),
        ('!= 628', '!= 629'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'create-six-hundred-forty-three.py',
    'create-six-hundred-forty-four.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('all_cases[:628]', 'all_cases[:629]'),
        ('{UNKNOWN, TYPO}][:628]', '{UNKNOWN, TYPO}][:629]'),
        ('!= 628', '!= 629'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'generate-validate-six-hundred-forty-three.py',
    'generate-validate-six-hundred-forty-four.py',
    [
        ('six-hundred-forty-three', 'six-hundred-forty-four'),
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('all_cases[:628]', 'all_cases[:629]'),
        ('{UNKNOWN, TYPO}][:628]', '{UNKNOWN, TYPO}][:629]'),
        ('!= 628', '!= 629'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'validate-six-hundred-forty-three-valid-list-cases.py',
    'validate-six-hundred-forty-four-valid-list-cases.py',
    [
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('613, 614, 615, 616, 617', '614, 615, 616, 617, 618'),
        ('all_cases[:628]', 'all_cases[:629]'),
        ('len(valid_cases) != 628', 'len(valid_cases) != 629'),
    ],
)

build(
    'validate-six-hundred-forty-three-valid-mixed.py',
    'validate-six-hundred-forty-four-valid-mixed.py',
    [
        ('zeshonderddrieënveertig', 'zeshonderdvierenveertig'),
        ('613, 614, 615, 616, 617', '614, 615, 616, 617, 618'),
        ('][:628]', '][:629]'),
        ('len(valid_cases) != 628', 'len(valid_cases) != 629'),
        ('plain stderr noemt niet alle zeshonderdachtentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdnegenentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-three.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-three', 'six-hundred-forty-four')
(ROOT / 'verify-six-hundred-forty-four.py').write_text(verify_text)
print('verify-six-hundred-forty-four.py')
