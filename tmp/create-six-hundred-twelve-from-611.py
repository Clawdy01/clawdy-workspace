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
    'create-six-hundred-eleven-assets.py',
    'create-six-hundred-twelve-assets.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('[:596]', '[:597]'),
        ('!= 596', '!= 597'),
        ('kreeg 596', 'kreeg 597'),
        ('583, 584, 585, 586, 587', '584, 585, 586, 587, 588'),
    ],
)

build(
    'create-six-hundred-eleven-bootstrap.py',
    'create-six-hundred-twelve-bootstrap.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('all_cases[:596]', 'all_cases[:597]'),
        ('{UNKNOWN, TYPO}][:596]', '{UNKNOWN, TYPO}][:597]'),
        ('!= 596', '!= 597'),
        ('kreeg 596', 'kreeg 597'),
        ('579, 580, 581, 582, 583', '580, 581, 582, 583, 584'),
    ],
)

build(
    'create-six-hundred-eleven-minimal.py',
    'create-six-hundred-twelve-minimal.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('!= 596', '!= 597'),
        ('kreeg 596', 'kreeg 597'),
        ('579, 580, 581, 582, 583', '580, 581, 582, 583, 584'),
    ],
)

build(
    'make-six-hundred-eleven.py',
    'make-six-hundred-twelve.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('all_cases[:596]', 'all_cases[:597]'),
        ('{UNKNOWN, TYPO}][:596]', '{UNKNOWN, TYPO}][:597]'),
        ('!= 596', '!= 597'),
        ('519, 520, 521, 522, 523', '520, 521, 522, 523, 524'),
    ],
)

build(
    'create-six-hundred-eleven-files.py',
    'create-six-hundred-twelve-files.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('all_cases[:596]', 'all_cases[:597]'),
        ('{UNKNOWN, TYPO}][:596]', '{UNKNOWN, TYPO}][:597]'),
        ('!= 596', '!= 597'),
        ('519, 520, 521, 522, 523', '520, 521, 522, 523, 524'),
    ],
)

build(
    'create-six-hundred-eleven.py',
    'create-six-hundred-twelve.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('all_cases[:596]', 'all_cases[:597]'),
        ('{UNKNOWN, TYPO}][:596]', '{UNKNOWN, TYPO}][:597]'),
        ('!= 596', '!= 597'),
        ('522, 523, 524, 525, 526', '523, 524, 525, 526, 527'),
    ],
)

build(
    'generate-validate-six-hundred-eleven.py',
    'generate-validate-six-hundred-twelve.py',
    [
        ('six-hundred-eleven', 'six-hundred-twelve'),
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('all_cases[:596]', 'all_cases[:597]'),
        ('{UNKNOWN, TYPO}][:596]', '{UNKNOWN, TYPO}][:597]'),
        ('!= 596', '!= 597'),
        ('519, 520, 521, 522, 523', '520, 521, 522, 523, 524'),
    ],
)

build(
    'validate-six-hundred-eleven-valid-list-cases.py',
    'validate-six-hundred-twelve-valid-list-cases.py',
    [
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('581, 582, 583, 584, 585', '582, 583, 584, 585, 586'),
        ('all_cases[:596]', 'all_cases[:597]'),
        ('len(valid_cases) != 596', 'len(valid_cases) != 597'),
    ],
)

build(
    'validate-six-hundred-eleven-valid-mixed.py',
    'validate-six-hundred-twelve-valid-mixed.py',
    [
        ('zeshonderdelf', 'zeshonderdtwaalf'),
        ('581, 582, 583, 584, 585', '582, 583, 584, 585, 586'),
        ('][:596]', '][:597]'),
        ('len(valid_cases) != 596', 'len(valid_cases) != 597'),
        ('plain stderr noemt niet alle vijfhonderdzesennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzevenennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-eleven.py').read_text()
verify_text = verify_src.replace('six-hundred-eleven', 'six-hundred-twelve')
(ROOT / 'verify-six-hundred-twelve.py').write_text(verify_text)
print('verify-six-hundred-twelve.py')
