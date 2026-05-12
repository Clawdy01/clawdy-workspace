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
    'create-five-hundred-thirty-assets.py',
    'create-five-hundred-thirty-one-assets.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('[:515]', '[:516]'),
        ('!= 515', '!= 516'),
        ('kreeg 515', 'kreeg 516'),
        ('498, 499, 500, 501, 502, 503, 504, 505, 506', '498, 499, 500, 501, 502, 503, 504, 505, 506, 507'),
    ],
)

build(
    'create-five-hundred-thirty-bootstrap.py',
    'create-five-hundred-thirty-one-bootstrap.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('all_cases[:515]', 'all_cases[:516]'),
        ('{UNKNOWN, TYPO}][:515]', '{UNKNOWN, TYPO}][:516]'),
        ('!= 515', '!= 516'),
        ('kreeg 515', 'kreeg 516'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503'),
    ],
)

build(
    'create-five-hundred-thirty-minimal.py',
    'create-five-hundred-thirty-one-minimal.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('!= 515', '!= 516'),
        ('kreeg 515', 'kreeg 516'),
        (' 456)', ' 457)'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503'),
    ],
)

build(
    'make-five-hundred-thirty.py',
    'make-five-hundred-thirty-one.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('all_cases[:515]', 'all_cases[:516]'),
        ('{UNKNOWN, TYPO}][:515]', '{UNKNOWN, TYPO}][:516]'),
        ('!= 515', '!= 516'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443'),
    ],
)

build(
    'create-five-hundred-thirty-files.py',
    'create-five-hundred-thirty-one-files.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('all_cases[:515]', 'all_cases[:516]'),
        ('{UNKNOWN, TYPO}][:515]', '{UNKNOWN, TYPO}][:516]'),
        ('!= 515', '!= 516'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443'),
    ],
)

build(
    'create-five-hundred-thirty.py',
    'create-five-hundred-thirty-one.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('all_cases[:515]', 'all_cases[:516]'),
        ('{UNKNOWN, TYPO}][:515]', '{UNKNOWN, TYPO}][:516]'),
        ('!= 515', '!= 516'),
        ('437, 438, 439, 440, 441, 442, 443, 444, 445', '437, 438, 439, 440, 441, 442, 443, 444, 445, 446'),
    ],
)

build(
    'generate-validate-five-hundred-thirty.py',
    'generate-validate-five-hundred-thirty-one.py',
    [
        ('five-hundred-thirty', 'five-hundred-thirty-one'),
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('all_cases[:515]', 'all_cases[:516]'),
        ('{UNKNOWN, TYPO}][:515]', '{UNKNOWN, TYPO}][:516]'),
        ('!= 515', '!= 516'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443'),
    ],
)

build(
    'validate-five-hundred-thirty-valid-list-cases.py',
    'validate-five-hundred-thirty-one-valid-list-cases.py',
    [
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504', '497, 498, 499, 500, 501, 502, 503, 504, 505'),
        ('all_cases[:515]', 'all_cases[:516]'),
        ('len(valid_cases) != 515', 'len(valid_cases) != 516'),
    ],
)

build(
    'validate-five-hundred-thirty-valid-mixed.py',
    'validate-five-hundred-thirty-one-valid-mixed.py',
    [
        ('vijfhonderddertig', 'vijfhonderdeenendertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504', '497, 498, 499, 500, 501, 502, 503, 504, 505'),
        ('][:515]', '][:516]'),
        ('len(valid_cases) != 515', 'len(valid_cases) != 516'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty', 'five-hundred-thirty-one')
(ROOT / 'verify-five-hundred-thirty-one.py').write_text(verify_text)
print('verify-five-hundred-thirty-one.py')
