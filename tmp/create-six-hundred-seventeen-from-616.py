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
    'create-six-hundred-sixteen-assets.py',
    'create-six-hundred-seventeen-assets.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('[:601]', '[:602]'),
        ('!= 601', '!= 602'),
        ('kreeg 601', 'kreeg 602'),
        ('588, 589, 590, 591, 592', '589, 590, 591, 592, 593'),
    ],
)

build(
    'create-six-hundred-sixteen-bootstrap.py',
    'create-six-hundred-seventeen-bootstrap.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('all_cases[:601]', 'all_cases[:602]'),
        ('{UNKNOWN, TYPO}][:601]', '{UNKNOWN, TYPO}][:602]'),
        ('!= 601', '!= 602'),
        ('kreeg 601', 'kreeg 602'),
        ('584, 585, 586, 587, 588', '585, 586, 587, 588, 589'),
    ],
)

build(
    'create-six-hundred-sixteen-minimal.py',
    'create-six-hundred-seventeen-minimal.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('!= 601', '!= 602'),
        ('kreeg 601', 'kreeg 602'),
        ('584, 585, 586, 587, 588', '585, 586, 587, 588, 589'),
    ],
)

build(
    'make-six-hundred-sixteen.py',
    'make-six-hundred-seventeen.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('all_cases[:601]', 'all_cases[:602]'),
        ('{UNKNOWN, TYPO}][:601]', '{UNKNOWN, TYPO}][:602]'),
        ('!= 601', '!= 602'),
        ('524, 525, 526, 527, 528', '525, 526, 527, 528, 529'),
    ],
)

build(
    'create-six-hundred-sixteen-files.py',
    'create-six-hundred-seventeen-files.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('all_cases[:601]', 'all_cases[:602]'),
        ('{UNKNOWN, TYPO}][:601]', '{UNKNOWN, TYPO}][:602]'),
        ('!= 601', '!= 602'),
        ('524, 525, 526, 527, 528', '525, 526, 527, 528, 529'),
    ],
)

build(
    'create-six-hundred-sixteen.py',
    'create-six-hundred-seventeen.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('all_cases[:601]', 'all_cases[:602]'),
        ('{UNKNOWN, TYPO}][:601]', '{UNKNOWN, TYPO}][:602]'),
        ('!= 601', '!= 602'),
        ('527, 528, 529, 530, 531', '528, 529, 530, 531, 532'),
    ],
)

build(
    'generate-validate-six-hundred-sixteen.py',
    'generate-validate-six-hundred-seventeen.py',
    [
        ('six-hundred-sixteen', 'six-hundred-seventeen'),
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('all_cases[:601]', 'all_cases[:602]'),
        ('{UNKNOWN, TYPO}][:601]', '{UNKNOWN, TYPO}][:602]'),
        ('!= 601', '!= 602'),
        ('524, 525, 526, 527, 528', '525, 526, 527, 528, 529'),
    ],
)

build(
    'validate-six-hundred-sixteen-valid-list-cases.py',
    'validate-six-hundred-seventeen-valid-list-cases.py',
    [
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('586, 587, 588, 589, 590', '587, 588, 589, 590, 591'),
        ('all_cases[:601]', 'all_cases[:602]'),
        ('len(valid_cases) != 601', 'len(valid_cases) != 602'),
    ],
)

build(
    'validate-six-hundred-sixteen-valid-mixed.py',
    'validate-six-hundred-seventeen-valid-mixed.py',
    [
        ('zeshonderdzestien', 'zeshonderdzeventien'),
        ('586, 587, 588, 589, 590', '587, 588, 589, 590, 591'),
        ('][:601]', '][:602]'),
        ('len(valid_cases) != 601', 'len(valid_cases) != 602'),
        ('plain stderr noemt niet alle zeshonderdeen geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdtwee geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-sixteen.py').read_text()
verify_text = verify_src.replace('six-hundred-sixteen', 'six-hundred-seventeen')
(ROOT / 'verify-six-hundred-seventeen.py').write_text(verify_text)
print('verify-six-hundred-seventeen.py')
