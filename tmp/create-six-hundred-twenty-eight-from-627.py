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
    'create-six-hundred-twenty-seven-assets.py',
    'create-six-hundred-twenty-eight-assets.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('[:612]', '[:613]'),
        ('!= 612', '!= 613'),
        ('kreeg 612', 'kreeg 613'),
        ('599, 600, 601, 602, 603', '600, 601, 602, 603, 604'),
    ],
)

build(
    'create-six-hundred-twenty-seven-bootstrap.py',
    'create-six-hundred-twenty-eight-bootstrap.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('all_cases[:612]', 'all_cases[:613]'),
        ('{UNKNOWN, TYPO}][:612]', '{UNKNOWN, TYPO}][:613]'),
        ('!= 612', '!= 613'),
        ('kreeg 612', 'kreeg 613'),
        ('595, 596, 597, 598, 599', '596, 597, 598, 599, 600'),
    ],
)

build(
    'create-six-hundred-twenty-seven-minimal.py',
    'create-six-hundred-twenty-eight-minimal.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('!= 612', '!= 613'),
        ('kreeg 612', 'kreeg 613'),
        ('595, 596, 597, 598, 599', '596, 597, 598, 599, 600'),
    ],
)

build(
    'make-six-hundred-twenty-seven.py',
    'make-six-hundred-twenty-eight.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('all_cases[:612]', 'all_cases[:613]'),
        ('{UNKNOWN, TYPO}][:612]', '{UNKNOWN, TYPO}][:613]'),
        ('!= 612', '!= 613'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'create-six-hundred-twenty-seven-files.py',
    'create-six-hundred-twenty-eight-files.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('all_cases[:612]', 'all_cases[:613]'),
        ('{UNKNOWN, TYPO}][:612]', '{UNKNOWN, TYPO}][:613]'),
        ('!= 612', '!= 613'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'create-six-hundred-twenty-seven.py',
    'create-six-hundred-twenty-eight.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('all_cases[:612]', 'all_cases[:613]'),
        ('{UNKNOWN, TYPO}][:612]', '{UNKNOWN, TYPO}][:613]'),
        ('!= 612', '!= 613'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-seven.py',
    'generate-validate-six-hundred-twenty-eight.py',
    [
        ('six-hundred-twenty-seven', 'six-hundred-twenty-eight'),
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('all_cases[:612]', 'all_cases[:613]'),
        ('{UNKNOWN, TYPO}][:612]', '{UNKNOWN, TYPO}][:613]'),
        ('!= 612', '!= 613'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'validate-six-hundred-twenty-seven-valid-list-cases.py',
    'validate-six-hundred-twenty-eight-valid-list-cases.py',
    [
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('597, 598, 599, 600, 601', '598, 599, 600, 601, 602'),
        ('all_cases[:612]', 'all_cases[:613]'),
        ('len(valid_cases) != 612', 'len(valid_cases) != 613'),
    ],
)

build(
    'validate-six-hundred-twenty-seven-valid-mixed.py',
    'validate-six-hundred-twenty-eight-valid-mixed.py',
    [
        ('zeshonderdzevenentwintig', 'zeshonderdachtentwintig'),
        ('597, 598, 599, 600, 601', '598, 599, 600, 601, 602'),
        ('][:612]', '][:613]'),
        ('len(valid_cases) != 612', 'len(valid_cases) != 613'),
        ('plain stderr noemt niet alle zeshonderdtwaalf geldige first-seen cases', 'plain stderr noemt niet alle zeshonderddertien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-seven.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-seven', 'six-hundred-twenty-eight')
(ROOT / 'verify-six-hundred-twenty-eight.py').write_text(verify_text)
print('verify-six-hundred-twenty-eight.py')
