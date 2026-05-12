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
    'create-five-hundred-twenty-eight-assets.py',
    'create-five-hundred-twenty-nine-assets.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('[:513]', '[:514]'),
        ('!= 513', '!= 514'),
        ('kreeg 513', 'kreeg 514'),
        ('498, 499, 500, 501, 502, 503, 504', '498, 499, 500, 501, 502, 503, 504, 505'),
    ],
)

build(
    'create-five-hundred-twenty-eight-bootstrap.py',
    'create-five-hundred-twenty-nine-bootstrap.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('all_cases[:513]', 'all_cases[:514]'),
        ('{UNKNOWN, TYPO}][:513]', '{UNKNOWN, TYPO}][:514]'),
        ('!= 513', '!= 514'),
        ('kreeg 513', 'kreeg 514'),
        ('494, 495, 496, 497, 498, 499, 500', '494, 495, 496, 497, 498, 499, 500, 501'),
    ],
)

build(
    'create-five-hundred-twenty-eight-minimal.py',
    'create-five-hundred-twenty-nine-minimal.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('!= 513', '!= 514'),
        ('kreeg 513', 'kreeg 514'),
        (' 454)', ' 455)'),
        ('494, 495, 496, 497, 498, 499, 500', '494, 495, 496, 497, 498, 499, 500, 501'),
    ],
)

build(
    'make-five-hundred-twenty-eight.py',
    'make-five-hundred-twenty-nine.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('all_cases[:513]', 'all_cases[:514]'),
        ('{UNKNOWN, TYPO}][:513]', '{UNKNOWN, TYPO}][:514]'),
        ('!= 513', '!= 514'),
        ('434, 435, 436, 437, 438, 439, 440', '434, 435, 436, 437, 438, 439, 440, 441'),
    ],
)

build(
    'create-five-hundred-twenty-eight-files.py',
    'create-five-hundred-twenty-nine-files.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('all_cases[:513]', 'all_cases[:514]'),
        ('{UNKNOWN, TYPO}][:513]', '{UNKNOWN, TYPO}][:514]'),
        ('!= 513', '!= 514'),
        ('434, 435, 436, 437, 438, 439, 440', '434, 435, 436, 437, 438, 439, 440, 441'),
    ],
)

build(
    'create-five-hundred-twenty-eight.py',
    'create-five-hundred-twenty-nine.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('all_cases[:513]', 'all_cases[:514]'),
        ('{UNKNOWN, TYPO}][:513]', '{UNKNOWN, TYPO}][:514]'),
        ('!= 513', '!= 514'),
        ('437, 438, 439, 440, 441, 442, 443', '437, 438, 439, 440, 441, 442, 443, 444'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-eight.py',
    'generate-validate-five-hundred-twenty-nine.py',
    [
        ('five-hundred-twenty-eight', 'five-hundred-twenty-nine'),
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('all_cases[:513]', 'all_cases[:514]'),
        ('{UNKNOWN, TYPO}][:513]', '{UNKNOWN, TYPO}][:514]'),
        ('!= 513', '!= 514'),
        ('434, 435, 436, 437, 438, 439, 440', '434, 435, 436, 437, 438, 439, 440, 441'),
    ],
)

build(
    'validate-five-hundred-twenty-eight-valid-list-cases.py',
    'validate-five-hundred-twenty-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('497, 498, 499, 500, 501, 502', '497, 498, 499, 500, 501, 502, 503'),
        ('all_cases[:513]', 'all_cases[:514]'),
        ('len(valid_cases) != 513', 'len(valid_cases) != 514'),
    ],
)

build(
    'validate-five-hundred-twenty-eight-valid-mixed.py',
    'validate-five-hundred-twenty-nine-valid-mixed.py',
    [
        ('vijfhonderdachtentwintig', 'vijfhonderdnegenentwintig'),
        ('497, 498, 499, 500, 501, 502', '497, 498, 499, 500, 501, 502, 503'),
        ('][:513]', '][:514]'),
        ('len(valid_cases) != 513', 'len(valid_cases) != 514'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-eight', 'five-hundred-twenty-nine')
(ROOT / 'verify-five-hundred-twenty-nine.py').write_text(verify_text)
print('verify-five-hundred-twenty-nine.py')
