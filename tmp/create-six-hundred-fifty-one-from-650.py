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
    'create-six-hundred-fifty-assets.py',
    'create-six-hundred-fifty-one-assets.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('[:635]', '[:636]'),
        ('!= 635', '!= 636'),
        ('kreeg 635', 'kreeg 636'),
        ('622, 623, 624, 625, 626', '623, 624, 625, 626, 627'),
    ],
)

build(
    'create-six-hundred-fifty-bootstrap.py',
    'create-six-hundred-fifty-one-bootstrap.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('all_cases[:635]', 'all_cases[:636]'),
        ('{UNKNOWN, TYPO}][:635]', '{UNKNOWN, TYPO}][:636]'),
        ('!= 635', '!= 636'),
        ('kreeg 635', 'kreeg 636'),
        ('618, 619, 620, 621, 622', '619, 620, 621, 622, 623'),
    ],
)

build(
    'create-six-hundred-fifty-minimal.py',
    'create-six-hundred-fifty-one-minimal.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('!= 635', '!= 636'),
        ('kreeg 635', 'kreeg 636'),
        ('618, 619, 620, 621, 622', '619, 620, 621, 622, 623'),
    ],
)

build(
    'make-six-hundred-fifty.py',
    'make-six-hundred-fifty-one.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('all_cases[:635]', 'all_cases[:636]'),
        ('{UNKNOWN, TYPO}][:635]', '{UNKNOWN, TYPO}][:636]'),
        ('!= 635', '!= 636'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'create-six-hundred-fifty-files.py',
    'create-six-hundred-fifty-one-files.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('all_cases[:635]', 'all_cases[:636]'),
        ('{UNKNOWN, TYPO}][:635]', '{UNKNOWN, TYPO}][:636]'),
        ('!= 635', '!= 636'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'create-six-hundred-fifty.py',
    'create-six-hundred-fifty-one.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('all_cases[:635]', 'all_cases[:636]'),
        ('{UNKNOWN, TYPO}][:635]', '{UNKNOWN, TYPO}][:636]'),
        ('!= 635', '!= 636'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'generate-validate-six-hundred-fifty.py',
    'generate-validate-six-hundred-fifty-one.py',
    [
        ('six-hundred-fifty', 'six-hundred-fifty-one'),
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('all_cases[:635]', 'all_cases[:636]'),
        ('{UNKNOWN, TYPO}][:635]', '{UNKNOWN, TYPO}][:636]'),
        ('!= 635', '!= 636'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'validate-six-hundred-fifty-valid-list-cases.py',
    'validate-six-hundred-fifty-one-valid-list-cases.py',
    [
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('620, 621, 622, 623, 624', '621, 622, 623, 624, 625'),
        ('all_cases[:635]', 'all_cases[:636]'),
        ('len(valid_cases) != 635', 'len(valid_cases) != 636'),
    ],
)

build(
    'validate-six-hundred-fifty-valid-mixed.py',
    'validate-six-hundred-fifty-one-valid-mixed.py',
    [
        ('zeshonderdvijftig', 'zeshonderdeenenvijftig'),
        ('620, 621, 622, 623, 624', '621, 622, 623, 624, 625'),
        ('][:635]', '][:636]'),
        ('len(valid_cases) != 635', 'len(valid_cases) != 636'),
        ('plain stderr noemt niet alle zeshonderdvijfendertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdzesendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-fifty.py').read_text()
verify_text = verify_src.replace('six-hundred-fifty', 'six-hundred-fifty-one')
(ROOT / 'verify-six-hundred-fifty-one.py').write_text(verify_text)
print('verify-six-hundred-fifty-one.py')
