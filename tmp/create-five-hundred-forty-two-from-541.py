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
    'create-five-hundred-forty-one-assets.py',
    'create-five-hundred-forty-two-assets.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('[:526]', '[:527]'),
        ('!= 526', '!= 527'),
        ('kreeg 526', 'kreeg 527'),
        ('513, 514, 515, 516, 517]', '514, 515, 516, 517, 518]'),
    ],
)

build(
    'create-five-hundred-forty-one-bootstrap.py',
    'create-five-hundred-forty-two-bootstrap.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('all_cases[:526]', 'all_cases[:527]'),
        ('{UNKNOWN, TYPO}][:526]', '{UNKNOWN, TYPO}][:527]'),
        ('!= 526', '!= 527'),
        ('kreeg 526', 'kreeg 527'),
        ('509, 510, 511, 512, 513]', '510, 511, 512, 513, 514]'),
    ],
)

build(
    'create-five-hundred-forty-one-minimal.py',
    'create-five-hundred-forty-two-minimal.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('!= 526', '!= 527'),
        ('kreeg 526', 'kreeg 527'),
        ('509, 510, 511, 512, 513]', '510, 511, 512, 513, 514]'),
    ],
)

build(
    'make-five-hundred-forty-one.py',
    'make-five-hundred-forty-two.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('all_cases[:526]', 'all_cases[:527]'),
        ('{UNKNOWN, TYPO}][:526]', '{UNKNOWN, TYPO}][:527]'),
        ('!= 526', '!= 527'),
        ('449, 450, 451, 452, 453]', '450, 451, 452, 453, 454]'),
    ],
)

build(
    'create-five-hundred-forty-one-files.py',
    'create-five-hundred-forty-two-files.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('all_cases[:526]', 'all_cases[:527]'),
        ('{UNKNOWN, TYPO}][:526]', '{UNKNOWN, TYPO}][:527]'),
        ('!= 526', '!= 527'),
        ('449, 450, 451, 452, 453]', '450, 451, 452, 453, 454]'),
    ],
)

build(
    'create-five-hundred-forty-one.py',
    'create-five-hundred-forty-two.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('all_cases[:526]', 'all_cases[:527]'),
        ('{UNKNOWN, TYPO}][:526]', '{UNKNOWN, TYPO}][:527]'),
        ('!= 526', '!= 527'),
        ('452, 453, 454, 455, 456]', '453, 454, 455, 456, 457]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-one.py',
    'generate-validate-five-hundred-forty-two.py',
    [
        ('five-hundred-forty-one', 'five-hundred-forty-two'),
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('all_cases[:526]', 'all_cases[:527]'),
        ('{UNKNOWN, TYPO}][:526]', '{UNKNOWN, TYPO}][:527]'),
        ('!= 526', '!= 527'),
        ('449, 450, 451, 452, 453]', '450, 451, 452, 453, 454]'),
    ],
)

build(
    'validate-five-hundred-forty-one-valid-list-cases.py',
    'validate-five-hundred-forty-two-valid-list-cases.py',
    [
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('511, 512, 513, 514, 515', '512, 513, 514, 515, 516'),
        ('all_cases[:526]', 'all_cases[:527]'),
        ('len(valid_cases) != 526', 'len(valid_cases) != 527'),
    ],
)

build(
    'validate-five-hundred-forty-one-valid-mixed.py',
    'validate-five-hundred-forty-two-valid-mixed.py',
    [
        ('vijfhonderdeenenveertig', 'vijfhonderdtweeënveertig'),
        ('511, 512, 513, 514, 515', '512, 513, 514, 515, 516'),
        ('][:526]', '][:527]'),
        ('len(valid_cases) != 526', 'len(valid_cases) != 527'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-one.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-one', 'five-hundred-forty-two')
(ROOT / 'verify-five-hundred-forty-two.py').write_text(verify_text)
print('verify-five-hundred-forty-two.py')
