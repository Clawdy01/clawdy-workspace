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
    'create-five-hundred-thirty-six-assets.py',
    'create-five-hundred-thirty-seven-assets.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('[:521]', '[:522]'),
        ('!= 521', '!= 522'),
        ('kreeg 521', 'kreeg 522'),
        ('510, 511, 512]', '510, 511, 512, 513]'),
    ],
)

build(
    'create-five-hundred-thirty-six-bootstrap.py',
    'create-five-hundred-thirty-seven-bootstrap.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('all_cases[:521]', 'all_cases[:522]'),
        ('{UNKNOWN, TYPO}][:521]', '{UNKNOWN, TYPO}][:522]'),
        ('!= 521', '!= 522'),
        ('kreeg 521', 'kreeg 522'),
        ('506, 507, 508]', '506, 507, 508, 509]'),
    ],
)

build(
    'create-five-hundred-thirty-six-minimal.py',
    'create-five-hundred-thirty-seven-minimal.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('!= 521', '!= 522'),
        ('kreeg 521', 'kreeg 522'),
        (' 507, 508]', ' 507, 508, 509]'),
    ],
)

build(
    'make-five-hundred-thirty-six.py',
    'make-five-hundred-thirty-seven.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('all_cases[:521]', 'all_cases[:522]'),
        ('{UNKNOWN, TYPO}][:521]', '{UNKNOWN, TYPO}][:522]'),
        ('!= 521', '!= 522'),
        ('446, 447, 448]', '446, 447, 448, 449]'),
    ],
)

build(
    'create-five-hundred-thirty-six-files.py',
    'create-five-hundred-thirty-seven-files.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('all_cases[:521]', 'all_cases[:522]'),
        ('{UNKNOWN, TYPO}][:521]', '{UNKNOWN, TYPO}][:522]'),
        ('!= 521', '!= 522'),
        ('446, 447, 448]', '446, 447, 448, 449]'),
    ],
)

build(
    'create-five-hundred-thirty-six.py',
    'create-five-hundred-thirty-seven.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('all_cases[:521]', 'all_cases[:522]'),
        ('{UNKNOWN, TYPO}][:521]', '{UNKNOWN, TYPO}][:522]'),
        ('!= 521', '!= 522'),
        ('449, 450, 451]', '449, 450, 451, 452]'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-six.py',
    'generate-validate-five-hundred-thirty-seven.py',
    [
        ('five-hundred-thirty-six', 'five-hundred-thirty-seven'),
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('all_cases[:521]', 'all_cases[:522]'),
        ('{UNKNOWN, TYPO}][:521]', '{UNKNOWN, TYPO}][:522]'),
        ('!= 521', '!= 522'),
        ('446, 447, 448]', '446, 447, 448, 449]'),
    ],
)

build(
    'validate-five-hundred-thirty-six-valid-list-cases.py',
    'validate-five-hundred-thirty-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('508, 509, 510', '508, 509, 510, 511'),
        ('all_cases[:521]', 'all_cases[:522]'),
        ('len(valid_cases) != 521', 'len(valid_cases) != 522'),
    ],
)

build(
    'validate-five-hundred-thirty-six-valid-mixed.py',
    'validate-five-hundred-thirty-seven-valid-mixed.py',
    [
        ('vijfhonderdzesendertig', 'vijfhonderdzevenendertig'),
        ('508, 509, 510', '508, 509, 510, 511'),
        ('][:521]', '][:522]'),
        ('len(valid_cases) != 521', 'len(valid_cases) != 522'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-six.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-six', 'five-hundred-thirty-seven')
(ROOT / 'verify-five-hundred-thirty-seven.py').write_text(verify_text)
print('verify-five-hundred-thirty-seven.py')
