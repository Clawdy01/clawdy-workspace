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
    'create-five-hundred-ninety-one-assets.py',
    'create-five-hundred-ninety-two-assets.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('[:576]', '[:577]'),
        ('!= 576', '!= 577'),
        ('kreeg 576', 'kreeg 577'),
        ('563, 564, 565, 566, 567', '564, 565, 566, 567, 568'),
    ],
)

build(
    'create-five-hundred-ninety-one-bootstrap.py',
    'create-five-hundred-ninety-two-bootstrap.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('all_cases[:576]', 'all_cases[:577]'),
        ('{UNKNOWN, TYPO}][:576]', '{UNKNOWN, TYPO}][:577]'),
        ('!= 576', '!= 577'),
        ('kreeg 576', 'kreeg 577'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'create-five-hundred-ninety-one-minimal.py',
    'create-five-hundred-ninety-two-minimal.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('!= 576', '!= 577'),
        ('kreeg 576', 'kreeg 577'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'make-five-hundred-ninety-one.py',
    'make-five-hundred-ninety-two.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('all_cases[:576]', 'all_cases[:577]'),
        ('{UNKNOWN, TYPO}][:576]', '{UNKNOWN, TYPO}][:577]'),
        ('!= 576', '!= 577'),
        ('499, 500, 501, 502, 503', '500, 501, 502, 503, 504'),
    ],
)

build(
    'create-five-hundred-ninety-one-files.py',
    'create-five-hundred-ninety-two-files.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('all_cases[:576]', 'all_cases[:577]'),
        ('{UNKNOWN, TYPO}][:576]', '{UNKNOWN, TYPO}][:577]'),
        ('!= 576', '!= 577'),
        ('499, 500, 501, 502, 503', '500, 501, 502, 503, 504'),
    ],
)

build(
    'create-five-hundred-ninety-one.py',
    'create-five-hundred-ninety-two.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('all_cases[:576]', 'all_cases[:577]'),
        ('{UNKNOWN, TYPO}][:576]', '{UNKNOWN, TYPO}][:577]'),
        ('!= 576', '!= 577'),
        ('502, 503, 504, 505, 506', '503, 504, 505, 506, 507'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-one.py',
    'generate-validate-five-hundred-ninety-two.py',
    [
        ('five-hundred-ninety-one', 'five-hundred-ninety-two'),
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('all_cases[:576]', 'all_cases[:577]'),
        ('{UNKNOWN, TYPO}][:576]', '{UNKNOWN, TYPO}][:577]'),
        ('!= 576', '!= 577'),
        ('499, 500, 501, 502, 503', '500, 501, 502, 503, 504'),
    ],
)

build(
    'validate-five-hundred-ninety-one-valid-list-cases.py',
    'validate-five-hundred-ninety-two-valid-list-cases.py',
    [
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
        ('all_cases[:576]', 'all_cases[:577]'),
        ('len(valid_cases) != 576', 'len(valid_cases) != 577'),
    ],
)

build(
    'validate-five-hundred-ninety-one-valid-mixed.py',
    'validate-five-hundred-ninety-two-valid-mixed.py',
    [
        ('vijfhonderdeenennegentig', 'vijfhonderdtweeënnegentig'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
        ('][:576]', '][:577]'),
        ('len(valid_cases) != 576', 'len(valid_cases) != 577'),
        ('plain stderr noemt niet alle vijfhonderdzesenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzevenenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-one.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-one', 'five-hundred-ninety-two')
(ROOT / 'verify-five-hundred-ninety-two.py').write_text(verify_text)
print('verify-five-hundred-ninety-two.py')
