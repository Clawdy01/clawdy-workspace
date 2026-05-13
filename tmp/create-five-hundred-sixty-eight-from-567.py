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
    'create-five-hundred-sixty-seven-assets.py',
    'create-five-hundred-sixty-eight-assets.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('[:552]', '[:553]'),
        ('!= 552', '!= 553'),
        ('kreeg 552', 'kreeg 553'),
        ('539, 540, 541, 542, 543', '540, 541, 542, 543, 544'),
    ],
)

build(
    'create-five-hundred-sixty-seven-bootstrap.py',
    'create-five-hundred-sixty-eight-bootstrap.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('all_cases[:552]', 'all_cases[:553]'),
        ('{UNKNOWN, TYPO}][:552]', '{UNKNOWN, TYPO}][:553]'),
        ('!= 552', '!= 553'),
        ('kreeg 552', 'kreeg 553'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'create-five-hundred-sixty-seven-minimal.py',
    'create-five-hundred-sixty-eight-minimal.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('!= 552', '!= 553'),
        ('kreeg 552', 'kreeg 553'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'make-five-hundred-sixty-seven.py',
    'make-five-hundred-sixty-eight.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('all_cases[:552]', 'all_cases[:553]'),
        ('{UNKNOWN, TYPO}][:552]', '{UNKNOWN, TYPO}][:553]'),
        ('!= 552', '!= 553'),
        ('475, 476, 477, 478, 479', '476, 477, 478, 479, 480'),
    ],
)

build(
    'create-five-hundred-sixty-seven-files.py',
    'create-five-hundred-sixty-eight-files.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('all_cases[:552]', 'all_cases[:553]'),
        ('{UNKNOWN, TYPO}][:552]', '{UNKNOWN, TYPO}][:553]'),
        ('!= 552', '!= 553'),
        ('475, 476, 477, 478, 479', '476, 477, 478, 479, 480'),
    ],
)

build(
    'create-five-hundred-sixty-seven.py',
    'create-five-hundred-sixty-eight.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('all_cases[:552]', 'all_cases[:553]'),
        ('{UNKNOWN, TYPO}][:552]', '{UNKNOWN, TYPO}][:553]'),
        ('!= 552', '!= 553'),
        ('478, 479, 480, 481, 482', '479, 480, 481, 482, 483'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-seven.py',
    'generate-validate-five-hundred-sixty-eight.py',
    [
        ('five-hundred-sixty-seven', 'five-hundred-sixty-eight'),
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('all_cases[:552]', 'all_cases[:553]'),
        ('{UNKNOWN, TYPO}][:552]', '{UNKNOWN, TYPO}][:553]'),
        ('!= 552', '!= 553'),
        ('475, 476, 477, 478, 479', '476, 477, 478, 479, 480'),
    ],
)

build(
    'validate-five-hundred-sixty-seven-valid-list-cases.py',
    'validate-five-hundred-sixty-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
        ('all_cases[:552]', 'all_cases[:553]'),
        ('len(valid_cases) != 552', 'len(valid_cases) != 553'),
    ],
)

build(
    'validate-five-hundred-sixty-seven-valid-mixed.py',
    'validate-five-hundred-sixty-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenenzestig', 'vijfhonderdachtenzestig'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
        ('][:552]', '][:553]'),
        ('len(valid_cases) != 552', 'len(valid_cases) != 553'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-seven', 'five-hundred-sixty-eight')
(ROOT / 'verify-five-hundred-sixty-eight.py').write_text(verify_text)
print('verify-five-hundred-sixty-eight.py')
