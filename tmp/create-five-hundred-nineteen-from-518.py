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
    'create-five-hundred-eighteen-assets.py',
    'create-five-hundred-nineteen-assets.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('[:503]', '[:504]'),
        ('!= 503', '!= 504'),
        ('kreeg 503', 'kreeg 504'),
        ('488, 489, 490, 491, 492, 493, 494]', '488, 489, 490, 491, 492, 493, 494, 495]'),
    ],
)

build(
    'create-five-hundred-eighteen-bootstrap.py',
    'create-five-hundred-nineteen-bootstrap.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('all_cases[:503]', 'all_cases[:504]'),
        ('{UNKNOWN, TYPO}][:503]', '{UNKNOWN, TYPO}][:504]'),
        ('!= 503', '!= 504'),
        ('kreeg 503', 'kreeg 504'),
        ('484, 485, 486, 487, 488, 489, 490]', '484, 485, 486, 487, 488, 489, 490, 491]'),
    ],
)

build(
    'create-five-hundred-eighteen-minimal.py',
    'create-five-hundred-nineteen-minimal.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('!= 503', '!= 504'),
        ('kreeg 503', 'kreeg 504'),
        (' 444)', ' 445)'),
        ('484, 485, 486, 487, 488, 489, 490]', '484, 485, 486, 487, 488, 489, 490, 491]'),
    ],
)

build(
    'make-five-hundred-eighteen.py',
    'make-five-hundred-nineteen.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('all_cases[:503]', 'all_cases[:504]'),
        ('{UNKNOWN, TYPO}][:503]', '{UNKNOWN, TYPO}][:504]'),
        ('!= 503', '!= 504'),
        ('424, 425, 426, 427, 428, 429, 430]', '424, 425, 426, 427, 428, 429, 430, 431]'),
    ],
)

build(
    'create-five-hundred-eighteen-files.py',
    'create-five-hundred-nineteen-files.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('all_cases[:503]', 'all_cases[:504]'),
        ('{UNKNOWN, TYPO}][:503]', '{UNKNOWN, TYPO}][:504]'),
        ('!= 503', '!= 504'),
        ('424, 425, 426, 427, 428, 429, 430]', '424, 425, 426, 427, 428, 429, 430, 431]'),
    ],
)

build(
    'create-five-hundred-eighteen.py',
    'create-five-hundred-nineteen.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('all_cases[:503]', 'all_cases[:504]'),
        ('{UNKNOWN, TYPO}][:503]', '{UNKNOWN, TYPO}][:504]'),
        ('!= 503', '!= 504'),
        ('428, 429, 430, 431, 432, 433]', '428, 429, 430, 431, 432, 433, 434]'),
    ],
)

build(
    'generate-validate-five-hundred-eighteen.py',
    'generate-validate-five-hundred-nineteen.py',
    [
        ('five-hundred-eighteen', 'five-hundred-nineteen'),
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('all_cases[:503]', 'all_cases[:504]'),
        ('{UNKNOWN, TYPO}][:503]', '{UNKNOWN, TYPO}][:504]'),
        ('!= 503', '!= 504'),
        ('424, 425, 426, 427, 428, 429, 430]', '424, 425, 426, 427, 428, 429, 430, 431]'),
    ],
)

build(
    'validate-five-hundred-eighteen-valid-list-cases.py',
    'validate-five-hundred-nineteen-valid-list-cases.py',
    [
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('486, 487, 488, 489, 490, 491, 492]', '486, 487, 488, 489, 490, 491, 492, 493]'),
        ('all_cases[:503]', 'all_cases[:504]'),
        ('len(valid_cases) != 503', 'len(valid_cases) != 504'),
    ],
)

build(
    'validate-five-hundred-eighteen-valid-mixed.py',
    'validate-five-hundred-nineteen-valid-mixed.py',
    [
        ('vijfhonderdachttien', 'vijfhonderdnegentien'),
        ('486, 487, 488, 489, 490, 491, 492]', '486, 487, 488, 489, 490, 491, 492, 493]'),
        ('][:503]', '][:504]'),
        ('len(valid_cases) != 503', 'len(valid_cases) != 504'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighteen.py').read_text()
verify_text = verify_src.replace('five-hundred-eighteen', 'five-hundred-nineteen')
(ROOT / 'verify-five-hundred-nineteen.py').write_text(verify_text)
print('verify-five-hundred-nineteen.py')
