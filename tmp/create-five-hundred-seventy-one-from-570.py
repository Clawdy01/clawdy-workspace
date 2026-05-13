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
    'create-five-hundred-seventy-assets.py',
    'create-five-hundred-seventy-one-assets.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('[:555]', '[:556]'),
        ('!= 555', '!= 556'),
        ('kreeg 555', 'kreeg 556'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'create-five-hundred-seventy-bootstrap.py',
    'create-five-hundred-seventy-one-bootstrap.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('all_cases[:555]', 'all_cases[:556]'),
        ('{UNKNOWN, TYPO}][:555]', '{UNKNOWN, TYPO}][:556]'),
        ('!= 555', '!= 556'),
        ('kreeg 555', 'kreeg 556'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'create-five-hundred-seventy-minimal.py',
    'create-five-hundred-seventy-one-minimal.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('!= 555', '!= 556'),
        ('kreeg 555', 'kreeg 556'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'make-five-hundred-seventy.py',
    'make-five-hundred-seventy-one.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('all_cases[:555]', 'all_cases[:556]'),
        ('{UNKNOWN, TYPO}][:555]', '{UNKNOWN, TYPO}][:556]'),
        ('!= 555', '!= 556'),
        ('478, 479, 480, 481, 482', '479, 480, 481, 482, 483'),
    ],
)

build(
    'create-five-hundred-seventy-files.py',
    'create-five-hundred-seventy-one-files.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('all_cases[:555]', 'all_cases[:556]'),
        ('{UNKNOWN, TYPO}][:555]', '{UNKNOWN, TYPO}][:556]'),
        ('!= 555', '!= 556'),
        ('478, 479, 480, 481, 482', '479, 480, 481, 482, 483'),
    ],
)

build(
    'create-five-hundred-seventy.py',
    'create-five-hundred-seventy-one.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('all_cases[:555]', 'all_cases[:556]'),
        ('{UNKNOWN, TYPO}][:555]', '{UNKNOWN, TYPO}][:556]'),
        ('!= 555', '!= 556'),
        ('481, 482, 483, 484, 485', '482, 483, 484, 485, 486'),
    ],
)

build(
    'generate-validate-five-hundred-seventy.py',
    'generate-validate-five-hundred-seventy-one.py',
    [
        ('five-hundred-seventy', 'five-hundred-seventy-one'),
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('all_cases[:555]', 'all_cases[:556]'),
        ('{UNKNOWN, TYPO}][:555]', '{UNKNOWN, TYPO}][:556]'),
        ('!= 555', '!= 556'),
        ('478, 479, 480, 481, 482', '479, 480, 481, 482, 483'),
    ],
)

build(
    'validate-five-hundred-seventy-valid-list-cases.py',
    'validate-five-hundred-seventy-one-valid-list-cases.py',
    [
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
        ('all_cases[:555]', 'all_cases[:556]'),
        ('len(valid_cases) != 555', 'len(valid_cases) != 556'),
    ],
)

build(
    'validate-five-hundred-seventy-valid-mixed.py',
    'validate-five-hundred-seventy-one-valid-mixed.py',
    [
        ('vijfhonderdzeventig', 'vijfhonderdeenenzeventig'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
        ('][:555]', '][:556]'),
        ('len(valid_cases) != 555', 'len(valid_cases) != 556'),
        ('plain stderr noemt niet alle vijfhonderdvijfenvijftig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzesenvijftig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy', 'five-hundred-seventy-one')
(ROOT / 'verify-five-hundred-seventy-one.py').write_text(verify_text)
print('verify-five-hundred-seventy-one.py')
