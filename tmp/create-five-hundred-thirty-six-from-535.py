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
    'create-five-hundred-thirty-five-assets.py',
    'create-five-hundred-thirty-six-assets.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('[:520]', '[:521]'),
        ('!= 520', '!= 521'),
        ('kreeg 520', 'kreeg 521'),
        ('509, 510, 511]', '509, 510, 511, 512]'),
    ],
)

build(
    'create-five-hundred-thirty-five-bootstrap.py',
    'create-five-hundred-thirty-six-bootstrap.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('all_cases[:520]', 'all_cases[:521]'),
        ('{UNKNOWN, TYPO}][:520]', '{UNKNOWN, TYPO}][:521]'),
        ('!= 520', '!= 521'),
        ('kreeg 520', 'kreeg 521'),
        ('505, 506, 507]', '505, 506, 507, 508]'),
    ],
)

build(
    'create-five-hundred-thirty-five-minimal.py',
    'create-five-hundred-thirty-six-minimal.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('!= 520', '!= 521'),
        ('kreeg 520', 'kreeg 521'),
        (' 507]', ' 507, 508]'),
    ],
)

build(
    'make-five-hundred-thirty-five.py',
    'make-five-hundred-thirty-six.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('all_cases[:520]', 'all_cases[:521]'),
        ('{UNKNOWN, TYPO}][:520]', '{UNKNOWN, TYPO}][:521]'),
        ('!= 520', '!= 521'),
        ('445, 446, 447]', '445, 446, 447, 448]'),
    ],
)

build(
    'create-five-hundred-thirty-five-files.py',
    'create-five-hundred-thirty-six-files.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('all_cases[:520]', 'all_cases[:521]'),
        ('{UNKNOWN, TYPO}][:520]', '{UNKNOWN, TYPO}][:521]'),
        ('!= 520', '!= 521'),
        ('445, 446, 447]', '445, 446, 447, 448]'),
    ],
)

build(
    'create-five-hundred-thirty-five.py',
    'create-five-hundred-thirty-six.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('all_cases[:520]', 'all_cases[:521]'),
        ('{UNKNOWN, TYPO}][:520]', '{UNKNOWN, TYPO}][:521]'),
        ('!= 520', '!= 521'),
        ('448, 449, 450]', '448, 449, 450, 451]'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-five.py',
    'generate-validate-five-hundred-thirty-six.py',
    [
        ('five-hundred-thirty-five', 'five-hundred-thirty-six'),
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('all_cases[:520]', 'all_cases[:521]'),
        ('{UNKNOWN, TYPO}][:520]', '{UNKNOWN, TYPO}][:521]'),
        ('!= 520', '!= 521'),
        ('445, 446, 447]', '445, 446, 447, 448]'),
    ],
)

build(
    'validate-five-hundred-thirty-five-valid-list-cases.py',
    'validate-five-hundred-thirty-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('507, 508, 509', '507, 508, 509, 510'),
        ('all_cases[:520]', 'all_cases[:521]'),
        ('len(valid_cases) != 520', 'len(valid_cases) != 521'),
    ],
)

build(
    'validate-five-hundred-thirty-five-valid-mixed.py',
    'validate-five-hundred-thirty-six-valid-mixed.py',
    [
        ('vijfhonderdvijfendertig', 'vijfhonderdzesendertig'),
        ('507, 508, 509', '507, 508, 509, 510'),
        ('][:520]', '][:521]'),
        ('len(valid_cases) != 520', 'len(valid_cases) != 521'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-five.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-five', 'five-hundred-thirty-six')
(ROOT / 'verify-five-hundred-thirty-six.py').write_text(verify_text)
print('verify-five-hundred-thirty-six.py')
