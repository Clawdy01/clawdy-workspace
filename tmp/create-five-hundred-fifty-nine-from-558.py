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
    'create-five-hundred-fifty-eight-assets.py',
    'create-five-hundred-fifty-nine-assets.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('[:543]', '[:544]'),
        ('!= 543', '!= 544'),
        ('kreeg 543', 'kreeg 544'),
        ('530, 531, 532, 533, 534]', '531, 532, 533, 534, 535]'),
    ],
)

build(
    'create-five-hundred-fifty-eight-bootstrap.py',
    'create-five-hundred-fifty-nine-bootstrap.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('all_cases[:543]', 'all_cases[:544]'),
        ('{UNKNOWN, TYPO}][:543]', '{UNKNOWN, TYPO}][:544]'),
        ('!= 543', '!= 544'),
        ('kreeg 543', 'kreeg 544'),
        ('526, 527, 528, 529, 530]', '527, 528, 529, 530, 531]'),
    ],
)

build(
    'create-five-hundred-fifty-eight-minimal.py',
    'create-five-hundred-fifty-nine-minimal.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('!= 543', '!= 544'),
        ('kreeg 543', 'kreeg 544'),
        ('526, 527, 528, 529, 530]', '527, 528, 529, 530, 531]'),
    ],
)

build(
    'make-five-hundred-fifty-eight.py',
    'make-five-hundred-fifty-nine.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('all_cases[:543]', 'all_cases[:544]'),
        ('{UNKNOWN, TYPO}][:543]', '{UNKNOWN, TYPO}][:544]'),
        ('!= 543', '!= 544'),
        ('466, 467, 468, 469, 470]', '467, 468, 469, 470, 471]'),
    ],
)

build(
    'create-five-hundred-fifty-eight-files.py',
    'create-five-hundred-fifty-nine-files.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('all_cases[:543]', 'all_cases[:544]'),
        ('{UNKNOWN, TYPO}][:543]', '{UNKNOWN, TYPO}][:544]'),
        ('!= 543', '!= 544'),
        ('466, 467, 468, 469, 470]', '467, 468, 469, 470, 471]'),
    ],
)

build(
    'create-five-hundred-fifty-eight.py',
    'create-five-hundred-fifty-nine.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('all_cases[:543]', 'all_cases[:544]'),
        ('{UNKNOWN, TYPO}][:543]', '{UNKNOWN, TYPO}][:544]'),
        ('!= 543', '!= 544'),
        ('469, 470, 471, 472, 473]', '470, 471, 472, 473, 474]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-eight.py',
    'generate-validate-five-hundred-fifty-nine.py',
    [
        ('five-hundred-fifty-eight', 'five-hundred-fifty-nine'),
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('all_cases[:543]', 'all_cases[:544]'),
        ('{UNKNOWN, TYPO}][:543]', '{UNKNOWN, TYPO}][:544]'),
        ('!= 543', '!= 544'),
        ('466, 467, 468, 469, 470]', '467, 468, 469, 470, 471]'),
    ],
)

build(
    'validate-five-hundred-fifty-eight-valid-list-cases.py',
    'validate-five-hundred-fifty-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('528, 529, 530, 531, 532', '529, 530, 531, 532, 533'),
        ('all_cases[:543]', 'all_cases[:544]'),
        ('len(valid_cases) != 543', 'len(valid_cases) != 544'),
    ],
)

build(
    'validate-five-hundred-fifty-eight-valid-mixed.py',
    'validate-five-hundred-fifty-nine-valid-mixed.py',
    [
        ('vijfhonderdachtenvijftig', 'vijfhonderdnegenenvijftig'),
        ('528, 529, 530, 531, 532', '529, 530, 531, 532, 533'),
        ('][:543]', '][:544]'),
        ('len(valid_cases) != 543', 'len(valid_cases) != 544'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-eight', 'five-hundred-fifty-nine')
(ROOT / 'verify-five-hundred-fifty-nine.py').write_text(verify_text)
print('verify-five-hundred-fifty-nine.py')
