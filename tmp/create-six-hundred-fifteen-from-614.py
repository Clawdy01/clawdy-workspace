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
    'create-six-hundred-fourteen-assets.py',
    'create-six-hundred-fifteen-assets.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('[:599]', '[:600]'),
        ('!= 599', '!= 600'),
        ('kreeg 599', 'kreeg 600'),
        ('586, 587, 588, 589, 590', '587, 588, 589, 590, 591'),
    ],
)

build(
    'create-six-hundred-fourteen-bootstrap.py',
    'create-six-hundred-fifteen-bootstrap.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('all_cases[:599]', 'all_cases[:600]'),
        ('{UNKNOWN, TYPO}][:599]', '{UNKNOWN, TYPO}][:600]'),
        ('!= 599', '!= 600'),
        ('kreeg 599', 'kreeg 600'),
        ('582, 583, 584, 585, 586', '583, 584, 585, 586, 587'),
    ],
)

build(
    'create-six-hundred-fourteen-minimal.py',
    'create-six-hundred-fifteen-minimal.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('!= 599', '!= 600'),
        ('kreeg 599', 'kreeg 600'),
        ('582, 583, 584, 585, 586', '583, 584, 585, 586, 587'),
    ],
)

build(
    'make-six-hundred-fourteen.py',
    'make-six-hundred-fifteen.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('all_cases[:599]', 'all_cases[:600]'),
        ('{UNKNOWN, TYPO}][:599]', '{UNKNOWN, TYPO}][:600]'),
        ('!= 599', '!= 600'),
        ('522, 523, 524, 525, 526', '523, 524, 525, 526, 527'),
    ],
)

build(
    'create-six-hundred-fourteen-files.py',
    'create-six-hundred-fifteen-files.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('all_cases[:599]', 'all_cases[:600]'),
        ('{UNKNOWN, TYPO}][:599]', '{UNKNOWN, TYPO}][:600]'),
        ('!= 599', '!= 600'),
        ('522, 523, 524, 525, 526', '523, 524, 525, 526, 527'),
    ],
)

build(
    'create-six-hundred-fourteen.py',
    'create-six-hundred-fifteen.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('all_cases[:599]', 'all_cases[:600]'),
        ('{UNKNOWN, TYPO}][:599]', '{UNKNOWN, TYPO}][:600]'),
        ('!= 599', '!= 600'),
        ('525, 526, 527, 528, 529', '526, 527, 528, 529, 530'),
    ],
)

build(
    'generate-validate-six-hundred-fourteen.py',
    'generate-validate-six-hundred-fifteen.py',
    [
        ('six-hundred-fourteen', 'six-hundred-fifteen'),
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('all_cases[:599]', 'all_cases[:600]'),
        ('{UNKNOWN, TYPO}][:599]', '{UNKNOWN, TYPO}][:600]'),
        ('!= 599', '!= 600'),
        ('522, 523, 524, 525, 526', '523, 524, 525, 526, 527'),
    ],
)

build(
    'validate-six-hundred-fourteen-valid-list-cases.py',
    'validate-six-hundred-fifteen-valid-list-cases.py',
    [
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('584, 585, 586, 587, 588', '585, 586, 587, 588, 589'),
        ('all_cases[:599]', 'all_cases[:600]'),
        ('len(valid_cases) != 599', 'len(valid_cases) != 600'),
    ],
)

build(
    'validate-six-hundred-fourteen-valid-mixed.py',
    'validate-six-hundred-fifteen-valid-mixed.py',
    [
        ('zeshonderdveertien', 'zeshonderdvijftien'),
        ('584, 585, 586, 587, 588', '585, 586, 587, 588, 589'),
        ('][:599]', '][:600]'),
        ('len(valid_cases) != 599', 'len(valid_cases) != 600'),
        ('plain stderr noemt niet alle vijfhonderdnegenennegentig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderd geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-fourteen.py').read_text()
verify_text = verify_src.replace('six-hundred-fourteen', 'six-hundred-fifteen')
(ROOT / 'verify-six-hundred-fifteen.py').write_text(verify_text)
print('verify-six-hundred-fifteen.py')
