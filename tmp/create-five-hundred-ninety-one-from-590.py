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
    'create-five-hundred-ninety-assets.py',
    'create-five-hundred-ninety-one-assets.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('[:575]', '[:576]'),
        ('!= 575', '!= 576'),
        ('kreeg 575', 'kreeg 576'),
        ('562, 563, 564, 565, 566', '563, 564, 565, 566, 567'),
    ],
)

build(
    'create-five-hundred-ninety-bootstrap.py',
    'create-five-hundred-ninety-one-bootstrap.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('all_cases[:575]', 'all_cases[:576]'),
        ('{UNKNOWN, TYPO}][:575]', '{UNKNOWN, TYPO}][:576]'),
        ('!= 575', '!= 576'),
        ('kreeg 575', 'kreeg 576'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'create-five-hundred-ninety-minimal.py',
    'create-five-hundred-ninety-one-minimal.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('!= 575', '!= 576'),
        ('kreeg 575', 'kreeg 576'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'make-five-hundred-ninety.py',
    'make-five-hundred-ninety-one.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('all_cases[:575]', 'all_cases[:576]'),
        ('{UNKNOWN, TYPO}][:575]', '{UNKNOWN, TYPO}][:576]'),
        ('!= 575', '!= 576'),
        ('498, 499, 500, 501, 502', '499, 500, 501, 502, 503'),
    ],
)

build(
    'create-five-hundred-ninety-files.py',
    'create-five-hundred-ninety-one-files.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('all_cases[:575]', 'all_cases[:576]'),
        ('{UNKNOWN, TYPO}][:575]', '{UNKNOWN, TYPO}][:576]'),
        ('!= 575', '!= 576'),
        ('498, 499, 500, 501, 502', '499, 500, 501, 502, 503'),
    ],
)

build(
    'create-five-hundred-ninety.py',
    'create-five-hundred-ninety-one.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('all_cases[:575]', 'all_cases[:576]'),
        ('{UNKNOWN, TYPO}][:575]', '{UNKNOWN, TYPO}][:576]'),
        ('!= 575', '!= 576'),
        ('501, 502, 503, 504, 505', '502, 503, 504, 505, 506'),
    ],
)

build(
    'generate-validate-five-hundred-ninety.py',
    'generate-validate-five-hundred-ninety-one.py',
    [
        ('five-hundred-ninety', 'five-hundred-ninety-one'),
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('all_cases[:575]', 'all_cases[:576]'),
        ('{UNKNOWN, TYPO}][:575]', '{UNKNOWN, TYPO}][:576]'),
        ('!= 575', '!= 576'),
        ('498, 499, 500, 501, 502', '499, 500, 501, 502, 503'),
    ],
)

build(
    'validate-five-hundred-ninety-valid-list-cases.py',
    'validate-five-hundred-ninety-one-valid-list-cases.py',
    [
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
        ('all_cases[:575]', 'all_cases[:576]'),
        ('len(valid_cases) != 575', 'len(valid_cases) != 576'),
    ],
)

build(
    'validate-five-hundred-ninety-valid-mixed.py',
    'validate-five-hundred-ninety-one-valid-mixed.py',
    [
        ('vijfhonderdnegentig', 'vijfhonderdeenennegentig'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
        ('][:575]', '][:576]'),
        ('len(valid_cases) != 575', 'len(valid_cases) != 576'),
        ('plain stderr noemt niet alle vijfhonderdvijfenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzesenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety', 'five-hundred-ninety-one')
(ROOT / 'verify-five-hundred-ninety-one.py').write_text(verify_text)
print('verify-five-hundred-ninety-one.py')
