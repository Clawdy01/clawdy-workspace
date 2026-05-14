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
    'create-six-hundred-seventeen-assets.py',
    'create-six-hundred-eighteen-assets.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('[:602]', '[:603]'),
        ('!= 602', '!= 603'),
        ('kreeg 602', 'kreeg 603'),
        ('589, 590, 591, 592, 593', '590, 591, 592, 593, 594'),
    ],
)

build(
    'create-six-hundred-seventeen-bootstrap.py',
    'create-six-hundred-eighteen-bootstrap.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('all_cases[:602]', 'all_cases[:603]'),
        ('{UNKNOWN, TYPO}][:602]', '{UNKNOWN, TYPO}][:603]'),
        ('!= 602', '!= 603'),
        ('kreeg 602', 'kreeg 603'),
        ('585, 586, 587, 588, 589', '586, 587, 588, 589, 590'),
    ],
)

build(
    'create-six-hundred-seventeen-minimal.py',
    'create-six-hundred-eighteen-minimal.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('!= 602', '!= 603'),
        ('kreeg 602', 'kreeg 603'),
        ('585, 586, 587, 588, 589', '586, 587, 588, 589, 590'),
    ],
)

build(
    'make-six-hundred-seventeen.py',
    'make-six-hundred-eighteen.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('all_cases[:602]', 'all_cases[:603]'),
        ('{UNKNOWN, TYPO}][:602]', '{UNKNOWN, TYPO}][:603]'),
        ('!= 602', '!= 603'),
        ('525, 526, 527, 528, 529', '526, 527, 528, 529, 530'),
    ],
)

build(
    'create-six-hundred-seventeen-files.py',
    'create-six-hundred-eighteen-files.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('all_cases[:602]', 'all_cases[:603]'),
        ('{UNKNOWN, TYPO}][:602]', '{UNKNOWN, TYPO}][:603]'),
        ('!= 602', '!= 603'),
        ('525, 526, 527, 528, 529', '526, 527, 528, 529, 530'),
    ],
)

build(
    'create-six-hundred-seventeen.py',
    'create-six-hundred-eighteen.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('all_cases[:602]', 'all_cases[:603]'),
        ('{UNKNOWN, TYPO}][:602]', '{UNKNOWN, TYPO}][:603]'),
        ('!= 602', '!= 603'),
        ('528, 529, 530, 531, 532', '529, 530, 531, 532, 533'),
    ],
)

build(
    'generate-validate-six-hundred-seventeen.py',
    'generate-validate-six-hundred-eighteen.py',
    [
        ('six-hundred-seventeen', 'six-hundred-eighteen'),
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('all_cases[:602]', 'all_cases[:603]'),
        ('{UNKNOWN, TYPO}][:602]', '{UNKNOWN, TYPO}][:603]'),
        ('!= 602', '!= 603'),
        ('525, 526, 527, 528, 529', '526, 527, 528, 529, 530'),
    ],
)

build(
    'validate-six-hundred-seventeen-valid-list-cases.py',
    'validate-six-hundred-eighteen-valid-list-cases.py',
    [
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('587, 588, 589, 590, 591', '588, 589, 590, 591, 592'),
        ('all_cases[:602]', 'all_cases[:603]'),
        ('len(valid_cases) != 602', 'len(valid_cases) != 603'),
    ],
)

build(
    'validate-six-hundred-seventeen-valid-mixed.py',
    'validate-six-hundred-eighteen-valid-mixed.py',
    [
        ('zeshonderdzeventien', 'zeshonderdachttien'),
        ('587, 588, 589, 590, 591', '588, 589, 590, 591, 592'),
        ('][:602]', '][:603]'),
        ('len(valid_cases) != 602', 'len(valid_cases) != 603'),
        ('plain stderr noemt niet alle zeshonderdtwee geldige first-seen cases', 'plain stderr noemt niet alle zeshonderddrie geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-seventeen.py').read_text()
verify_text = verify_src.replace('six-hundred-seventeen', 'six-hundred-eighteen')
(ROOT / 'verify-six-hundred-eighteen.py').write_text(verify_text)
print('verify-six-hundred-eighteen.py')
