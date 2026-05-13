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
    'create-five-hundred-sixty-nine-assets.py',
    'create-five-hundred-seventy-assets.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('[:554]', '[:555]'),
        ('!= 554', '!= 555'),
        ('kreeg 554', 'kreeg 555'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'create-five-hundred-sixty-nine-bootstrap.py',
    'create-five-hundred-seventy-bootstrap.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('all_cases[:554]', 'all_cases[:555]'),
        ('{UNKNOWN, TYPO}][:554]', '{UNKNOWN, TYPO}][:555]'),
        ('!= 554', '!= 555'),
        ('kreeg 554', 'kreeg 555'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'create-five-hundred-sixty-nine-minimal.py',
    'create-five-hundred-seventy-minimal.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('!= 554', '!= 555'),
        ('kreeg 554', 'kreeg 555'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'make-five-hundred-sixty-nine.py',
    'make-five-hundred-seventy.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('all_cases[:554]', 'all_cases[:555]'),
        ('{UNKNOWN, TYPO}][:554]', '{UNKNOWN, TYPO}][:555]'),
        ('!= 554', '!= 555'),
        ('477, 478, 479, 480, 481', '478, 479, 480, 481, 482'),
    ],
)

build(
    'create-five-hundred-sixty-nine-files.py',
    'create-five-hundred-seventy-files.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('all_cases[:554]', 'all_cases[:555]'),
        ('{UNKNOWN, TYPO}][:554]', '{UNKNOWN, TYPO}][:555]'),
        ('!= 554', '!= 555'),
        ('477, 478, 479, 480, 481', '478, 479, 480, 481, 482'),
    ],
)

build(
    'create-five-hundred-sixty-nine.py',
    'create-five-hundred-seventy.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('all_cases[:554]', 'all_cases[:555]'),
        ('{UNKNOWN, TYPO}][:554]', '{UNKNOWN, TYPO}][:555]'),
        ('!= 554', '!= 555'),
        ('480, 481, 482, 483, 484', '481, 482, 483, 484, 485'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-nine.py',
    'generate-validate-five-hundred-seventy.py',
    [
        ('five-hundred-sixty-nine', 'five-hundred-seventy'),
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('all_cases[:554]', 'all_cases[:555]'),
        ('{UNKNOWN, TYPO}][:554]', '{UNKNOWN, TYPO}][:555]'),
        ('!= 554', '!= 555'),
        ('477, 478, 479, 480, 481', '478, 479, 480, 481, 482'),
    ],
)

build(
    'validate-five-hundred-sixty-nine-valid-list-cases.py',
    'validate-five-hundred-seventy-valid-list-cases.py',
    [
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
        ('all_cases[:554]', 'all_cases[:555]'),
        ('len(valid_cases) != 554', 'len(valid_cases) != 555'),
    ],
)

build(
    'validate-five-hundred-sixty-nine-valid-mixed.py',
    'validate-five-hundred-seventy-valid-mixed.py',
    [
        ('vijfhonderdnegenenzestig', 'vijfhonderdzeventig'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
        ('][:554]', '][:555]'),
        ('len(valid_cases) != 554', 'len(valid_cases) != 555'),
        ('plain stderr noemt niet alle vierhonderdnegenennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvijfenvijftig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-nine', 'five-hundred-seventy')
(ROOT / 'verify-five-hundred-seventy.py').write_text(verify_text)
print('verify-five-hundred-seventy.py')
