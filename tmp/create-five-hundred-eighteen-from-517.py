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
    'create-five-hundred-seventeen-assets.py',
    'create-five-hundred-eighteen-assets.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('[:502]', '[:503]'),
        ('!= 502', '!= 503'),
        ('kreeg 502', 'kreeg 503'),
        ('488, 489, 490, 491, 492, 493]', '488, 489, 490, 491, 492, 493, 494]'),
    ],
)

build(
    'create-five-hundred-seventeen-bootstrap.py',
    'create-five-hundred-eighteen-bootstrap.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('all_cases[:502]', 'all_cases[:503]'),
        ('{UNKNOWN, TYPO}][:502]', '{UNKNOWN, TYPO}][:503]'),
        ('!= 502', '!= 503'),
        ('kreeg 502', 'kreeg 503'),
        ('484, 485, 486, 487, 488, 489]', '484, 485, 486, 487, 488, 489, 490]'),
    ],
)

build(
    'create-five-hundred-seventeen-minimal.py',
    'create-five-hundred-eighteen-minimal.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('!= 502', '!= 503'),
        ('kreeg 502', 'kreeg 503'),
        (' 443)', ' 444)'),
        ('484, 485, 486, 487, 488, 489]', '484, 485, 486, 487, 488, 489, 490]'),
    ],
)

build(
    'make-five-hundred-seventeen.py',
    'make-five-hundred-eighteen.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('all_cases[:502]', 'all_cases[:503]'),
        ('{UNKNOWN, TYPO}][:502]', '{UNKNOWN, TYPO}][:503]'),
        ('!= 502', '!= 503'),
        ('424, 425, 426, 427, 428, 429]', '424, 425, 426, 427, 428, 429, 430]'),
    ],
)

build(
    'create-five-hundred-seventeen-files.py',
    'create-five-hundred-eighteen-files.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('all_cases[:502]', 'all_cases[:503]'),
        ('{UNKNOWN, TYPO}][:502]', '{UNKNOWN, TYPO}][:503]'),
        ('!= 502', '!= 503'),
        ('424, 425, 426, 427, 428, 429]', '424, 425, 426, 427, 428, 429, 430]'),
    ],
)

build(
    'create-five-hundred-seventeen.py',
    'create-five-hundred-eighteen.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('all_cases[:502]', 'all_cases[:503]'),
        ('{UNKNOWN, TYPO}][:502]', '{UNKNOWN, TYPO}][:503]'),
        ('!= 502', '!= 503'),
        ('428, 429, 430, 431, 432]', '428, 429, 430, 431, 432, 433]'),
    ],
)

build(
    'generate-validate-five-hundred-seventeen.py',
    'generate-validate-five-hundred-eighteen.py',
    [
        ('five-hundred-seventeen', 'five-hundred-eighteen'),
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('all_cases[:502]', 'all_cases[:503]'),
        ('{UNKNOWN, TYPO}][:502]', '{UNKNOWN, TYPO}][:503]'),
        ('!= 502', '!= 503'),
        ('424, 425, 426, 427, 428, 429]', '424, 425, 426, 427, 428, 429, 430]'),
    ],
)

build(
    'validate-five-hundred-seventeen-valid-list-cases.py',
    'validate-five-hundred-eighteen-valid-list-cases.py',
    [
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('486, 487, 488, 489, 490, 491]', '486, 487, 488, 489, 490, 491, 492]'),
        ('all_cases[:502]', 'all_cases[:503]'),
        ('len(valid_cases) != 502', 'len(valid_cases) != 503'),
    ],
)

build(
    'validate-five-hundred-seventeen-valid-mixed.py',
    'validate-five-hundred-eighteen-valid-mixed.py',
    [
        ('vijfhonderdzeventien', 'vijfhonderdachttien'),
        ('486, 487, 488, 489, 490, 491]', '486, 487, 488, 489, 490, 491, 492]'),
        ('][:502]', '][:503]'),
        ('len(valid_cases) != 502', 'len(valid_cases) != 503'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventeen.py').read_text()
verify_text = verify_src.replace('five-hundred-seventeen', 'five-hundred-eighteen')
(ROOT / 'verify-five-hundred-eighteen.py').write_text(verify_text)
print('verify-five-hundred-eighteen.py')
