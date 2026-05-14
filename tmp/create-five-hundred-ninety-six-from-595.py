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
    'create-five-hundred-ninety-five-assets.py',
    'create-five-hundred-ninety-six-assets.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('[:580]', '[:581]'),
        ('!= 580', '!= 581'),
        ('kreeg 580', 'kreeg 581'),
        ('567, 568, 569, 570, 571', '568, 569, 570, 571, 572'),
    ],
)

build(
    'create-five-hundred-ninety-five-bootstrap.py',
    'create-five-hundred-ninety-six-bootstrap.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('all_cases[:580]', 'all_cases[:581]'),
        ('{UNKNOWN, TYPO}][:580]', '{UNKNOWN, TYPO}][:581]'),
        ('!= 580', '!= 581'),
        ('kreeg 580', 'kreeg 581'),
        ('563, 564, 565, 566, 567', '564, 565, 566, 567, 568'),
    ],
)

build(
    'create-five-hundred-ninety-five-minimal.py',
    'create-five-hundred-ninety-six-minimal.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('!= 580', '!= 581'),
        ('kreeg 580', 'kreeg 581'),
        ('563, 564, 565, 566, 567', '564, 565, 566, 567, 568'),
    ],
)

build(
    'make-five-hundred-ninety-five.py',
    'make-five-hundred-ninety-six.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('all_cases[:580]', 'all_cases[:581]'),
        ('{UNKNOWN, TYPO}][:580]', '{UNKNOWN, TYPO}][:581]'),
        ('!= 580', '!= 581'),
        ('503, 504, 505, 506, 507', '504, 505, 506, 507, 508'),
    ],
)

build(
    'create-five-hundred-ninety-five-files.py',
    'create-five-hundred-ninety-six-files.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('all_cases[:580]', 'all_cases[:581]'),
        ('{UNKNOWN, TYPO}][:580]', '{UNKNOWN, TYPO}][:581]'),
        ('!= 580', '!= 581'),
        ('503, 504, 505, 506, 507', '504, 505, 506, 507, 508'),
    ],
)

build(
    'create-five-hundred-ninety-five.py',
    'create-five-hundred-ninety-six.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('all_cases[:580]', 'all_cases[:581]'),
        ('{UNKNOWN, TYPO}][:580]', '{UNKNOWN, TYPO}][:581]'),
        ('!= 580', '!= 581'),
        ('506, 507, 508, 509, 510', '507, 508, 509, 510, 511'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-five.py',
    'generate-validate-five-hundred-ninety-six.py',
    [
        ('five-hundred-ninety-five', 'five-hundred-ninety-six'),
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('all_cases[:580]', 'all_cases[:581]'),
        ('{UNKNOWN, TYPO}][:580]', '{UNKNOWN, TYPO}][:581]'),
        ('!= 580', '!= 581'),
        ('503, 504, 505, 506, 507', '504, 505, 506, 507, 508'),
    ],
)

build(
    'validate-five-hundred-ninety-five-valid-list-cases.py',
    'validate-five-hundred-ninety-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('565, 566, 567, 568, 569', '566, 567, 568, 569, 570'),
        ('all_cases[:580]', 'all_cases[:581]'),
        ('len(valid_cases) != 580', 'len(valid_cases) != 581'),
    ],
)

build(
    'validate-five-hundred-ninety-five-valid-mixed.py',
    'validate-five-hundred-ninety-six-valid-mixed.py',
    [
        ('vijfhonderdvijfennegentig', 'vijfhonderdzesennegentig'),
        ('565, 566, 567, 568, 569', '566, 567, 568, 569, 570'),
        ('][:580]', '][:581]'),
        ('len(valid_cases) != 580', 'len(valid_cases) != 581'),
        ('plain stderr noemt niet alle vijfhonderdtachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdeenentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-five.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-five', 'five-hundred-ninety-six')
(ROOT / 'verify-five-hundred-ninety-six.py').write_text(verify_text)
print('verify-five-hundred-ninety-six.py')
