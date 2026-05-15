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
    'create-six-hundred-forty-two-assets.py',
    'create-six-hundred-forty-three-assets.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('[:627]', '[:628]'),
        ('!= 627', '!= 628'),
        ('kreeg 627', 'kreeg 628'),
        ('614, 615, 616, 617, 618', '615, 616, 617, 618, 619'),
    ],
)

build(
    'create-six-hundred-forty-two-bootstrap.py',
    'create-six-hundred-forty-three-bootstrap.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('all_cases[:627]', 'all_cases[:628]'),
        ('{UNKNOWN, TYPO}][:627]', '{UNKNOWN, TYPO}][:628]'),
        ('!= 627', '!= 628'),
        ('kreeg 627', 'kreeg 628'),
        ('610, 611, 612, 613, 614', '611, 612, 613, 614, 615'),
    ],
)

build(
    'create-six-hundred-forty-two-minimal.py',
    'create-six-hundred-forty-three-minimal.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('!= 627', '!= 628'),
        ('kreeg 627', 'kreeg 628'),
        ('610, 611, 612, 613, 614', '611, 612, 613, 614, 615'),
    ],
)

build(
    'make-six-hundred-forty-two.py',
    'make-six-hundred-forty-three.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('all_cases[:627]', 'all_cases[:628]'),
        ('{UNKNOWN, TYPO}][:627]', '{UNKNOWN, TYPO}][:628]'),
        ('!= 627', '!= 628'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'create-six-hundred-forty-two-files.py',
    'create-six-hundred-forty-three-files.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('all_cases[:627]', 'all_cases[:628]'),
        ('{UNKNOWN, TYPO}][:627]', '{UNKNOWN, TYPO}][:628]'),
        ('!= 627', '!= 628'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'create-six-hundred-forty-two.py',
    'create-six-hundred-forty-three.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('all_cases[:627]', 'all_cases[:628]'),
        ('{UNKNOWN, TYPO}][:627]', '{UNKNOWN, TYPO}][:628]'),
        ('!= 627', '!= 628'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'generate-validate-six-hundred-forty-two.py',
    'generate-validate-six-hundred-forty-three.py',
    [
        ('six-hundred-forty-two', 'six-hundred-forty-three'),
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('all_cases[:627]', 'all_cases[:628]'),
        ('{UNKNOWN, TYPO}][:627]', '{UNKNOWN, TYPO}][:628]'),
        ('!= 627', '!= 628'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'validate-six-hundred-forty-two-valid-list-cases.py',
    'validate-six-hundred-forty-three-valid-list-cases.py',
    [
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('612, 613, 614, 615, 616', '613, 614, 615, 616, 617'),
        ('all_cases[:627]', 'all_cases[:628]'),
        ('len(valid_cases) != 627', 'len(valid_cases) != 628'),
    ],
)

build(
    'validate-six-hundred-forty-two-valid-mixed.py',
    'validate-six-hundred-forty-three-valid-mixed.py',
    [
        ('zeshonderdtweeënveertig', 'zeshonderddrieënveertig'),
        ('612, 613, 614, 615, 616', '613, 614, 615, 616, 617'),
        ('][:627]', '][:628]'),
        ('len(valid_cases) != 627', 'len(valid_cases) != 628'),
        ('plain stderr noemt niet alle zeshonderdzevenentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdachtentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-two.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-two', 'six-hundred-forty-three')
(ROOT / 'verify-six-hundred-forty-three.py').write_text(verify_text)
print('verify-six-hundred-forty-three.py')
