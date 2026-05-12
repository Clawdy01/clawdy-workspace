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
    'create-five-hundred-forty-four-assets.py',
    'create-five-hundred-forty-five-assets.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('[:529]', '[:530]'),
        ('!= 529', '!= 530'),
        ('kreeg 529', 'kreeg 530'),
        ('516, 517, 518, 519, 520]', '517, 518, 519, 520, 521]'),
    ],
)

build(
    'create-five-hundred-forty-four-bootstrap.py',
    'create-five-hundred-forty-five-bootstrap.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('all_cases[:529]', 'all_cases[:530]'),
        ('{UNKNOWN, TYPO}][:529]', '{UNKNOWN, TYPO}][:530]'),
        ('!= 529', '!= 530'),
        ('kreeg 529', 'kreeg 530'),
        ('512, 513, 514, 515, 516]', '513, 514, 515, 516, 517]'),
    ],
)

build(
    'create-five-hundred-forty-four-minimal.py',
    'create-five-hundred-forty-five-minimal.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('!= 529', '!= 530'),
        ('kreeg 529', 'kreeg 530'),
        ('512, 513, 514, 515, 516]', '513, 514, 515, 516, 517]'),
    ],
)

build(
    'make-five-hundred-forty-four.py',
    'make-five-hundred-forty-five.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('all_cases[:529]', 'all_cases[:530]'),
        ('{UNKNOWN, TYPO}][:529]', '{UNKNOWN, TYPO}][:530]'),
        ('!= 529', '!= 530'),
        ('452, 453, 454, 455, 456]', '453, 454, 455, 456, 457]'),
    ],
)

build(
    'create-five-hundred-forty-four-files.py',
    'create-five-hundred-forty-five-files.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('all_cases[:529]', 'all_cases[:530]'),
        ('{UNKNOWN, TYPO}][:529]', '{UNKNOWN, TYPO}][:530]'),
        ('!= 529', '!= 530'),
        ('452, 453, 454, 455, 456]', '453, 454, 455, 456, 457]'),
    ],
)

build(
    'create-five-hundred-forty-four.py',
    'create-five-hundred-forty-five.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('all_cases[:529]', 'all_cases[:530]'),
        ('{UNKNOWN, TYPO}][:529]', '{UNKNOWN, TYPO}][:530]'),
        ('!= 529', '!= 530'),
        ('455, 456, 457, 458, 459]', '456, 457, 458, 459, 460]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-four.py',
    'generate-validate-five-hundred-forty-five.py',
    [
        ('five-hundred-forty-four', 'five-hundred-forty-five'),
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('all_cases[:529]', 'all_cases[:530]'),
        ('{UNKNOWN, TYPO}][:529]', '{UNKNOWN, TYPO}][:530]'),
        ('!= 529', '!= 530'),
        ('452, 453, 454, 455, 456]', '453, 454, 455, 456, 457]'),
    ],
)

build(
    'validate-five-hundred-forty-four-valid-list-cases.py',
    'validate-five-hundred-forty-five-valid-list-cases.py',
    [
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('514, 515, 516, 517, 518', '515, 516, 517, 518, 519'),
        ('all_cases[:529]', 'all_cases[:530]'),
        ('len(valid_cases) != 529', 'len(valid_cases) != 530'),
    ],
)

build(
    'validate-five-hundred-forty-four-valid-mixed.py',
    'validate-five-hundred-forty-five-valid-mixed.py',
    [
        ('vijfhonderdvierenveertig', 'vijfhonderdvijfenveertig'),
        ('514, 515, 516, 517, 518', '515, 516, 517, 518, 519'),
        ('][:529]', '][:530]'),
        ('len(valid_cases) != 529', 'len(valid_cases) != 530'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-four.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-four', 'five-hundred-forty-five')
(ROOT / 'verify-five-hundred-forty-five.py').write_text(verify_text)
print('verify-five-hundred-forty-five.py')
