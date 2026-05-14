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
    'create-five-hundred-ninety-four-assets.py',
    'create-five-hundred-ninety-five-assets.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('[:579]', '[:580]'),
        ('!= 579', '!= 580'),
        ('kreeg 579', 'kreeg 580'),
        ('566, 567, 568, 569, 570', '567, 568, 569, 570, 571'),
    ],
)

build(
    'create-five-hundred-ninety-four-bootstrap.py',
    'create-five-hundred-ninety-five-bootstrap.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('all_cases[:579]', 'all_cases[:580]'),
        ('{UNKNOWN, TYPO}][:579]', '{UNKNOWN, TYPO}][:580]'),
        ('!= 579', '!= 580'),
        ('kreeg 579', 'kreeg 580'),
        ('562, 563, 564, 565, 566', '563, 564, 565, 566, 567'),
    ],
)

build(
    'create-five-hundred-ninety-four-minimal.py',
    'create-five-hundred-ninety-five-minimal.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('!= 579', '!= 580'),
        ('kreeg 579', 'kreeg 580'),
        ('562, 563, 564, 565, 566', '563, 564, 565, 566, 567'),
    ],
)

build(
    'make-five-hundred-ninety-four.py',
    'make-five-hundred-ninety-five.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('all_cases[:579]', 'all_cases[:580]'),
        ('{UNKNOWN, TYPO}][:579]', '{UNKNOWN, TYPO}][:580]'),
        ('!= 579', '!= 580'),
        ('502, 503, 504, 505, 506', '503, 504, 505, 506, 507'),
    ],
)

build(
    'create-five-hundred-ninety-four-files.py',
    'create-five-hundred-ninety-five-files.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('all_cases[:579]', 'all_cases[:580]'),
        ('{UNKNOWN, TYPO}][:579]', '{UNKNOWN, TYPO}][:580]'),
        ('!= 579', '!= 580'),
        ('502, 503, 504, 505, 506', '503, 504, 505, 506, 507'),
    ],
)

build(
    'create-five-hundred-ninety-four.py',
    'create-five-hundred-ninety-five.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('all_cases[:579]', 'all_cases[:580]'),
        ('{UNKNOWN, TYPO}][:579]', '{UNKNOWN, TYPO}][:580]'),
        ('!= 579', '!= 580'),
        ('505, 506, 507, 508, 509', '506, 507, 508, 509, 510'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-four.py',
    'generate-validate-five-hundred-ninety-five.py',
    [
        ('five-hundred-ninety-four', 'five-hundred-ninety-five'),
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('all_cases[:579]', 'all_cases[:580]'),
        ('{UNKNOWN, TYPO}][:579]', '{UNKNOWN, TYPO}][:580]'),
        ('!= 579', '!= 580'),
        ('502, 503, 504, 505, 506', '503, 504, 505, 506, 507'),
    ],
)

build(
    'validate-five-hundred-ninety-four-valid-list-cases.py',
    'validate-five-hundred-ninety-five-valid-list-cases.py',
    [
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('564, 565, 566, 567, 568', '565, 566, 567, 568, 569'),
        ('all_cases[:579]', 'all_cases[:580]'),
        ('len(valid_cases) != 579', 'len(valid_cases) != 580'),
    ],
)

build(
    'validate-five-hundred-ninety-four-valid-mixed.py',
    'validate-five-hundred-ninety-five-valid-mixed.py',
    [
        ('vijfhonderdvierennegentig', 'vijfhonderdvijfennegentig'),
        ('564, 565, 566, 567, 568', '565, 566, 567, 568, 569'),
        ('][:579]', '][:580]'),
        ('len(valid_cases) != 579', 'len(valid_cases) != 580'),
        ('plain stderr noemt niet alle vijfhonderdnegenenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdtachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-four.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-four', 'five-hundred-ninety-five')
(ROOT / 'verify-five-hundred-ninety-five.py').write_text(verify_text)
print('verify-five-hundred-ninety-five.py')
