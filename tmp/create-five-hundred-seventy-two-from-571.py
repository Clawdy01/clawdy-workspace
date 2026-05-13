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
    'create-five-hundred-seventy-one-assets.py',
    'create-five-hundred-seventy-two-assets.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('[:556]', '[:557]'),
        ('!= 556', '!= 557'),
        ('kreeg 556', 'kreeg 557'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'create-five-hundred-seventy-one-bootstrap.py',
    'create-five-hundred-seventy-two-bootstrap.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('all_cases[:556]', 'all_cases[:557]'),
        ('{UNKNOWN, TYPO}][:556]', '{UNKNOWN, TYPO}][:557]'),
        ('!= 556', '!= 557'),
        ('kreeg 556', 'kreeg 557'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'create-five-hundred-seventy-one-minimal.py',
    'create-five-hundred-seventy-two-minimal.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('!= 556', '!= 557'),
        ('kreeg 556', 'kreeg 557'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'make-five-hundred-seventy-one.py',
    'make-five-hundred-seventy-two.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('all_cases[:556]', 'all_cases[:557]'),
        ('{UNKNOWN, TYPO}][:556]', '{UNKNOWN, TYPO}][:557]'),
        ('!= 556', '!= 557'),
        ('479, 480, 481, 482, 483', '480, 481, 482, 483, 484'),
    ],
)

build(
    'create-five-hundred-seventy-one-files.py',
    'create-five-hundred-seventy-two-files.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('all_cases[:556]', 'all_cases[:557]'),
        ('{UNKNOWN, TYPO}][:556]', '{UNKNOWN, TYPO}][:557]'),
        ('!= 556', '!= 557'),
        ('479, 480, 481, 482, 483', '480, 481, 482, 483, 484'),
    ],
)

build(
    'create-five-hundred-seventy-one.py',
    'create-five-hundred-seventy-two.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('all_cases[:556]', 'all_cases[:557]'),
        ('{UNKNOWN, TYPO}][:556]', '{UNKNOWN, TYPO}][:557]'),
        ('!= 556', '!= 557'),
        ('482, 483, 484, 485, 486', '483, 484, 485, 486, 487'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-one.py',
    'generate-validate-five-hundred-seventy-two.py',
    [
        ('five-hundred-seventy-one', 'five-hundred-seventy-two'),
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('all_cases[:556]', 'all_cases[:557]'),
        ('{UNKNOWN, TYPO}][:556]', '{UNKNOWN, TYPO}][:557]'),
        ('!= 556', '!= 557'),
        ('479, 480, 481, 482, 483', '480, 481, 482, 483, 484'),
    ],
)

build(
    'validate-five-hundred-seventy-one-valid-list-cases.py',
    'validate-five-hundred-seventy-two-valid-list-cases.py',
    [
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
        ('all_cases[:556]', 'all_cases[:557]'),
        ('len(valid_cases) != 556', 'len(valid_cases) != 557'),
    ],
)

build(
    'validate-five-hundred-seventy-one-valid-mixed.py',
    'validate-five-hundred-seventy-two-valid-mixed.py',
    [
        ('vijfhonderdeenenzeventig', 'vijfhonderdtweeënzeventig'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
        ('][:556]', '][:557]'),
        ('len(valid_cases) != 556', 'len(valid_cases) != 557'),
        ('plain stderr noemt niet alle vijfhonderdzesenvijftig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzevenenvijftig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-one.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-one', 'five-hundred-seventy-two')
(ROOT / 'verify-five-hundred-seventy-two.py').write_text(verify_text)
print('verify-five-hundred-seventy-two.py')
