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
    'create-six-hundred-fifteen-assets.py',
    'create-six-hundred-sixteen-assets.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('[:600]', '[:601]'),
        ('!= 600', '!= 601'),
        ('kreeg 600', 'kreeg 601'),
        ('587, 588, 589, 590, 591', '588, 589, 590, 591, 592'),
    ],
)

build(
    'create-six-hundred-fifteen-bootstrap.py',
    'create-six-hundred-sixteen-bootstrap.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('all_cases[:600]', 'all_cases[:601]'),
        ('{UNKNOWN, TYPO}][:600]', '{UNKNOWN, TYPO}][:601]'),
        ('!= 600', '!= 601'),
        ('kreeg 600', 'kreeg 601'),
        ('583, 584, 585, 586, 587', '584, 585, 586, 587, 588'),
    ],
)

build(
    'create-six-hundred-fifteen-minimal.py',
    'create-six-hundred-sixteen-minimal.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('!= 600', '!= 601'),
        ('kreeg 600', 'kreeg 601'),
        ('583, 584, 585, 586, 587', '584, 585, 586, 587, 588'),
    ],
)

build(
    'make-six-hundred-fifteen.py',
    'make-six-hundred-sixteen.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('all_cases[:600]', 'all_cases[:601]'),
        ('{UNKNOWN, TYPO}][:600]', '{UNKNOWN, TYPO}][:601]'),
        ('!= 600', '!= 601'),
        ('523, 524, 525, 526, 527', '524, 525, 526, 527, 528'),
    ],
)

build(
    'create-six-hundred-fifteen-files.py',
    'create-six-hundred-sixteen-files.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('all_cases[:600]', 'all_cases[:601]'),
        ('{UNKNOWN, TYPO}][:600]', '{UNKNOWN, TYPO}][:601]'),
        ('!= 600', '!= 601'),
        ('523, 524, 525, 526, 527', '524, 525, 526, 527, 528'),
    ],
)

build(
    'create-six-hundred-fifteen.py',
    'create-six-hundred-sixteen.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('all_cases[:600]', 'all_cases[:601]'),
        ('{UNKNOWN, TYPO}][:600]', '{UNKNOWN, TYPO}][:601]'),
        ('!= 600', '!= 601'),
        ('526, 527, 528, 529, 530', '527, 528, 529, 530, 531'),
    ],
)

build(
    'generate-validate-six-hundred-fifteen.py',
    'generate-validate-six-hundred-sixteen.py',
    [
        ('six-hundred-fifteen', 'six-hundred-sixteen'),
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('all_cases[:600]', 'all_cases[:601]'),
        ('{UNKNOWN, TYPO}][:600]', '{UNKNOWN, TYPO}][:601]'),
        ('!= 600', '!= 601'),
        ('523, 524, 525, 526, 527', '524, 525, 526, 527, 528'),
    ],
)

build(
    'validate-six-hundred-fifteen-valid-list-cases.py',
    'validate-six-hundred-sixteen-valid-list-cases.py',
    [
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('585, 586, 587, 588, 589', '586, 587, 588, 589, 590'),
        ('all_cases[:600]', 'all_cases[:601]'),
        ('len(valid_cases) != 600', 'len(valid_cases) != 601'),
    ],
)

build(
    'validate-six-hundred-fifteen-valid-mixed.py',
    'validate-six-hundred-sixteen-valid-mixed.py',
    [
        ('zeshonderdvijftien', 'zeshonderdzestien'),
        ('585, 586, 587, 588, 589', '586, 587, 588, 589, 590'),
        ('][:600]', '][:601]'),
        ('len(valid_cases) != 600', 'len(valid_cases) != 601'),
        ('plain stderr noemt niet alle zeshonderd geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdeen geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-fifteen.py').read_text()
verify_text = verify_src.replace('six-hundred-fifteen', 'six-hundred-sixteen')
(ROOT / 'verify-six-hundred-sixteen.py').write_text(verify_text)
print('verify-six-hundred-sixteen.py')
