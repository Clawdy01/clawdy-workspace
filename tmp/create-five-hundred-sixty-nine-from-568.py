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
    'create-five-hundred-sixty-eight-assets.py',
    'create-five-hundred-sixty-nine-assets.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('[:553]', '[:554]'),
        ('!= 553', '!= 554'),
        ('kreeg 553', 'kreeg 554'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'create-five-hundred-sixty-eight-bootstrap.py',
    'create-five-hundred-sixty-nine-bootstrap.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('all_cases[:553]', 'all_cases[:554]'),
        ('{UNKNOWN, TYPO}][:553]', '{UNKNOWN, TYPO}][:554]'),
        ('!= 553', '!= 554'),
        ('kreeg 553', 'kreeg 554'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'create-five-hundred-sixty-eight-minimal.py',
    'create-five-hundred-sixty-nine-minimal.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('!= 553', '!= 554'),
        ('kreeg 553', 'kreeg 554'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'make-five-hundred-sixty-eight.py',
    'make-five-hundred-sixty-nine.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('all_cases[:553]', 'all_cases[:554]'),
        ('{UNKNOWN, TYPO}][:553]', '{UNKNOWN, TYPO}][:554]'),
        ('!= 553', '!= 554'),
        ('476, 477, 478, 479, 480', '477, 478, 479, 480, 481'),
    ],
)

build(
    'create-five-hundred-sixty-eight-files.py',
    'create-five-hundred-sixty-nine-files.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('all_cases[:553]', 'all_cases[:554]'),
        ('{UNKNOWN, TYPO}][:553]', '{UNKNOWN, TYPO}][:554]'),
        ('!= 553', '!= 554'),
        ('476, 477, 478, 479, 480', '477, 478, 479, 480, 481'),
    ],
)

build(
    'create-five-hundred-sixty-eight.py',
    'create-five-hundred-sixty-nine.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('all_cases[:553]', 'all_cases[:554]'),
        ('{UNKNOWN, TYPO}][:553]', '{UNKNOWN, TYPO}][:554]'),
        ('!= 553', '!= 554'),
        ('479, 480, 481, 482, 483', '480, 481, 482, 483, 484'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-eight.py',
    'generate-validate-five-hundred-sixty-nine.py',
    [
        ('five-hundred-sixty-eight', 'five-hundred-sixty-nine'),
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('all_cases[:553]', 'all_cases[:554]'),
        ('{UNKNOWN, TYPO}][:553]', '{UNKNOWN, TYPO}][:554]'),
        ('!= 553', '!= 554'),
        ('476, 477, 478, 479, 480', '477, 478, 479, 480, 481'),
    ],
)

build(
    'validate-five-hundred-sixty-eight-valid-list-cases.py',
    'validate-five-hundred-sixty-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
        ('all_cases[:553]', 'all_cases[:554]'),
        ('len(valid_cases) != 553', 'len(valid_cases) != 554'),
    ],
)

build(
    'validate-five-hundred-sixty-eight-valid-mixed.py',
    'validate-five-hundred-sixty-nine-valid-mixed.py',
    [
        ('vijfhonderdachtenzestig', 'vijfhonderdnegenenzestig'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
        ('][:553]', '][:554]'),
        ('len(valid_cases) != 553', 'len(valid_cases) != 554'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-eight', 'five-hundred-sixty-nine')
(ROOT / 'verify-five-hundred-sixty-nine.py').write_text(verify_text)
print('verify-five-hundred-sixty-nine.py')
