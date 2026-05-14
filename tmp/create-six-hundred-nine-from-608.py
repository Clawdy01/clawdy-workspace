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
    'create-six-hundred-eight-assets.py',
    'create-six-hundred-nine-assets.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('[:593]', '[:594]'),
        ('!= 593', '!= 594'),
        ('kreeg 593', 'kreeg 594'),
        ('580, 581, 582, 583, 584', '581, 582, 583, 584, 585'),
    ],
)

build(
    'create-six-hundred-eight-bootstrap.py',
    'create-six-hundred-nine-bootstrap.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('all_cases[:593]', 'all_cases[:594]'),
        ('{UNKNOWN, TYPO}][:593]', '{UNKNOWN, TYPO}][:594]'),
        ('!= 593', '!= 594'),
        ('kreeg 593', 'kreeg 594'),
        ('576, 577, 578, 579, 580', '577, 578, 579, 580, 581'),
    ],
)

build(
    'create-six-hundred-eight-minimal.py',
    'create-six-hundred-nine-minimal.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('!= 593', '!= 594'),
        ('kreeg 593', 'kreeg 594'),
        ('576, 577, 578, 579, 580', '577, 578, 579, 580, 581'),
    ],
)

build(
    'make-six-hundred-eight.py',
    'make-six-hundred-nine.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('all_cases[:593]', 'all_cases[:594]'),
        ('{UNKNOWN, TYPO}][:593]', '{UNKNOWN, TYPO}][:594]'),
        ('!= 593', '!= 594'),
        ('516, 517, 518, 519, 520', '517, 518, 519, 520, 521'),
    ],
)

build(
    'create-six-hundred-eight-files.py',
    'create-six-hundred-nine-files.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('all_cases[:593]', 'all_cases[:594]'),
        ('{UNKNOWN, TYPO}][:593]', '{UNKNOWN, TYPO}][:594]'),
        ('!= 593', '!= 594'),
        ('516, 517, 518, 519, 520', '517, 518, 519, 520, 521'),
    ],
)

build(
    'create-six-hundred-eight.py',
    'create-six-hundred-nine.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('all_cases[:593]', 'all_cases[:594]'),
        ('{UNKNOWN, TYPO}][:593]', '{UNKNOWN, TYPO}][:594]'),
        ('!= 593', '!= 594'),
        ('519, 520, 521, 522, 523', '520, 521, 522, 523, 524'),
    ],
)

build(
    'generate-validate-six-hundred-eight.py',
    'generate-validate-six-hundred-nine.py',
    [
        ('six-hundred-eight', 'six-hundred-nine'),
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('all_cases[:593]', 'all_cases[:594]'),
        ('{UNKNOWN, TYPO}][:593]', '{UNKNOWN, TYPO}][:594]'),
        ('!= 593', '!= 594'),
        ('516, 517, 518, 519, 520', '517, 518, 519, 520, 521'),
    ],
)

build(
    'validate-six-hundred-eight-valid-list-cases.py',
    'validate-six-hundred-nine-valid-list-cases.py',
    [
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('578, 579, 580, 581, 582', '579, 580, 581, 582, 583'),
        ('all_cases[:593]', 'all_cases[:594]'),
        ('len(valid_cases) != 593', 'len(valid_cases) != 594'),
    ],
)

build(
    'validate-six-hundred-eight-valid-mixed.py',
    'validate-six-hundred-nine-valid-mixed.py',
    [
        ('zeshonderdacht', 'zeshonderdnegen'),
        ('578, 579, 580, 581, 582', '579, 580, 581, 582, 583'),
        ('][:593]', '][:594]'),
        ('len(valid_cases) != 593', 'len(valid_cases) != 594'),
        ('plain stderr noemt niet alle vijfhonderddrieënnegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvierennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-eight.py').read_text()
verify_text = verify_src.replace('six-hundred-eight', 'six-hundred-nine')
(ROOT / 'verify-six-hundred-nine.py').write_text(verify_text)
print('verify-six-hundred-nine.py')
