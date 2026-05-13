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
    'create-five-hundred-fifty-seven-assets.py',
    'create-five-hundred-fifty-eight-assets.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('[:542]', '[:543]'),
        ('!= 542', '!= 543'),
        ('kreeg 542', 'kreeg 543'),
        ('529, 530, 531, 532, 533]', '530, 531, 532, 533, 534]'),
    ],
)

build(
    'create-five-hundred-fifty-seven-bootstrap.py',
    'create-five-hundred-fifty-eight-bootstrap.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('all_cases[:542]', 'all_cases[:543]'),
        ('{UNKNOWN, TYPO}][:542]', '{UNKNOWN, TYPO}][:543]'),
        ('!= 542', '!= 543'),
        ('kreeg 542', 'kreeg 543'),
        ('525, 526, 527, 528, 529]', '526, 527, 528, 529, 530]'),
    ],
)

build(
    'create-five-hundred-fifty-seven-minimal.py',
    'create-five-hundred-fifty-eight-minimal.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('!= 542', '!= 543'),
        ('kreeg 542', 'kreeg 543'),
        ('525, 526, 527, 528, 529]', '526, 527, 528, 529, 530]'),
    ],
)

build(
    'make-five-hundred-fifty-seven.py',
    'make-five-hundred-fifty-eight.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('all_cases[:542]', 'all_cases[:543]'),
        ('{UNKNOWN, TYPO}][:542]', '{UNKNOWN, TYPO}][:543]'),
        ('!= 542', '!= 543'),
        ('465, 466, 467, 468, 469]', '466, 467, 468, 469, 470]'),
    ],
)

build(
    'create-five-hundred-fifty-seven-files.py',
    'create-five-hundred-fifty-eight-files.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('all_cases[:542]', 'all_cases[:543]'),
        ('{UNKNOWN, TYPO}][:542]', '{UNKNOWN, TYPO}][:543]'),
        ('!= 542', '!= 543'),
        ('465, 466, 467, 468, 469]', '466, 467, 468, 469, 470]'),
    ],
)

build(
    'create-five-hundred-fifty-seven.py',
    'create-five-hundred-fifty-eight.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('all_cases[:542]', 'all_cases[:543]'),
        ('{UNKNOWN, TYPO}][:542]', '{UNKNOWN, TYPO}][:543]'),
        ('!= 542', '!= 543'),
        ('468, 469, 470, 471, 472]', '469, 470, 471, 472, 473]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-seven.py',
    'generate-validate-five-hundred-fifty-eight.py',
    [
        ('five-hundred-fifty-seven', 'five-hundred-fifty-eight'),
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('all_cases[:542]', 'all_cases[:543]'),
        ('{UNKNOWN, TYPO}][:542]', '{UNKNOWN, TYPO}][:543]'),
        ('!= 542', '!= 543'),
        ('465, 466, 467, 468, 469]', '466, 467, 468, 469, 470]'),
    ],
)

build(
    'validate-five-hundred-fifty-seven-valid-list-cases.py',
    'validate-five-hundred-fifty-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('527, 528, 529, 530, 531', '528, 529, 530, 531, 532'),
        ('all_cases[:542]', 'all_cases[:543]'),
        ('len(valid_cases) != 542', 'len(valid_cases) != 543'),
    ],
)

build(
    'validate-five-hundred-fifty-seven-valid-mixed.py',
    'validate-five-hundred-fifty-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenenvijftig', 'vijfhonderdachtenvijftig'),
        ('527, 528, 529, 530, 531', '528, 529, 530, 531, 532'),
        ('][:542]', '][:543]'),
        ('len(valid_cases) != 542', 'len(valid_cases) != 543'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-seven', 'five-hundred-fifty-eight')
(ROOT / 'verify-five-hundred-fifty-eight.py').write_text(verify_text)
print('verify-five-hundred-fifty-eight.py')
