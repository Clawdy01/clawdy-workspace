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
    'create-five-hundred-forty-five-assets.py',
    'create-five-hundred-forty-six-assets.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('[:530]', '[:531]'),
        ('!= 530', '!= 531'),
        ('kreeg 530', 'kreeg 531'),
        ('517, 518, 519, 520, 521]', '518, 519, 520, 521, 522]'),
    ],
)

build(
    'create-five-hundred-forty-five-bootstrap.py',
    'create-five-hundred-forty-six-bootstrap.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('all_cases[:530]', 'all_cases[:531]'),
        ('{UNKNOWN, TYPO}][:530]', '{UNKNOWN, TYPO}][:531]'),
        ('!= 530', '!= 531'),
        ('kreeg 530', 'kreeg 531'),
        ('513, 514, 515, 516, 517]', '514, 515, 516, 517, 518]'),
    ],
)

build(
    'create-five-hundred-forty-five-minimal.py',
    'create-five-hundred-forty-six-minimal.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('!= 530', '!= 531'),
        ('kreeg 530', 'kreeg 531'),
        ('513, 514, 515, 516, 517]', '514, 515, 516, 517, 518]'),
    ],
)

build(
    'make-five-hundred-forty-five.py',
    'make-five-hundred-forty-six.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('all_cases[:530]', 'all_cases[:531]'),
        ('{UNKNOWN, TYPO}][:530]', '{UNKNOWN, TYPO}][:531]'),
        ('!= 530', '!= 531'),
        ('453, 454, 455, 456, 457]', '454, 455, 456, 457, 458]'),
    ],
)

build(
    'create-five-hundred-forty-five-files.py',
    'create-five-hundred-forty-six-files.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('all_cases[:530]', 'all_cases[:531]'),
        ('{UNKNOWN, TYPO}][:530]', '{UNKNOWN, TYPO}][:531]'),
        ('!= 530', '!= 531'),
        ('453, 454, 455, 456, 457]', '454, 455, 456, 457, 458]'),
    ],
)

build(
    'create-five-hundred-forty-five.py',
    'create-five-hundred-forty-six.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('all_cases[:530]', 'all_cases[:531]'),
        ('{UNKNOWN, TYPO}][:530]', '{UNKNOWN, TYPO}][:531]'),
        ('!= 530', '!= 531'),
        ('456, 457, 458, 459, 460]', '457, 458, 459, 460, 461]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-five.py',
    'generate-validate-five-hundred-forty-six.py',
    [
        ('five-hundred-forty-five', 'five-hundred-forty-six'),
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('all_cases[:530]', 'all_cases[:531]'),
        ('{UNKNOWN, TYPO}][:530]', '{UNKNOWN, TYPO}][:531]'),
        ('!= 530', '!= 531'),
        ('453, 454, 455, 456, 457]', '454, 455, 456, 457, 458]'),
    ],
)

build(
    'validate-five-hundred-forty-five-valid-list-cases.py',
    'validate-five-hundred-forty-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('515, 516, 517, 518, 519', '516, 517, 518, 519, 520'),
        ('all_cases[:530]', 'all_cases[:531]'),
        ('len(valid_cases) != 530', 'len(valid_cases) != 531'),
    ],
)

build(
    'validate-five-hundred-forty-five-valid-mixed.py',
    'validate-five-hundred-forty-six-valid-mixed.py',
    [
        ('vijfhonderdvijfenveertig', 'vijfhonderdzesenveertig'),
        ('515, 516, 517, 518, 519', '516, 517, 518, 519, 520'),
        ('][:530]', '][:531]'),
        ('len(valid_cases) != 530', 'len(valid_cases) != 531'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-five.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-five', 'five-hundred-forty-six')
(ROOT / 'verify-five-hundred-forty-six.py').write_text(verify_text)
print('verify-five-hundred-forty-six.py')
