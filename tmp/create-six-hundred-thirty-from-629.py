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
    'create-six-hundred-twenty-nine-assets.py',
    'create-six-hundred-thirty-assets.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('[:614]', '[:615]'),
        ('!= 614', '!= 615'),
        ('kreeg 614', 'kreeg 615'),
        ('601, 602, 603, 604, 605', '602, 603, 604, 605, 606'),
    ],
)

build(
    'create-six-hundred-twenty-nine-bootstrap.py',
    'create-six-hundred-thirty-bootstrap.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('all_cases[:614]', 'all_cases[:615]'),
        ('{UNKNOWN, TYPO}][:614]', '{UNKNOWN, TYPO}][:615]'),
        ('!= 614', '!= 615'),
        ('kreeg 614', 'kreeg 615'),
        ('597, 598, 599, 600, 601', '598, 599, 600, 601, 602'),
    ],
)

build(
    'create-six-hundred-twenty-nine-minimal.py',
    'create-six-hundred-thirty-minimal.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('!= 614', '!= 615'),
        ('kreeg 614', 'kreeg 615'),
        ('597, 598, 599, 600, 601', '598, 599, 600, 601, 602'),
    ],
)

build(
    'make-six-hundred-twenty-nine.py',
    'make-six-hundred-thirty.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('all_cases[:614]', 'all_cases[:615]'),
        ('{UNKNOWN, TYPO}][:614]', '{UNKNOWN, TYPO}][:615]'),
        ('!= 614', '!= 615'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'create-six-hundred-twenty-nine-files.py',
    'create-six-hundred-thirty-files.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('all_cases[:614]', 'all_cases[:615]'),
        ('{UNKNOWN, TYPO}][:614]', '{UNKNOWN, TYPO}][:615]'),
        ('!= 614', '!= 615'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'create-six-hundred-twenty-nine.py',
    'create-six-hundred-thirty.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('all_cases[:614]', 'all_cases[:615]'),
        ('{UNKNOWN, TYPO}][:614]', '{UNKNOWN, TYPO}][:615]'),
        ('!= 614', '!= 615'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-nine.py',
    'generate-validate-six-hundred-thirty.py',
    [
        ('six-hundred-twenty-nine', 'six-hundred-thirty'),
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('all_cases[:614]', 'all_cases[:615]'),
        ('{UNKNOWN, TYPO}][:614]', '{UNKNOWN, TYPO}][:615]'),
        ('!= 614', '!= 615'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'validate-six-hundred-twenty-nine-valid-list-cases.py',
    'validate-six-hundred-thirty-valid-list-cases.py',
    [
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('599, 600, 601, 602, 603', '600, 601, 602, 603, 604'),
        ('all_cases[:614]', 'all_cases[:615]'),
        ('len(valid_cases) != 614', 'len(valid_cases) != 615'),
    ],
)

build(
    'validate-six-hundred-twenty-nine-valid-mixed.py',
    'validate-six-hundred-thirty-valid-mixed.py',
    [
        ('zeshonderdnegenentwintig', 'zeshonderddertig'),
        ('599, 600, 601, 602, 603', '600, 601, 602, 603, 604'),
        ('][:614]', '][:615]'),
        ('len(valid_cases) != 614', 'len(valid_cases) != 615'),
        ('plain stderr noemt niet alle zeshonderdveertien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvijftien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-nine.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-nine', 'six-hundred-thirty')
(ROOT / 'verify-six-hundred-thirty.py').write_text(verify_text)
print('verify-six-hundred-thirty.py')
