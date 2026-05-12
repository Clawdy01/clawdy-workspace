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
    'create-five-hundred-twenty-seven-assets.py',
    'create-five-hundred-twenty-eight-assets.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('[:512]', '[:513]'),
        ('!= 512', '!= 513'),
        ('kreeg 512', 'kreeg 513'),
        ('498, 499, 500, 501, 502, 503', '498, 499, 500, 501, 502, 503, 504'),
    ],
)

build(
    'create-five-hundred-twenty-seven-bootstrap.py',
    'create-five-hundred-twenty-eight-bootstrap.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('all_cases[:512]', 'all_cases[:513]'),
        ('{UNKNOWN, TYPO}][:512]', '{UNKNOWN, TYPO}][:513]'),
        ('!= 512', '!= 513'),
        ('kreeg 512', 'kreeg 513'),
        ('494, 495, 496, 497, 498, 499', '494, 495, 496, 497, 498, 499, 500'),
    ],
)

build(
    'create-five-hundred-twenty-seven-minimal.py',
    'create-five-hundred-twenty-eight-minimal.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('!= 512', '!= 513'),
        ('kreeg 512', 'kreeg 513'),
        (' 453)', ' 454)'),
        ('494, 495, 496, 497, 498, 499', '494, 495, 496, 497, 498, 499, 500'),
    ],
)

build(
    'make-five-hundred-twenty-seven.py',
    'make-five-hundred-twenty-eight.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('all_cases[:512]', 'all_cases[:513]'),
        ('{UNKNOWN, TYPO}][:512]', '{UNKNOWN, TYPO}][:513]'),
        ('!= 512', '!= 513'),
        ('434, 435, 436, 437, 438, 439', '434, 435, 436, 437, 438, 439, 440'),
    ],
)

build(
    'create-five-hundred-twenty-seven-files.py',
    'create-five-hundred-twenty-eight-files.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('all_cases[:512]', 'all_cases[:513]'),
        ('{UNKNOWN, TYPO}][:512]', '{UNKNOWN, TYPO}][:513]'),
        ('!= 512', '!= 513'),
        ('434, 435, 436, 437, 438, 439', '434, 435, 436, 437, 438, 439, 440'),
    ],
)

build(
    'create-five-hundred-twenty-seven.py',
    'create-five-hundred-twenty-eight.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('all_cases[:512]', 'all_cases[:513]'),
        ('{UNKNOWN, TYPO}][:512]', '{UNKNOWN, TYPO}][:513]'),
        ('!= 512', '!= 513'),
        ('437, 438, 439, 440, 441, 442', '437, 438, 439, 440, 441, 442, 443'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-seven.py',
    'generate-validate-five-hundred-twenty-eight.py',
    [
        ('five-hundred-twenty-seven', 'five-hundred-twenty-eight'),
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('all_cases[:512]', 'all_cases[:513]'),
        ('{UNKNOWN, TYPO}][:512]', '{UNKNOWN, TYPO}][:513]'),
        ('!= 512', '!= 513'),
        ('434, 435, 436, 437, 438, 439', '434, 435, 436, 437, 438, 439, 440'),
    ],
)

build(
    'validate-five-hundred-twenty-seven-valid-list-cases.py',
    'validate-five-hundred-twenty-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('497, 498, 499, 500, 501', '497, 498, 499, 500, 501, 502'),
        ('all_cases[:512]', 'all_cases[:513]'),
        ('len(valid_cases) != 512', 'len(valid_cases) != 513'),
    ],
)

build(
    'validate-five-hundred-twenty-seven-valid-mixed.py',
    'validate-five-hundred-twenty-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenentwintig', 'vijfhonderdachtentwintig'),
        ('497, 498, 499, 500, 501', '497, 498, 499, 500, 501, 502'),
        ('][:512]', '][:513]'),
        ('len(valid_cases) != 512', 'len(valid_cases) != 513'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-seven', 'five-hundred-twenty-eight')
(ROOT / 'verify-five-hundred-twenty-eight.py').write_text(verify_text)
print('verify-five-hundred-twenty-eight.py')
