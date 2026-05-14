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
    'create-five-hundred-ninety-six-assets.py',
    'create-five-hundred-ninety-seven-assets.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('[:581]', '[:582]'),
        ('!= 581', '!= 582'),
        ('kreeg 581', 'kreeg 582'),
        ('568, 569, 570, 571, 572', '569, 570, 571, 572, 573'),
    ],
)

build(
    'create-five-hundred-ninety-six-bootstrap.py',
    'create-five-hundred-ninety-seven-bootstrap.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('all_cases[:581]', 'all_cases[:582]'),
        ('{UNKNOWN, TYPO}][:581]', '{UNKNOWN, TYPO}][:582]'),
        ('!= 581', '!= 582'),
        ('kreeg 581', 'kreeg 582'),
        ('564, 565, 566, 567, 568', '565, 566, 567, 568, 569'),
    ],
)

build(
    'create-five-hundred-ninety-six-minimal.py',
    'create-five-hundred-ninety-seven-minimal.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('!= 581', '!= 582'),
        ('kreeg 581', 'kreeg 582'),
        ('564, 565, 566, 567, 568', '565, 566, 567, 568, 569'),
    ],
)

build(
    'make-five-hundred-ninety-six.py',
    'make-five-hundred-ninety-seven.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('all_cases[:581]', 'all_cases[:582]'),
        ('{UNKNOWN, TYPO}][:581]', '{UNKNOWN, TYPO}][:582]'),
        ('!= 581', '!= 582'),
        ('504, 505, 506, 507, 508', '505, 506, 507, 508, 509'),
    ],
)

build(
    'create-five-hundred-ninety-six-files.py',
    'create-five-hundred-ninety-seven-files.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('all_cases[:581]', 'all_cases[:582]'),
        ('{UNKNOWN, TYPO}][:581]', '{UNKNOWN, TYPO}][:582]'),
        ('!= 581', '!= 582'),
        ('504, 505, 506, 507, 508', '505, 506, 507, 508, 509'),
    ],
)

build(
    'create-five-hundred-ninety-six.py',
    'create-five-hundred-ninety-seven.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('all_cases[:581]', 'all_cases[:582]'),
        ('{UNKNOWN, TYPO}][:581]', '{UNKNOWN, TYPO}][:582]'),
        ('!= 581', '!= 582'),
        ('507, 508, 509, 510, 511', '508, 509, 510, 511, 512'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-six.py',
    'generate-validate-five-hundred-ninety-seven.py',
    [
        ('five-hundred-ninety-six', 'five-hundred-ninety-seven'),
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('all_cases[:581]', 'all_cases[:582]'),
        ('{UNKNOWN, TYPO}][:581]', '{UNKNOWN, TYPO}][:582]'),
        ('!= 581', '!= 582'),
        ('504, 505, 506, 507, 508', '505, 506, 507, 508, 509'),
    ],
)

build(
    'validate-five-hundred-ninety-six-valid-list-cases.py',
    'validate-five-hundred-ninety-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('566, 567, 568, 569, 570', '567, 568, 569, 570, 571'),
        ('all_cases[:581]', 'all_cases[:582]'),
        ('len(valid_cases) != 581', 'len(valid_cases) != 582'),
    ],
)

build(
    'validate-five-hundred-ninety-six-valid-mixed.py',
    'validate-five-hundred-ninety-seven-valid-mixed.py',
    [
        ('vijfhonderdzesennegentig', 'vijfhonderdzevenennegentig'),
        ('566, 567, 568, 569, 570', '567, 568, 569, 570, 571'),
        ('][:581]', '][:582]'),
        ('len(valid_cases) != 581', 'len(valid_cases) != 582'),
        ('plain stderr noemt niet alle vijfhonderdeenentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdtweeëntachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-six.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-six', 'five-hundred-ninety-seven')
(ROOT / 'verify-five-hundred-ninety-seven.py').write_text(verify_text)
print('verify-five-hundred-ninety-seven.py')
