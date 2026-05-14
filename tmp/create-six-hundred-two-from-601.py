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
    'create-six-hundred-one-assets.py',
    'create-six-hundred-two-assets.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('[:586]', '[:587]'),
        ('!= 586', '!= 587'),
        ('kreeg 586', 'kreeg 587'),
        ('573, 574, 575, 576, 577', '574, 575, 576, 577, 578'),
    ],
)

build(
    'create-six-hundred-one-bootstrap.py',
    'create-six-hundred-two-bootstrap.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('all_cases[:586]', 'all_cases[:587]'),
        ('{UNKNOWN, TYPO}][:586]', '{UNKNOWN, TYPO}][:587]'),
        ('!= 586', '!= 587'),
        ('kreeg 586', 'kreeg 587'),
        ('569, 570, 571, 572, 573', '570, 571, 572, 573, 574'),
    ],
)

build(
    'create-six-hundred-one-minimal.py',
    'create-six-hundred-two-minimal.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('!= 586', '!= 587'),
        ('kreeg 586', 'kreeg 587'),
        ('569, 570, 571, 572, 573', '570, 571, 572, 573, 574'),
    ],
)

build(
    'make-six-hundred-one.py',
    'make-six-hundred-two.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('all_cases[:586]', 'all_cases[:587]'),
        ('{UNKNOWN, TYPO}][:586]', '{UNKNOWN, TYPO}][:587]'),
        ('!= 586', '!= 587'),
        ('509, 510, 511, 512, 513', '510, 511, 512, 513, 514'),
    ],
)

build(
    'create-six-hundred-one-files.py',
    'create-six-hundred-two-files.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('all_cases[:586]', 'all_cases[:587]'),
        ('{UNKNOWN, TYPO}][:586]', '{UNKNOWN, TYPO}][:587]'),
        ('!= 586', '!= 587'),
        ('509, 510, 511, 512, 513', '510, 511, 512, 513, 514'),
    ],
)

build(
    'create-six-hundred-one.py',
    'create-six-hundred-two.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('all_cases[:586]', 'all_cases[:587]'),
        ('{UNKNOWN, TYPO}][:586]', '{UNKNOWN, TYPO}][:587]'),
        ('!= 586', '!= 587'),
        ('512, 513, 514, 515, 516', '513, 514, 515, 516, 517'),
    ],
)

build(
    'generate-validate-six-hundred-one.py',
    'generate-validate-six-hundred-two.py',
    [
        ('six-hundred-one', 'six-hundred-two'),
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('all_cases[:586]', 'all_cases[:587]'),
        ('{UNKNOWN, TYPO}][:586]', '{UNKNOWN, TYPO}][:587]'),
        ('!= 586', '!= 587'),
        ('509, 510, 511, 512, 513', '510, 511, 512, 513, 514'),
    ],
)

build(
    'validate-six-hundred-one-valid-list-cases.py',
    'validate-six-hundred-two-valid-list-cases.py',
    [
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('571, 572, 573, 574, 575', '572, 573, 574, 575, 576'),
        ('all_cases[:586]', 'all_cases[:587]'),
        ('len(valid_cases) != 586', 'len(valid_cases) != 587'),
    ],
)

build(
    'validate-six-hundred-one-valid-mixed.py',
    'validate-six-hundred-two-valid-mixed.py',
    [
        ('zeshonderdeen', 'zeshonderdtwee'),
        ('571, 572, 573, 574, 575', '572, 573, 574, 575, 576'),
        ('][:586]', '][:587]'),
        ('len(valid_cases) != 586', 'len(valid_cases) != 587'),
        ('plain stderr noemt niet alle vijfhonderdzesentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzevenentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-one.py').read_text()
verify_text = verify_src.replace('six-hundred-one', 'six-hundred-two')
(ROOT / 'verify-six-hundred-two.py').write_text(verify_text)
print('verify-six-hundred-two.py')
