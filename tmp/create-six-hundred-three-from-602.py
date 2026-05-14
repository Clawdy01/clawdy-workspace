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
    'create-six-hundred-two-assets.py',
    'create-six-hundred-three-assets.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('[:587]', '[:588]'),
        ('!= 587', '!= 588'),
        ('kreeg 587', 'kreeg 588'),
        ('574, 575, 576, 577, 578', '575, 576, 577, 578, 579'),
    ],
)

build(
    'create-six-hundred-two-bootstrap.py',
    'create-six-hundred-three-bootstrap.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('all_cases[:587]', 'all_cases[:588]'),
        ('{UNKNOWN, TYPO}][:587]', '{UNKNOWN, TYPO}][:588]'),
        ('!= 587', '!= 588'),
        ('kreeg 587', 'kreeg 588'),
        ('570, 571, 572, 573, 574', '571, 572, 573, 574, 575'),
    ],
)

build(
    'create-six-hundred-two-minimal.py',
    'create-six-hundred-three-minimal.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('!= 587', '!= 588'),
        ('kreeg 587', 'kreeg 588'),
        ('570, 571, 572, 573, 574', '571, 572, 573, 574, 575'),
    ],
)

build(
    'make-six-hundred-two.py',
    'make-six-hundred-three.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('all_cases[:587]', 'all_cases[:588]'),
        ('{UNKNOWN, TYPO}][:587]', '{UNKNOWN, TYPO}][:588]'),
        ('!= 587', '!= 588'),
        ('510, 511, 512, 513, 514', '511, 512, 513, 514, 515'),
    ],
)

build(
    'create-six-hundred-two-files.py',
    'create-six-hundred-three-files.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('all_cases[:587]', 'all_cases[:588]'),
        ('{UNKNOWN, TYPO}][:587]', '{UNKNOWN, TYPO}][:588]'),
        ('!= 587', '!= 588'),
        ('510, 511, 512, 513, 514', '511, 512, 513, 514, 515'),
    ],
)

build(
    'create-six-hundred-two.py',
    'create-six-hundred-three.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('all_cases[:587]', 'all_cases[:588]'),
        ('{UNKNOWN, TYPO}][:587]', '{UNKNOWN, TYPO}][:588]'),
        ('!= 587', '!= 588'),
        ('513, 514, 515, 516, 517', '514, 515, 516, 517, 518'),
    ],
)

build(
    'generate-validate-six-hundred-two.py',
    'generate-validate-six-hundred-three.py',
    [
        ('six-hundred-two', 'six-hundred-three'),
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('all_cases[:587]', 'all_cases[:588]'),
        ('{UNKNOWN, TYPO}][:587]', '{UNKNOWN, TYPO}][:588]'),
        ('!= 587', '!= 588'),
        ('510, 511, 512, 513, 514', '511, 512, 513, 514, 515'),
    ],
)

build(
    'validate-six-hundred-two-valid-list-cases.py',
    'validate-six-hundred-three-valid-list-cases.py',
    [
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('572, 573, 574, 575, 576', '573, 574, 575, 576, 577'),
        ('all_cases[:587]', 'all_cases[:588]'),
        ('len(valid_cases) != 587', 'len(valid_cases) != 588'),
    ],
)

build(
    'validate-six-hundred-two-valid-mixed.py',
    'validate-six-hundred-three-valid-mixed.py',
    [
        ('zeshonderdtwee', 'zeshonderddrie'),
        ('572, 573, 574, 575, 576', '573, 574, 575, 576, 577'),
        ('][:587]', '][:588]'),
        ('len(valid_cases) != 587', 'len(valid_cases) != 588'),
        ('plain stderr noemt niet alle vijfhonderdzevenentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdachtentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-two.py').read_text()
verify_text = verify_src.replace('six-hundred-two', 'six-hundred-three')
(ROOT / 'verify-six-hundred-three.py').write_text(verify_text)
print('verify-six-hundred-three.py')
