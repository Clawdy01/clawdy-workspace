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
    'create-five-hundred-twenty-three-assets.py',
    'create-five-hundred-twenty-four-assets.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('[:508]', '[:509]'),
        ('!= 508', '!= 509'),
        ('kreeg 508', 'kreeg 509'),
        ('498, 499]', '498, 499, 500]'),
    ],
)

build(
    'create-five-hundred-twenty-three-bootstrap.py',
    'create-five-hundred-twenty-four-bootstrap.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('all_cases[:508]', 'all_cases[:509]'),
        ('{UNKNOWN, TYPO}][:508]', '{UNKNOWN, TYPO}][:509]'),
        ('!= 508', '!= 509'),
        ('kreeg 508', 'kreeg 509'),
        ('494, 495]', '494, 495, 496]'),
    ],
)

build(
    'create-five-hundred-twenty-three-minimal.py',
    'create-five-hundred-twenty-four-minimal.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('!= 508', '!= 509'),
        ('kreeg 508', 'kreeg 509'),
        (' 449)', ' 450)'),
        ('494, 495]', '494, 495, 496]'),
    ],
)

build(
    'make-five-hundred-twenty-three.py',
    'make-five-hundred-twenty-four.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('all_cases[:508]', 'all_cases[:509]'),
        ('{UNKNOWN, TYPO}][:508]', '{UNKNOWN, TYPO}][:509]'),
        ('!= 508', '!= 509'),
        ('434, 435]', '434, 435, 436]'),
    ],
)

build(
    'create-five-hundred-twenty-three-files.py',
    'create-five-hundred-twenty-four-files.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('all_cases[:508]', 'all_cases[:509]'),
        ('{UNKNOWN, TYPO}][:508]', '{UNKNOWN, TYPO}][:509]'),
        ('!= 508', '!= 509'),
        ('434, 435]', '434, 435, 436]'),
    ],
)

build(
    'create-five-hundred-twenty-three.py',
    'create-five-hundred-twenty-four.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('all_cases[:508]', 'all_cases[:509]'),
        ('{UNKNOWN, TYPO}][:508]', '{UNKNOWN, TYPO}][:509]'),
        ('!= 508', '!= 509'),
        ('437, 438]', '437, 438, 439]'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-three.py',
    'generate-validate-five-hundred-twenty-four.py',
    [
        ('five-hundred-twenty-three', 'five-hundred-twenty-four'),
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('all_cases[:508]', 'all_cases[:509]'),
        ('{UNKNOWN, TYPO}][:508]', '{UNKNOWN, TYPO}][:509]'),
        ('!= 508', '!= 509'),
        ('434, 435]', '434, 435, 436]'),
    ],
)

build(
    'validate-five-hundred-twenty-three-valid-list-cases.py',
    'validate-five-hundred-twenty-four-valid-list-cases.py',
    [
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('496, 497]', '496, 497, 498]'),
        ('all_cases[:508]', 'all_cases[:509]'),
        ('len(valid_cases) != 508', 'len(valid_cases) != 509'),
    ],
)

build(
    'validate-five-hundred-twenty-three-valid-mixed.py',
    'validate-five-hundred-twenty-four-valid-mixed.py',
    [
        ('vijfhonderddrieëntwintig', 'vijfhonderdvierentwintig'),
        ('496, 497]', '496, 497, 498]'),
        ('][:508]', '][:509]'),
        ('len(valid_cases) != 508', 'len(valid_cases) != 509'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-three.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-three', 'five-hundred-twenty-four')
(ROOT / 'verify-five-hundred-twenty-four.py').write_text(verify_text)
print('verify-five-hundred-twenty-four.py')
