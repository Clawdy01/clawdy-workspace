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
    'create-five-hundred-thirty-one-assets.py',
    'create-five-hundred-thirty-two-assets.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('[:516]', '[:517]'),
        ('!= 516', '!= 517'),
        ('kreeg 516', 'kreeg 517'),
        ('498, 499, 500, 501, 502, 503, 504, 505, 506, 507', '498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508'),
    ],
)

build(
    'create-five-hundred-thirty-one-bootstrap.py',
    'create-five-hundred-thirty-two-bootstrap.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('all_cases[:516]', 'all_cases[:517]'),
        ('{UNKNOWN, TYPO}][:516]', '{UNKNOWN, TYPO}][:517]'),
        ('!= 516', '!= 517'),
        ('kreeg 516', 'kreeg 517'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504'),
    ],
)

build(
    'create-five-hundred-thirty-one-minimal.py',
    'create-five-hundred-thirty-two-minimal.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('!= 516', '!= 517'),
        ('kreeg 516', 'kreeg 517'),
        (' 457)', ' 458)'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504'),
    ],
)

build(
    'make-five-hundred-thirty-one.py',
    'make-five-hundred-thirty-two.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('all_cases[:516]', 'all_cases[:517]'),
        ('{UNKNOWN, TYPO}][:516]', '{UNKNOWN, TYPO}][:517]'),
        ('!= 516', '!= 517'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444'),
    ],
)

build(
    'create-five-hundred-thirty-one-files.py',
    'create-five-hundred-thirty-two-files.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('all_cases[:516]', 'all_cases[:517]'),
        ('{UNKNOWN, TYPO}][:516]', '{UNKNOWN, TYPO}][:517]'),
        ('!= 516', '!= 517'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444'),
    ],
)

build(
    'create-five-hundred-thirty-one.py',
    'create-five-hundred-thirty-two.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('all_cases[:516]', 'all_cases[:517]'),
        ('{UNKNOWN, TYPO}][:516]', '{UNKNOWN, TYPO}][:517]'),
        ('!= 516', '!= 517'),
        ('437, 438, 439, 440, 441, 442, 443, 444, 445, 446', '437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-one.py',
    'generate-validate-five-hundred-thirty-two.py',
    [
        ('five-hundred-thirty-one', 'five-hundred-thirty-two'),
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('all_cases[:516]', 'all_cases[:517]'),
        ('{UNKNOWN, TYPO}][:516]', '{UNKNOWN, TYPO}][:517]'),
        ('!= 516', '!= 517'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444'),
    ],
)

build(
    'validate-five-hundred-thirty-one-valid-list-cases.py',
    'validate-five-hundred-thirty-two-valid-list-cases.py',
    [
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506'),
        ('all_cases[:516]', 'all_cases[:517]'),
        ('len(valid_cases) != 516', 'len(valid_cases) != 517'),
    ],
)

build(
    'validate-five-hundred-thirty-one-valid-mixed.py',
    'validate-five-hundred-thirty-two-valid-mixed.py',
    [
        ('vijfhonderdeenendertig', 'vijfhonderdtweeëndertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506'),
        ('][:516]', '][:517]'),
        ('len(valid_cases) != 516', 'len(valid_cases) != 517'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-one.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-one', 'five-hundred-thirty-two')
(ROOT / 'verify-five-hundred-thirty-two.py').write_text(verify_text)
print('verify-five-hundred-thirty-two.py')
