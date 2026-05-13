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
    'create-five-hundred-fifty-five-assets.py',
    'create-five-hundred-fifty-six-assets.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('[:540]', '[:541]'),
        ('!= 540', '!= 541'),
        ('kreeg 540', 'kreeg 541'),
        ('527, 528, 529, 530, 531]', '528, 529, 530, 531, 532]'),
    ],
)

build(
    'create-five-hundred-fifty-five-bootstrap.py',
    'create-five-hundred-fifty-six-bootstrap.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('all_cases[:540]', 'all_cases[:541]'),
        ('{UNKNOWN, TYPO}][:540]', '{UNKNOWN, TYPO}][:541]'),
        ('!= 540', '!= 541'),
        ('kreeg 540', 'kreeg 541'),
        ('523, 524, 525, 526, 527]', '524, 525, 526, 527, 528]'),
    ],
)

build(
    'create-five-hundred-fifty-five-minimal.py',
    'create-five-hundred-fifty-six-minimal.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('!= 540', '!= 541'),
        ('kreeg 540', 'kreeg 541'),
        ('523, 524, 525, 526, 527]', '524, 525, 526, 527, 528]'),
    ],
)

build(
    'make-five-hundred-fifty-five.py',
    'make-five-hundred-fifty-six.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('all_cases[:540]', 'all_cases[:541]'),
        ('{UNKNOWN, TYPO}][:540]', '{UNKNOWN, TYPO}][:541]'),
        ('!= 540', '!= 541'),
        ('463, 464, 465, 466, 467]', '464, 465, 466, 467, 468]'),
    ],
)

build(
    'create-five-hundred-fifty-five-files.py',
    'create-five-hundred-fifty-six-files.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('all_cases[:540]', 'all_cases[:541]'),
        ('{UNKNOWN, TYPO}][:540]', '{UNKNOWN, TYPO}][:541]'),
        ('!= 540', '!= 541'),
        ('463, 464, 465, 466, 467]', '464, 465, 466, 467, 468]'),
    ],
)

build(
    'create-five-hundred-fifty-five.py',
    'create-five-hundred-fifty-six.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('all_cases[:540]', 'all_cases[:541]'),
        ('{UNKNOWN, TYPO}][:540]', '{UNKNOWN, TYPO}][:541]'),
        ('!= 540', '!= 541'),
        ('466, 467, 468, 469, 470]', '467, 468, 469, 470, 471]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-five.py',
    'generate-validate-five-hundred-fifty-six.py',
    [
        ('five-hundred-fifty-five', 'five-hundred-fifty-six'),
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('all_cases[:540]', 'all_cases[:541]'),
        ('{UNKNOWN, TYPO}][:540]', '{UNKNOWN, TYPO}][:541]'),
        ('!= 540', '!= 541'),
        ('463, 464, 465, 466, 467]', '464, 465, 466, 467, 468]'),
    ],
)

build(
    'validate-five-hundred-fifty-five-valid-list-cases.py',
    'validate-five-hundred-fifty-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('525, 526, 527, 528, 529', '526, 527, 528, 529, 530'),
        ('all_cases[:540]', 'all_cases[:541]'),
        ('len(valid_cases) != 540', 'len(valid_cases) != 541'),
    ],
)

build(
    'validate-five-hundred-fifty-five-valid-mixed.py',
    'validate-five-hundred-fifty-six-valid-mixed.py',
    [
        ('vijfhonderdvijfenvijftig', 'vijfhonderdzesenvijftig'),
        ('525, 526, 527, 528, 529', '526, 527, 528, 529, 530'),
        ('][:540]', '][:541]'),
        ('len(valid_cases) != 540', 'len(valid_cases) != 541'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-five.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-five', 'five-hundred-fifty-six')
(ROOT / 'verify-five-hundred-fifty-six.py').write_text(verify_text)
print('verify-five-hundred-fifty-six.py')
