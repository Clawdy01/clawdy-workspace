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
    'create-six-hundred-thirteen-assets.py',
    'create-six-hundred-fourteen-assets.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('[:598]', '[:599]'),
        ('!= 598', '!= 599'),
        ('kreeg 598', 'kreeg 599'),
        ('585, 586, 587, 588, 589', '586, 587, 588, 589, 590'),
    ],
)

build(
    'create-six-hundred-thirteen-bootstrap.py',
    'create-six-hundred-fourteen-bootstrap.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('all_cases[:598]', 'all_cases[:599]'),
        ('{UNKNOWN, TYPO}][:598]', '{UNKNOWN, TYPO}][:599]'),
        ('!= 598', '!= 599'),
        ('kreeg 598', 'kreeg 599'),
        ('581, 582, 583, 584, 585', '582, 583, 584, 585, 586'),
    ],
)

build(
    'create-six-hundred-thirteen-minimal.py',
    'create-six-hundred-fourteen-minimal.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('!= 598', '!= 599'),
        ('kreeg 598', 'kreeg 599'),
        ('581, 582, 583, 584, 585', '582, 583, 584, 585, 586'),
    ],
)

build(
    'make-six-hundred-thirteen.py',
    'make-six-hundred-fourteen.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('all_cases[:598]', 'all_cases[:599]'),
        ('{UNKNOWN, TYPO}][:598]', '{UNKNOWN, TYPO}][:599]'),
        ('!= 598', '!= 599'),
        ('521, 522, 523, 524, 525', '522, 523, 524, 525, 526'),
    ],
)

build(
    'create-six-hundred-thirteen-files.py',
    'create-six-hundred-fourteen-files.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('all_cases[:598]', 'all_cases[:599]'),
        ('{UNKNOWN, TYPO}][:598]', '{UNKNOWN, TYPO}][:599]'),
        ('!= 598', '!= 599'),
        ('521, 522, 523, 524, 525', '522, 523, 524, 525, 526'),
    ],
)

build(
    'create-six-hundred-thirteen.py',
    'create-six-hundred-fourteen.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('all_cases[:598]', 'all_cases[:599]'),
        ('{UNKNOWN, TYPO}][:598]', '{UNKNOWN, TYPO}][:599]'),
        ('!= 598', '!= 599'),
        ('524, 525, 526, 527, 528', '525, 526, 527, 528, 529'),
    ],
)

build(
    'generate-validate-six-hundred-thirteen.py',
    'generate-validate-six-hundred-fourteen.py',
    [
        ('six-hundred-thirteen', 'six-hundred-fourteen'),
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('all_cases[:598]', 'all_cases[:599]'),
        ('{UNKNOWN, TYPO}][:598]', '{UNKNOWN, TYPO}][:599]'),
        ('!= 598', '!= 599'),
        ('521, 522, 523, 524, 525', '522, 523, 524, 525, 526'),
    ],
)

build(
    'validate-six-hundred-thirteen-valid-list-cases.py',
    'validate-six-hundred-fourteen-valid-list-cases.py',
    [
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('583, 584, 585, 586, 587', '584, 585, 586, 587, 588'),
        ('all_cases[:598]', 'all_cases[:599]'),
        ('len(valid_cases) != 598', 'len(valid_cases) != 599'),
    ],
)

build(
    'validate-six-hundred-thirteen-valid-mixed.py',
    'validate-six-hundred-fourteen-valid-mixed.py',
    [
        ('zeshonderddertien', 'zeshonderdveertien'),
        ('583, 584, 585, 586, 587', '584, 585, 586, 587, 588'),
        ('][:598]', '][:599]'),
        ('len(valid_cases) != 598', 'len(valid_cases) != 599'),
        ('plain stderr noemt niet alle vijfhonderdachtennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdnegenennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirteen.py').read_text()
verify_text = verify_src.replace('six-hundred-thirteen', 'six-hundred-fourteen')
(ROOT / 'verify-six-hundred-fourteen.py').write_text(verify_text)
print('verify-six-hundred-fourteen.py')
