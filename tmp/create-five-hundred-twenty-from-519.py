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
    'create-five-hundred-nineteen-assets.py',
    'create-five-hundred-twenty-assets.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('[:504]', '[:505]'),
        ('!= 504', '!= 505'),
        ('kreeg 504', 'kreeg 505'),
        ('488, 489, 490, 491, 492, 493, 494, 495]', '488, 489, 490, 491, 492, 493, 494, 495, 496]'),
    ],
)

build(
    'create-five-hundred-nineteen-bootstrap.py',
    'create-five-hundred-twenty-bootstrap.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('all_cases[:504]', 'all_cases[:505]'),
        ('{UNKNOWN, TYPO}][:504]', '{UNKNOWN, TYPO}][:505]'),
        ('!= 504', '!= 505'),
        ('kreeg 504', 'kreeg 505'),
        ('484, 485, 486, 487, 488, 489, 490, 491]', '484, 485, 486, 487, 488, 489, 490, 491, 492]'),
    ],
)

build(
    'create-five-hundred-nineteen-minimal.py',
    'create-five-hundred-twenty-minimal.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('!= 504', '!= 505'),
        ('kreeg 504', 'kreeg 505'),
        (' 445)', ' 446)'),
        ('484, 485, 486, 487, 488, 489, 490, 491]', '484, 485, 486, 487, 488, 489, 490, 491, 492]'),
    ],
)

build(
    'make-five-hundred-nineteen.py',
    'make-five-hundred-twenty.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('all_cases[:504]', 'all_cases[:505]'),
        ('{UNKNOWN, TYPO}][:504]', '{UNKNOWN, TYPO}][:505]'),
        ('!= 504', '!= 505'),
        ('424, 425, 426, 427, 428, 429, 430, 431]', '424, 425, 426, 427, 428, 429, 430, 431, 432]'),
    ],
)

build(
    'create-five-hundred-nineteen-files.py',
    'create-five-hundred-twenty-files.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('all_cases[:504]', 'all_cases[:505]'),
        ('{UNKNOWN, TYPO}][:504]', '{UNKNOWN, TYPO}][:505]'),
        ('!= 504', '!= 505'),
        ('424, 425, 426, 427, 428, 429, 430, 431]', '424, 425, 426, 427, 428, 429, 430, 431, 432]'),
    ],
)

build(
    'create-five-hundred-nineteen.py',
    'create-five-hundred-twenty.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('all_cases[:504]', 'all_cases[:505]'),
        ('{UNKNOWN, TYPO}][:504]', '{UNKNOWN, TYPO}][:505]'),
        ('!= 504', '!= 505'),
        ('428, 429, 430, 431, 432, 433, 434]', '428, 429, 430, 431, 432, 433, 434, 435]'),
    ],
)

build(
    'generate-validate-five-hundred-nineteen.py',
    'generate-validate-five-hundred-twenty.py',
    [
        ('five-hundred-nineteen', 'five-hundred-twenty'),
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('all_cases[:504]', 'all_cases[:505]'),
        ('{UNKNOWN, TYPO}][:504]', '{UNKNOWN, TYPO}][:505]'),
        ('!= 504', '!= 505'),
        ('424, 425, 426, 427, 428, 429, 430, 431]', '424, 425, 426, 427, 428, 429, 430, 431, 432]'),
    ],
)

build(
    'validate-five-hundred-nineteen-valid-list-cases.py',
    'validate-five-hundred-twenty-valid-list-cases.py',
    [
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('486, 487, 488, 489, 490, 491, 492, 493]', '486, 487, 488, 489, 490, 491, 492, 493, 494]'),
        ('all_cases[:504]', 'all_cases[:505]'),
        ('len(valid_cases) != 504', 'len(valid_cases) != 505'),
    ],
)

build(
    'validate-five-hundred-nineteen-valid-mixed.py',
    'validate-five-hundred-twenty-valid-mixed.py',
    [
        ('vijfhonderdnegentien', 'vijfhonderdtwintig'),
        ('486, 487, 488, 489, 490, 491, 492, 493]', '486, 487, 488, 489, 490, 491, 492, 493, 494]'),
        ('][:504]', '][:505]'),
        ('len(valid_cases) != 504', 'len(valid_cases) != 505'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-nineteen.py').read_text()
verify_text = verify_src.replace('five-hundred-nineteen', 'five-hundred-twenty')
(ROOT / 'verify-five-hundred-twenty.py').write_text(verify_text)
print('verify-five-hundred-twenty.py')
