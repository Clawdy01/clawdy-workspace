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
    'create-six-hundred-fifty-one-assets.py',
    'create-six-hundred-fifty-two-assets.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('[:636]', '[:637]'),
        ('!= 636', '!= 637'),
        ('kreeg 636', 'kreeg 637'),
        ('623, 624, 625, 626, 627', '624, 625, 626, 627, 628'),
    ],
)

build(
    'create-six-hundred-fifty-one-bootstrap.py',
    'create-six-hundred-fifty-two-bootstrap.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('all_cases[:636]', 'all_cases[:637]'),
        ('{UNKNOWN, TYPO}][:636]', '{UNKNOWN, TYPO}][:637]'),
        ('!= 636', '!= 637'),
        ('kreeg 636', 'kreeg 637'),
        ('619, 620, 621, 622, 623', '620, 621, 622, 623, 624'),
    ],
)

build(
    'create-six-hundred-fifty-one-minimal.py',
    'create-six-hundred-fifty-two-minimal.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('!= 636', '!= 637'),
        ('kreeg 636', 'kreeg 637'),
        ('619, 620, 621, 622, 623', '620, 621, 622, 623, 624'),
    ],
)

build(
    'make-six-hundred-fifty-one.py',
    'make-six-hundred-fifty-two.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('all_cases[:636]', 'all_cases[:637]'),
        ('{UNKNOWN, TYPO}][:636]', '{UNKNOWN, TYPO}][:637]'),
        ('!= 636', '!= 637'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'create-six-hundred-fifty-one-files.py',
    'create-six-hundred-fifty-two-files.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('all_cases[:636]', 'all_cases[:637]'),
        ('{UNKNOWN, TYPO}][:636]', '{UNKNOWN, TYPO}][:637]'),
        ('!= 636', '!= 637'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'create-six-hundred-fifty-one.py',
    'create-six-hundred-fifty-two.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('all_cases[:636]', 'all_cases[:637]'),
        ('{UNKNOWN, TYPO}][:636]', '{UNKNOWN, TYPO}][:637]'),
        ('!= 636', '!= 637'),
        ('562, 563, 564, 565, 566', '563, 564, 565, 566, 567'),
    ],
)

build(
    'generate-validate-six-hundred-fifty-one.py',
    'generate-validate-six-hundred-fifty-two.py',
    [
        ('six-hundred-fifty-one', 'six-hundred-fifty-two'),
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('all_cases[:636]', 'all_cases[:637]'),
        ('{UNKNOWN, TYPO}][:636]', '{UNKNOWN, TYPO}][:637]'),
        ('!= 636', '!= 637'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'validate-six-hundred-fifty-one-valid-list-cases.py',
    'validate-six-hundred-fifty-two-valid-list-cases.py',
    [
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('621, 622, 623, 624, 625', '622, 623, 624, 625, 626'),
        ('all_cases[:636]', 'all_cases[:637]'),
        ('len(valid_cases) != 636', 'len(valid_cases) != 637'),
    ],
)

build(
    'validate-six-hundred-fifty-one-valid-mixed.py',
    'validate-six-hundred-fifty-two-valid-mixed.py',
    [
        ('zeshonderdeenenvijftig', 'zeshonderdtweeënvijftig'),
        ('621, 622, 623, 624, 625', '622, 623, 624, 625, 626'),
        ('][:636]', '][:637]'),
        ('len(valid_cases) != 636', 'len(valid_cases) != 637'),
        ('plain stderr noemt niet alle zeshonderdzesendertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzevenendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-fifty-one.py').read_text()
verify_text = verify_src.replace('six-hundred-fifty-one', 'six-hundred-fifty-two')
(ROOT / 'verify-six-hundred-fifty-two.py').write_text(verify_text)
print('verify-six-hundred-fifty-two.py')
