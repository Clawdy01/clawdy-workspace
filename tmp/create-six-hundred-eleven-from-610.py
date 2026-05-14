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
    'create-six-hundred-ten-assets.py',
    'create-six-hundred-eleven-assets.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('[:595]', '[:596]'),
        ('!= 595', '!= 596'),
        ('kreeg 595', 'kreeg 596'),
        ('582, 583, 584, 585, 586', '583, 584, 585, 586, 587'),
    ],
)

build(
    'create-six-hundred-ten-bootstrap.py',
    'create-six-hundred-eleven-bootstrap.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('all_cases[:595]', 'all_cases[:596]'),
        ('{UNKNOWN, TYPO}][:595]', '{UNKNOWN, TYPO}][:596]'),
        ('!= 595', '!= 596'),
        ('kreeg 595', 'kreeg 596'),
        ('578, 579, 580, 581, 582', '579, 580, 581, 582, 583'),
    ],
)

build(
    'create-six-hundred-ten-minimal.py',
    'create-six-hundred-eleven-minimal.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('!= 595', '!= 596'),
        ('kreeg 595', 'kreeg 596'),
        ('578, 579, 580, 581, 582', '579, 580, 581, 582, 583'),
    ],
)

build(
    'make-six-hundred-ten.py',
    'make-six-hundred-eleven.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('all_cases[:595]', 'all_cases[:596]'),
        ('{UNKNOWN, TYPO}][:595]', '{UNKNOWN, TYPO}][:596]'),
        ('!= 595', '!= 596'),
        ('518, 519, 520, 521, 522', '519, 520, 521, 522, 523'),
    ],
)

build(
    'create-six-hundred-ten-files.py',
    'create-six-hundred-eleven-files.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('all_cases[:595]', 'all_cases[:596]'),
        ('{UNKNOWN, TYPO}][:595]', '{UNKNOWN, TYPO}][:596]'),
        ('!= 595', '!= 596'),
        ('518, 519, 520, 521, 522', '519, 520, 521, 522, 523'),
    ],
)

build(
    'create-six-hundred-ten.py',
    'create-six-hundred-eleven.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('all_cases[:595]', 'all_cases[:596]'),
        ('{UNKNOWN, TYPO}][:595]', '{UNKNOWN, TYPO}][:596]'),
        ('!= 595', '!= 596'),
        ('521, 522, 523, 524, 525', '522, 523, 524, 525, 526'),
    ],
)

build(
    'generate-validate-six-hundred-ten.py',
    'generate-validate-six-hundred-eleven.py',
    [
        ('six-hundred-ten', 'six-hundred-eleven'),
        ('zeshonderdtien', 'zeshonderdelf'),
        ('all_cases[:595]', 'all_cases[:596]'),
        ('{UNKNOWN, TYPO}][:595]', '{UNKNOWN, TYPO}][:596]'),
        ('!= 595', '!= 596'),
        ('518, 519, 520, 521, 522', '519, 520, 521, 522, 523'),
    ],
)

build(
    'validate-six-hundred-ten-valid-list-cases.py',
    'validate-six-hundred-eleven-valid-list-cases.py',
    [
        ('zeshonderdtien', 'zeshonderdelf'),
        ('580, 581, 582, 583, 584', '581, 582, 583, 584, 585'),
        ('all_cases[:595]', 'all_cases[:596]'),
        ('len(valid_cases) != 595', 'len(valid_cases) != 596'),
    ],
)

build(
    'validate-six-hundred-ten-valid-mixed.py',
    'validate-six-hundred-eleven-valid-mixed.py',
    [
        ('zeshonderdtien', 'zeshonderdelf'),
        ('580, 581, 582, 583, 584', '581, 582, 583, 584, 585'),
        ('][:595]', '][:596]'),
        ('len(valid_cases) != 595', 'len(valid_cases) != 596'),
        ('plain stderr noemt niet alle vijfhonderdvijfennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzesennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-ten.py').read_text()
verify_text = verify_src.replace('six-hundred-ten', 'six-hundred-eleven')
(ROOT / 'verify-six-hundred-eleven.py').write_text(verify_text)
print('verify-six-hundred-eleven.py')
