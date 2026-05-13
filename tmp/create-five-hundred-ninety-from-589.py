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
    'create-five-hundred-eighty-nine-assets.py',
    'create-five-hundred-ninety-assets.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('[:574]', '[:575]'),
        ('!= 574', '!= 575'),
        ('kreeg 574', 'kreeg 575'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'create-five-hundred-eighty-nine-bootstrap.py',
    'create-five-hundred-ninety-bootstrap.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('all_cases[:574]', 'all_cases[:575]'),
        ('{UNKNOWN, TYPO}][:574]', '{UNKNOWN, TYPO}][:575]'),
        ('!= 574', '!= 575'),
        ('kreeg 574', 'kreeg 575'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'create-five-hundred-eighty-nine-minimal.py',
    'create-five-hundred-ninety-minimal.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('!= 574', '!= 575'),
        ('kreeg 574', 'kreeg 575'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'make-five-hundred-eighty-nine.py',
    'make-five-hundred-ninety.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('all_cases[:574]', 'all_cases[:575]'),
        ('{UNKNOWN, TYPO}][:574]', '{UNKNOWN, TYPO}][:575]'),
        ('!= 574', '!= 575'),
        ('497, 498, 499, 500, 501', '498, 499, 500, 501, 502'),
    ],
)

build(
    'create-five-hundred-eighty-nine-files.py',
    'create-five-hundred-ninety-files.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('all_cases[:574]', 'all_cases[:575]'),
        ('{UNKNOWN, TYPO}][:574]', '{UNKNOWN, TYPO}][:575]'),
        ('!= 574', '!= 575'),
        ('497, 498, 499, 500, 501', '498, 499, 500, 501, 502'),
    ],
)

build(
    'create-five-hundred-eighty-nine.py',
    'create-five-hundred-ninety.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('all_cases[:574]', 'all_cases[:575]'),
        ('{UNKNOWN, TYPO}][:574]', '{UNKNOWN, TYPO}][:575]'),
        ('!= 574', '!= 575'),
        ('500, 501, 502, 503, 504', '501, 502, 503, 504, 505'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-nine.py',
    'generate-validate-five-hundred-ninety.py',
    [
        ('five-hundred-eighty-nine', 'five-hundred-ninety'),
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('all_cases[:574]', 'all_cases[:575]'),
        ('{UNKNOWN, TYPO}][:574]', '{UNKNOWN, TYPO}][:575]'),
        ('!= 574', '!= 575'),
        ('497, 498, 499, 500, 501', '498, 499, 500, 501, 502'),
    ],
)

build(
    'validate-five-hundred-eighty-nine-valid-list-cases.py',
    'validate-five-hundred-ninety-valid-list-cases.py',
    [
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
        ('all_cases[:574]', 'all_cases[:575]'),
        ('len(valid_cases) != 574', 'len(valid_cases) != 575'),
    ],
)

build(
    'validate-five-hundred-eighty-nine-valid-mixed.py',
    'validate-five-hundred-ninety-valid-mixed.py',
    [
        ('vijfhonderdnegenentachtig', 'vijfhonderdnegentig'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
        ('][:574]', '][:575]'),
        ('len(valid_cases) != 574', 'len(valid_cases) != 575'),
        ('plain stderr noemt niet alle vijfhonderdvierenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvijfenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-nine', 'five-hundred-ninety')
(ROOT / 'verify-five-hundred-ninety.py').write_text(verify_text)
print('verify-five-hundred-ninety.py')
