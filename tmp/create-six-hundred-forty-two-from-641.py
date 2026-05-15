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
    'create-six-hundred-forty-one-assets.py',
    'create-six-hundred-forty-two-assets.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('[:626]', '[:627]'),
        ('!= 626', '!= 627'),
        ('kreeg 626', 'kreeg 627'),
        ('613, 614, 615, 616, 617', '614, 615, 616, 617, 618'),
    ],
)

build(
    'create-six-hundred-forty-one-bootstrap.py',
    'create-six-hundred-forty-two-bootstrap.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('all_cases[:626]', 'all_cases[:627]'),
        ('{UNKNOWN, TYPO}][:626]', '{UNKNOWN, TYPO}][:627]'),
        ('!= 626', '!= 627'),
        ('kreeg 626', 'kreeg 627'),
        ('609, 610, 611, 612, 613', '610, 611, 612, 613, 614'),
    ],
)

build(
    'create-six-hundred-forty-one-minimal.py',
    'create-six-hundred-forty-two-minimal.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('!= 626', '!= 627'),
        ('kreeg 626', 'kreeg 627'),
        ('609, 610, 611, 612, 613', '610, 611, 612, 613, 614'),
    ],
)

build(
    'make-six-hundred-forty-one.py',
    'make-six-hundred-forty-two.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('all_cases[:626]', 'all_cases[:627]'),
        ('{UNKNOWN, TYPO}][:626]', '{UNKNOWN, TYPO}][:627]'),
        ('!= 626', '!= 627'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'create-six-hundred-forty-one-files.py',
    'create-six-hundred-forty-two-files.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('all_cases[:626]', 'all_cases[:627]'),
        ('{UNKNOWN, TYPO}][:626]', '{UNKNOWN, TYPO}][:627]'),
        ('!= 626', '!= 627'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'create-six-hundred-forty-one.py',
    'create-six-hundred-forty-two.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('all_cases[:626]', 'all_cases[:627]'),
        ('{UNKNOWN, TYPO}][:626]', '{UNKNOWN, TYPO}][:627]'),
        ('!= 626', '!= 627'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'generate-validate-six-hundred-forty-one.py',
    'generate-validate-six-hundred-forty-two.py',
    [
        ('six-hundred-forty-one', 'six-hundred-forty-two'),
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('all_cases[:626]', 'all_cases[:627]'),
        ('{UNKNOWN, TYPO}][:626]', '{UNKNOWN, TYPO}][:627]'),
        ('!= 626', '!= 627'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'validate-six-hundred-forty-one-valid-list-cases.py',
    'validate-six-hundred-forty-two-valid-list-cases.py',
    [
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('611, 612, 613, 614, 615', '612, 613, 614, 615, 616'),
        ('all_cases[:626]', 'all_cases[:627]'),
        ('len(valid_cases) != 626', 'len(valid_cases) != 627'),
    ],
)

build(
    'validate-six-hundred-forty-one-valid-mixed.py',
    'validate-six-hundred-forty-two-valid-mixed.py',
    [
        ('zeshonderdeenenveertig', 'zeshonderdtweeënveertig'),
        ('611, 612, 613, 614, 615', '612, 613, 614, 615, 616'),
        ('][:626]', '][:627]'),
        ('len(valid_cases) != 626', 'len(valid_cases) != 627'),
        ('plain stderr noemt niet alle zeshonderdzesentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzevenentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-one.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-one', 'six-hundred-forty-two')
(ROOT / 'verify-six-hundred-forty-two.py').write_text(verify_text)
print('verify-six-hundred-forty-two.py')
