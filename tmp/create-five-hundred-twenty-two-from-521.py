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
    'create-five-hundred-twenty-one-assets.py',
    'create-five-hundred-twenty-two-assets.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('[:506]', '[:507]'),
        ('!= 506', '!= 507'),
        ('kreeg 506', 'kreeg 507'),
        ('488, 489, 490, 491, 492, 493, 494, 495, 496, 497]', '488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498]'),
    ],
)

build(
    'create-five-hundred-twenty-one-bootstrap.py',
    'create-five-hundred-twenty-two-bootstrap.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('all_cases[:506]', 'all_cases[:507]'),
        ('{UNKNOWN, TYPO}][:506]', '{UNKNOWN, TYPO}][:507]'),
        ('!= 506', '!= 507'),
        ('kreeg 506', 'kreeg 507'),
        ('484, 485, 486, 487, 488, 489, 490, 491, 492, 493]', '484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494]'),
    ],
)

build(
    'create-five-hundred-twenty-one-minimal.py',
    'create-five-hundred-twenty-two-minimal.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('!= 506', '!= 507'),
        ('kreeg 506', 'kreeg 507'),
        (' 447)', ' 448)'),
        ('484, 485, 486, 487, 488, 489, 490, 491, 492, 493]', '484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494]'),
    ],
)

build(
    'make-five-hundred-twenty-one.py',
    'make-five-hundred-twenty-two.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('all_cases[:506]', 'all_cases[:507]'),
        ('{UNKNOWN, TYPO}][:506]', '{UNKNOWN, TYPO}][:507]'),
        ('!= 506', '!= 507'),
        ('424, 425, 426, 427, 428, 429, 430, 431, 432, 433]', '424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434]'),
    ],
)

build(
    'create-five-hundred-twenty-one-files.py',
    'create-five-hundred-twenty-two-files.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('all_cases[:506]', 'all_cases[:507]'),
        ('{UNKNOWN, TYPO}][:506]', '{UNKNOWN, TYPO}][:507]'),
        ('!= 506', '!= 507'),
        ('424, 425, 426, 427, 428, 429, 430, 431, 432, 433]', '424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434]'),
    ],
)

build(
    'create-five-hundred-twenty-one.py',
    'create-five-hundred-twenty-two.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('all_cases[:506]', 'all_cases[:507]'),
        ('{UNKNOWN, TYPO}][:506]', '{UNKNOWN, TYPO}][:507]'),
        ('!= 506', '!= 507'),
        ('428, 429, 430, 431, 432, 433, 434, 435, 436]', '428, 429, 430, 431, 432, 433, 434, 435, 436, 437]'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-one.py',
    'generate-validate-five-hundred-twenty-two.py',
    [
        ('five-hundred-twenty-one', 'five-hundred-twenty-two'),
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('all_cases[:506]', 'all_cases[:507]'),
        ('{UNKNOWN, TYPO}][:506]', '{UNKNOWN, TYPO}][:507]'),
        ('!= 506', '!= 507'),
        ('424, 425, 426, 427, 428, 429, 430, 431, 432, 433]', '424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434]'),
    ],
)

build(
    'validate-five-hundred-twenty-one-valid-list-cases.py',
    'validate-five-hundred-twenty-two-valid-list-cases.py',
    [
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('486, 487, 488, 489, 490, 491, 492, 493, 494, 495]', '486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496]'),
        ('all_cases[:506]', 'all_cases[:507]'),
        ('len(valid_cases) != 506', 'len(valid_cases) != 507'),
    ],
)

build(
    'validate-five-hundred-twenty-one-valid-mixed.py',
    'validate-five-hundred-twenty-two-valid-mixed.py',
    [
        ('vijfhonderdeenentwintig', 'vijfhonderdtweeëntwintig'),
        ('486, 487, 488, 489, 490, 491, 492, 493, 494, 495]', '486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496]'),
        ('][:506]', '][:507]'),
        ('len(valid_cases) != 506', 'len(valid_cases) != 507'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-one.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-one', 'five-hundred-twenty-two')
(ROOT / 'verify-five-hundred-twenty-two.py').write_text(verify_text)
print('verify-five-hundred-twenty-two.py')
