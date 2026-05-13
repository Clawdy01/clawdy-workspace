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
    'create-five-hundred-forty-six-assets.py',
    'create-five-hundred-forty-seven-assets.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('[:531]', '[:532]'),
        ('!= 531', '!= 532'),
        ('kreeg 531', 'kreeg 532'),
        ('518, 519, 520, 521, 522]', '519, 520, 521, 522, 523]'),
    ],
)

build(
    'create-five-hundred-forty-six-bootstrap.py',
    'create-five-hundred-forty-seven-bootstrap.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('all_cases[:531]', 'all_cases[:532]'),
        ('{UNKNOWN, TYPO}][:531]', '{UNKNOWN, TYPO}][:532]'),
        ('!= 531', '!= 532'),
        ('kreeg 531', 'kreeg 532'),
        ('514, 515, 516, 517, 518]', '515, 516, 517, 518, 519]'),
    ],
)

build(
    'create-five-hundred-forty-six-minimal.py',
    'create-five-hundred-forty-seven-minimal.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('!= 531', '!= 532'),
        ('kreeg 531', 'kreeg 532'),
        ('514, 515, 516, 517, 518]', '515, 516, 517, 518, 519]'),
    ],
)

build(
    'make-five-hundred-forty-six.py',
    'make-five-hundred-forty-seven.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('all_cases[:531]', 'all_cases[:532]'),
        ('{UNKNOWN, TYPO}][:531]', '{UNKNOWN, TYPO}][:532]'),
        ('!= 531', '!= 532'),
        ('454, 455, 456, 457, 458]', '455, 456, 457, 458, 459]'),
    ],
)

build(
    'create-five-hundred-forty-six-files.py',
    'create-five-hundred-forty-seven-files.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('all_cases[:531]', 'all_cases[:532]'),
        ('{UNKNOWN, TYPO}][:531]', '{UNKNOWN, TYPO}][:532]'),
        ('!= 531', '!= 532'),
        ('454, 455, 456, 457, 458]', '455, 456, 457, 458, 459]'),
    ],
)

build(
    'create-five-hundred-forty-six.py',
    'create-five-hundred-forty-seven.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('all_cases[:531]', 'all_cases[:532]'),
        ('{UNKNOWN, TYPO}][:531]', '{UNKNOWN, TYPO}][:532]'),
        ('!= 531', '!= 532'),
        ('457, 458, 459, 460, 461]', '458, 459, 460, 461, 462]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-six.py',
    'generate-validate-five-hundred-forty-seven.py',
    [
        ('five-hundred-forty-six', 'five-hundred-forty-seven'),
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('all_cases[:531]', 'all_cases[:532]'),
        ('{UNKNOWN, TYPO}][:531]', '{UNKNOWN, TYPO}][:532]'),
        ('!= 531', '!= 532'),
        ('454, 455, 456, 457, 458]', '455, 456, 457, 458, 459]'),
    ],
)

build(
    'validate-five-hundred-forty-six-valid-list-cases.py',
    'validate-five-hundred-forty-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('516, 517, 518, 519, 520', '517, 518, 519, 520, 521'),
        ('all_cases[:531]', 'all_cases[:532]'),
        ('len(valid_cases) != 531', 'len(valid_cases) != 532'),
    ],
)

build(
    'validate-five-hundred-forty-six-valid-mixed.py',
    'validate-five-hundred-forty-seven-valid-mixed.py',
    [
        ('vijfhonderdzesenveertig', 'vijfhonderdzevenenveertig'),
        ('516, 517, 518, 519, 520', '517, 518, 519, 520, 521'),
        ('][:531]', '][:532]'),
        ('len(valid_cases) != 531', 'len(valid_cases) != 532'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-six.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-six', 'five-hundred-forty-seven')
(ROOT / 'verify-five-hundred-forty-seven.py').write_text(verify_text)
print('verify-five-hundred-forty-seven.py')
