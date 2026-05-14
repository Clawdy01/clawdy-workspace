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
    'create-six-hundred-three-assets.py',
    'create-six-hundred-four-assets.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('[:588]', '[:589]'),
        ('!= 588', '!= 589'),
        ('kreeg 588', 'kreeg 589'),
        ('575, 576, 577, 578, 579', '576, 577, 578, 579, 580'),
    ],
)

build(
    'create-six-hundred-three-bootstrap.py',
    'create-six-hundred-four-bootstrap.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('all_cases[:588]', 'all_cases[:589]'),
        ('{UNKNOWN, TYPO}][:588]', '{UNKNOWN, TYPO}][:589]'),
        ('!= 588', '!= 589'),
        ('kreeg 588', 'kreeg 589'),
        ('571, 572, 573, 574, 575', '572, 573, 574, 575, 576'),
    ],
)

build(
    'create-six-hundred-three-minimal.py',
    'create-six-hundred-four-minimal.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('!= 588', '!= 589'),
        ('kreeg 588', 'kreeg 589'),
        ('571, 572, 573, 574, 575', '572, 573, 574, 575, 576'),
    ],
)

build(
    'make-six-hundred-three.py',
    'make-six-hundred-four.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('all_cases[:588]', 'all_cases[:589]'),
        ('{UNKNOWN, TYPO}][:588]', '{UNKNOWN, TYPO}][:589]'),
        ('!= 588', '!= 589'),
        ('511, 512, 513, 514, 515', '512, 513, 514, 515, 516'),
    ],
)

build(
    'create-six-hundred-three-files.py',
    'create-six-hundred-four-files.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('all_cases[:588]', 'all_cases[:589]'),
        ('{UNKNOWN, TYPO}][:588]', '{UNKNOWN, TYPO}][:589]'),
        ('!= 588', '!= 589'),
        ('511, 512, 513, 514, 515', '512, 513, 514, 515, 516'),
    ],
)

build(
    'create-six-hundred-three.py',
    'create-six-hundred-four.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('all_cases[:588]', 'all_cases[:589]'),
        ('{UNKNOWN, TYPO}][:588]', '{UNKNOWN, TYPO}][:589]'),
        ('!= 588', '!= 589'),
        ('514, 515, 516, 517, 518', '515, 516, 517, 518, 519'),
    ],
)

build(
    'generate-validate-six-hundred-three.py',
    'generate-validate-six-hundred-four.py',
    [
        ('six-hundred-three', 'six-hundred-four'),
        ('zeshonderddrie', 'zeshonderdvier'),
        ('all_cases[:588]', 'all_cases[:589]'),
        ('{UNKNOWN, TYPO}][:588]', '{UNKNOWN, TYPO}][:589]'),
        ('!= 588', '!= 589'),
        ('511, 512, 513, 514, 515', '512, 513, 514, 515, 516'),
    ],
)

build(
    'validate-six-hundred-three-valid-list-cases.py',
    'validate-six-hundred-four-valid-list-cases.py',
    [
        ('zeshonderddrie', 'zeshonderdvier'),
        ('573, 574, 575, 576, 577', '574, 575, 576, 577, 578'),
        ('all_cases[:588]', 'all_cases[:589]'),
        ('len(valid_cases) != 588', 'len(valid_cases) != 589'),
    ],
)

build(
    'validate-six-hundred-three-valid-mixed.py',
    'validate-six-hundred-four-valid-mixed.py',
    [
        ('zeshonderddrie', 'zeshonderdvier'),
        ('573, 574, 575, 576, 577', '574, 575, 576, 577, 578'),
        ('][:588]', '][:589]'),
        ('len(valid_cases) != 588', 'len(valid_cases) != 589'),
        ('plain stderr noemt niet alle vijfhonderdachtentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdnegenentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-three.py').read_text()
verify_text = verify_src.replace('six-hundred-three', 'six-hundred-four')
(ROOT / 'verify-six-hundred-four.py').write_text(verify_text)
print('verify-six-hundred-four.py')
