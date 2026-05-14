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
    'create-six-hundred-nine-assets.py',
    'create-six-hundred-ten-assets.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('[:594]', '[:595]'),
        ('!= 594', '!= 595'),
        ('kreeg 594', 'kreeg 595'),
        ('581, 582, 583, 584, 585', '582, 583, 584, 585, 586'),
    ],
)

build(
    'create-six-hundred-nine-bootstrap.py',
    'create-six-hundred-ten-bootstrap.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('all_cases[:594]', 'all_cases[:595]'),
        ('{UNKNOWN, TYPO}][:594]', '{UNKNOWN, TYPO}][:595]'),
        ('!= 594', '!= 595'),
        ('kreeg 594', 'kreeg 595'),
        ('577, 578, 579, 580, 581', '578, 579, 580, 581, 582'),
    ],
)

build(
    'create-six-hundred-nine-minimal.py',
    'create-six-hundred-ten-minimal.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('!= 594', '!= 595'),
        ('kreeg 594', 'kreeg 595'),
        ('577, 578, 579, 580, 581', '578, 579, 580, 581, 582'),
    ],
)

build(
    'make-six-hundred-nine.py',
    'make-six-hundred-ten.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('all_cases[:594]', 'all_cases[:595]'),
        ('{UNKNOWN, TYPO}][:594]', '{UNKNOWN, TYPO}][:595]'),
        ('!= 594', '!= 595'),
        ('517, 518, 519, 520, 521', '518, 519, 520, 521, 522'),
    ],
)

build(
    'create-six-hundred-nine-files.py',
    'create-six-hundred-ten-files.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('all_cases[:594]', 'all_cases[:595]'),
        ('{UNKNOWN, TYPO}][:594]', '{UNKNOWN, TYPO}][:595]'),
        ('!= 594', '!= 595'),
        ('517, 518, 519, 520, 521', '518, 519, 520, 521, 522'),
    ],
)

build(
    'create-six-hundred-nine.py',
    'create-six-hundred-ten.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('all_cases[:594]', 'all_cases[:595]'),
        ('{UNKNOWN, TYPO}][:594]', '{UNKNOWN, TYPO}][:595]'),
        ('!= 594', '!= 595'),
        ('520, 521, 522, 523, 524', '521, 522, 523, 524, 525'),
    ],
)

build(
    'generate-validate-six-hundred-nine.py',
    'generate-validate-six-hundred-ten.py',
    [
        ('six-hundred-nine', 'six-hundred-ten'),
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('all_cases[:594]', 'all_cases[:595]'),
        ('{UNKNOWN, TYPO}][:594]', '{UNKNOWN, TYPO}][:595]'),
        ('!= 594', '!= 595'),
        ('517, 518, 519, 520, 521', '518, 519, 520, 521, 522'),
    ],
)

build(
    'validate-six-hundred-nine-valid-list-cases.py',
    'validate-six-hundred-ten-valid-list-cases.py',
    [
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('579, 580, 581, 582, 583', '580, 581, 582, 583, 584'),
        ('all_cases[:594]', 'all_cases[:595]'),
        ('len(valid_cases) != 594', 'len(valid_cases) != 595'),
    ],
)

build(
    'validate-six-hundred-nine-valid-mixed.py',
    'validate-six-hundred-ten-valid-mixed.py',
    [
        ('zeshonderdnegen', 'zeshonderdtien'),
        ('579, 580, 581, 582, 583', '580, 581, 582, 583, 584'),
        ('][:594]', '][:595]'),
        ('len(valid_cases) != 594', 'len(valid_cases) != 595'),
        ('plain stderr noemt niet alle vijfhonderdvierennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvijfennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-nine.py').read_text()
verify_text = verify_src.replace('six-hundred-nine', 'six-hundred-ten')
(ROOT / 'verify-six-hundred-ten.py').write_text(verify_text)
print('verify-six-hundred-ten.py')
