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
    'create-five-hundred-twenty-assets.py',
    'create-five-hundred-twenty-one-assets.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('[:505]', '[:506]'),
        ('!= 505', '!= 506'),
        ('kreeg 505', 'kreeg 506'),
        ('488, 489, 490, 491, 492, 493, 494, 495, 496]', '488, 489, 490, 491, 492, 493, 494, 495, 496, 497]'),
    ],
)

build(
    'create-five-hundred-twenty-bootstrap.py',
    'create-five-hundred-twenty-one-bootstrap.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('all_cases[:505]', 'all_cases[:506]'),
        ('{UNKNOWN, TYPO}][:505]', '{UNKNOWN, TYPO}][:506]'),
        ('!= 505', '!= 506'),
        ('kreeg 505', 'kreeg 506'),
        ('484, 485, 486, 487, 488, 489, 490, 491, 492]', '484, 485, 486, 487, 488, 489, 490, 491, 492, 493]'),
    ],
)

build(
    'create-five-hundred-twenty-minimal.py',
    'create-five-hundred-twenty-one-minimal.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('!= 505', '!= 506'),
        ('kreeg 505', 'kreeg 506'),
        (' 446)', ' 447)'),
        ('484, 485, 486, 487, 488, 489, 490, 491, 492]', '484, 485, 486, 487, 488, 489, 490, 491, 492, 493]'),
    ],
)

build(
    'make-five-hundred-twenty.py',
    'make-five-hundred-twenty-one.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('all_cases[:505]', 'all_cases[:506]'),
        ('{UNKNOWN, TYPO}][:505]', '{UNKNOWN, TYPO}][:506]'),
        ('!= 505', '!= 506'),
        ('424, 425, 426, 427, 428, 429, 430, 431, 432]', '424, 425, 426, 427, 428, 429, 430, 431, 432, 433]'),
    ],
)

build(
    'create-five-hundred-twenty-files.py',
    'create-five-hundred-twenty-one-files.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('all_cases[:505]', 'all_cases[:506]'),
        ('{UNKNOWN, TYPO}][:505]', '{UNKNOWN, TYPO}][:506]'),
        ('!= 505', '!= 506'),
        ('424, 425, 426, 427, 428, 429, 430, 431, 432]', '424, 425, 426, 427, 428, 429, 430, 431, 432, 433]'),
    ],
)

build(
    'create-five-hundred-twenty.py',
    'create-five-hundred-twenty-one.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('all_cases[:505]', 'all_cases[:506]'),
        ('{UNKNOWN, TYPO}][:505]', '{UNKNOWN, TYPO}][:506]'),
        ('!= 505', '!= 506'),
        ('428, 429, 430, 431, 432, 433, 434, 435]', '428, 429, 430, 431, 432, 433, 434, 435, 436]'),
    ],
)

build(
    'generate-validate-five-hundred-twenty.py',
    'generate-validate-five-hundred-twenty-one.py',
    [
        ('five-hundred-twenty', 'five-hundred-twenty-one'),
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('all_cases[:505]', 'all_cases[:506]'),
        ('{UNKNOWN, TYPO}][:505]', '{UNKNOWN, TYPO}][:506]'),
        ('!= 505', '!= 506'),
        ('424, 425, 426, 427, 428, 429, 430, 431, 432]', '424, 425, 426, 427, 428, 429, 430, 431, 432, 433]'),
    ],
)

build(
    'validate-five-hundred-twenty-valid-list-cases.py',
    'validate-five-hundred-twenty-one-valid-list-cases.py',
    [
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('486, 487, 488, 489, 490, 491, 492, 493, 494]', '486, 487, 488, 489, 490, 491, 492, 493, 494, 495]'),
        ('all_cases[:505]', 'all_cases[:506]'),
        ('len(valid_cases) != 505', 'len(valid_cases) != 506'),
    ],
)

build(
    'validate-five-hundred-twenty-valid-mixed.py',
    'validate-five-hundred-twenty-one-valid-mixed.py',
    [
        ('vijfhonderdtwintig', 'vijfhonderdeenentwintig'),
        ('486, 487, 488, 489, 490, 491, 492, 493, 494]', '486, 487, 488, 489, 490, 491, 492, 493, 494, 495]'),
        ('][:505]', '][:506]'),
        ('len(valid_cases) != 505', 'len(valid_cases) != 506'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty', 'five-hundred-twenty-one')
(ROOT / 'verify-five-hundred-twenty-one.py').write_text(verify_text)
print('verify-five-hundred-twenty-one.py')
