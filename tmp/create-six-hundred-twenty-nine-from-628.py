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
    'create-six-hundred-twenty-eight-assets.py',
    'create-six-hundred-twenty-nine-assets.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('[:613]', '[:614]'),
        ('!= 613', '!= 614'),
        ('kreeg 613', 'kreeg 614'),
        ('600, 601, 602, 603, 604', '601, 602, 603, 604, 605'),
    ],
)

build(
    'create-six-hundred-twenty-eight-bootstrap.py',
    'create-six-hundred-twenty-nine-bootstrap.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('all_cases[:613]', 'all_cases[:614]'),
        ('{UNKNOWN, TYPO}][:613]', '{UNKNOWN, TYPO}][:614]'),
        ('!= 613', '!= 614'),
        ('kreeg 613', 'kreeg 614'),
        ('596, 597, 598, 599, 600', '597, 598, 599, 600, 601'),
    ],
)

build(
    'create-six-hundred-twenty-eight-minimal.py',
    'create-six-hundred-twenty-nine-minimal.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('!= 613', '!= 614'),
        ('kreeg 613', 'kreeg 614'),
        ('596, 597, 598, 599, 600', '597, 598, 599, 600, 601'),
    ],
)

build(
    'make-six-hundred-twenty-eight.py',
    'make-six-hundred-twenty-nine.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('all_cases[:613]', 'all_cases[:614]'),
        ('{UNKNOWN, TYPO}][:613]', '{UNKNOWN, TYPO}][:614]'),
        ('!= 613', '!= 614'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'create-six-hundred-twenty-eight-files.py',
    'create-six-hundred-twenty-nine-files.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('all_cases[:613]', 'all_cases[:614]'),
        ('{UNKNOWN, TYPO}][:613]', '{UNKNOWN, TYPO}][:614]'),
        ('!= 613', '!= 614'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'create-six-hundred-twenty-eight.py',
    'create-six-hundred-twenty-nine.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('all_cases[:613]', 'all_cases[:614]'),
        ('{UNKNOWN, TYPO}][:613]', '{UNKNOWN, TYPO}][:614]'),
        ('!= 613', '!= 614'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-eight.py',
    'generate-validate-six-hundred-twenty-nine.py',
    [
        ('six-hundred-twenty-eight', 'six-hundred-twenty-nine'),
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('all_cases[:613]', 'all_cases[:614]'),
        ('{UNKNOWN, TYPO}][:613]', '{UNKNOWN, TYPO}][:614]'),
        ('!= 613', '!= 614'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'validate-six-hundred-twenty-eight-valid-list-cases.py',
    'validate-six-hundred-twenty-nine-valid-list-cases.py',
    [
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('598, 599, 600, 601, 602', '599, 600, 601, 602, 603'),
        ('all_cases[:613]', 'all_cases[:614]'),
        ('len(valid_cases) != 613', 'len(valid_cases) != 614'),
    ],
)

build(
    'validate-six-hundred-twenty-eight-valid-mixed.py',
    'validate-six-hundred-twenty-nine-valid-mixed.py',
    [
        ('zeshonderdachtentwintig', 'zeshonderdnegenentwintig'),
        ('598, 599, 600, 601, 602', '599, 600, 601, 602, 603'),
        ('][:613]', '][:614]'),
        ('len(valid_cases) != 613', 'len(valid_cases) != 614'),
        ('plain stderr noemt niet alle zeshonderddertien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdveertien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-eight.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-eight', 'six-hundred-twenty-nine')
(ROOT / 'verify-six-hundred-twenty-nine.py').write_text(verify_text)
print('verify-six-hundred-twenty-nine.py')
