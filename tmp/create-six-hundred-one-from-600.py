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
    'create-six-hundred-assets.py',
    'create-six-hundred-one-assets.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('[:585]', '[:586]'),
        ('!= 585', '!= 586'),
        ('kreeg 585', 'kreeg 586'),
        ('572, 573, 574, 575, 576', '573, 574, 575, 576, 577'),
    ],
)

build(
    'create-six-hundred-bootstrap.py',
    'create-six-hundred-one-bootstrap.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('all_cases[:585]', 'all_cases[:586]'),
        ('{UNKNOWN, TYPO}][:585]', '{UNKNOWN, TYPO}][:586]'),
        ('!= 585', '!= 586'),
        ('kreeg 585', 'kreeg 586'),
        ('568, 569, 570, 571, 572', '569, 570, 571, 572, 573'),
    ],
)

build(
    'create-six-hundred-minimal.py',
    'create-six-hundred-one-minimal.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('!= 585', '!= 586'),
        ('kreeg 585', 'kreeg 586'),
        ('568, 569, 570, 571, 572', '569, 570, 571, 572, 573'),
    ],
)

build(
    'make-six-hundred.py',
    'make-six-hundred-one.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('all_cases[:585]', 'all_cases[:586]'),
        ('{UNKNOWN, TYPO}][:585]', '{UNKNOWN, TYPO}][:586]'),
        ('!= 585', '!= 586'),
        ('508, 509, 510, 511, 512', '509, 510, 511, 512, 513'),
    ],
)

build(
    'create-six-hundred-files.py',
    'create-six-hundred-one-files.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('all_cases[:585]', 'all_cases[:586]'),
        ('{UNKNOWN, TYPO}][:585]', '{UNKNOWN, TYPO}][:586]'),
        ('!= 585', '!= 586'),
        ('508, 509, 510, 511, 512', '509, 510, 511, 512, 513'),
    ],
)

build(
    'create-six-hundred.py',
    'create-six-hundred-one.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('all_cases[:585]', 'all_cases[:586]'),
        ('{UNKNOWN, TYPO}][:585]', '{UNKNOWN, TYPO}][:586]'),
        ('!= 585', '!= 586'),
        ('511, 512, 513, 514, 515', '512, 513, 514, 515, 516'),
    ],
)

build(
    'generate-validate-six-hundred.py',
    'generate-validate-six-hundred-one.py',
    [
        ('six-hundred', 'six-hundred-one'),
        ('zeshonderd', 'zeshonderdeen'),
        ('all_cases[:585]', 'all_cases[:586]'),
        ('{UNKNOWN, TYPO}][:585]', '{UNKNOWN, TYPO}][:586]'),
        ('!= 585', '!= 586'),
        ('508, 509, 510, 511, 512', '509, 510, 511, 512, 513'),
    ],
)

build(
    'validate-six-hundred-valid-list-cases.py',
    'validate-six-hundred-one-valid-list-cases.py',
    [
        ('zeshonderd', 'zeshonderdeen'),
        ('570, 571, 572, 573, 574', '571, 572, 573, 574, 575'),
        ('all_cases[:585]', 'all_cases[:586]'),
        ('len(valid_cases) != 585', 'len(valid_cases) != 586'),
    ],
)

build(
    'validate-six-hundred-valid-mixed.py',
    'validate-six-hundred-one-valid-mixed.py',
    [
        ('zeshonderd', 'zeshonderdeen'),
        ('570, 571, 572, 573, 574', '571, 572, 573, 574, 575'),
        ('][:585]', '][:586]'),
        ('len(valid_cases) != 585', 'len(valid_cases) != 586'),
        ('plain stderr noemt niet alle vijfhonderdvijfentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzesentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred.py').read_text()
verify_text = verify_src.replace('six-hundred', 'six-hundred-one')
(ROOT / 'verify-six-hundred-one.py').write_text(verify_text)
print('verify-six-hundred-one.py')
