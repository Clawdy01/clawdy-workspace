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
    'create-five-hundred-twenty-nine-assets.py',
    'create-five-hundred-thirty-assets.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('[:514]', '[:515]'),
        ('!= 514', '!= 515'),
        ('kreeg 514', 'kreeg 515'),
        ('498, 499, 500, 501, 502, 503, 504, 505', '498, 499, 500, 501, 502, 503, 504, 505, 506'),
    ],
)

build(
    'create-five-hundred-twenty-nine-bootstrap.py',
    'create-five-hundred-thirty-bootstrap.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('all_cases[:514]', 'all_cases[:515]'),
        ('{UNKNOWN, TYPO}][:514]', '{UNKNOWN, TYPO}][:515]'),
        ('!= 514', '!= 515'),
        ('kreeg 514', 'kreeg 515'),
        ('494, 495, 496, 497, 498, 499, 500, 501', '494, 495, 496, 497, 498, 499, 500, 501, 502'),
    ],
)

build(
    'create-five-hundred-twenty-nine-minimal.py',
    'create-five-hundred-thirty-minimal.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('!= 514', '!= 515'),
        ('kreeg 514', 'kreeg 515'),
        (' 455)', ' 456)'),
        ('494, 495, 496, 497, 498, 499, 500, 501', '494, 495, 496, 497, 498, 499, 500, 501, 502'),
    ],
)

build(
    'make-five-hundred-twenty-nine.py',
    'make-five-hundred-thirty.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('all_cases[:514]', 'all_cases[:515]'),
        ('{UNKNOWN, TYPO}][:514]', '{UNKNOWN, TYPO}][:515]'),
        ('!= 514', '!= 515'),
        ('434, 435, 436, 437, 438, 439, 440, 441', '434, 435, 436, 437, 438, 439, 440, 441, 442'),
    ],
)

build(
    'create-five-hundred-twenty-nine-files.py',
    'create-five-hundred-thirty-files.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('all_cases[:514]', 'all_cases[:515]'),
        ('{UNKNOWN, TYPO}][:514]', '{UNKNOWN, TYPO}][:515]'),
        ('!= 514', '!= 515'),
        ('434, 435, 436, 437, 438, 439, 440, 441', '434, 435, 436, 437, 438, 439, 440, 441, 442'),
    ],
)

build(
    'create-five-hundred-twenty-nine.py',
    'create-five-hundred-thirty.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('all_cases[:514]', 'all_cases[:515]'),
        ('{UNKNOWN, TYPO}][:514]', '{UNKNOWN, TYPO}][:515]'),
        ('!= 514', '!= 515'),
        ('437, 438, 439, 440, 441, 442, 443, 444', '437, 438, 439, 440, 441, 442, 443, 444, 445'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-nine.py',
    'generate-validate-five-hundred-thirty.py',
    [
        ('five-hundred-twenty-nine', 'five-hundred-thirty'),
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('all_cases[:514]', 'all_cases[:515]'),
        ('{UNKNOWN, TYPO}][:514]', '{UNKNOWN, TYPO}][:515]'),
        ('!= 514', '!= 515'),
        ('434, 435, 436, 437, 438, 439, 440, 441', '434, 435, 436, 437, 438, 439, 440, 441, 442'),
    ],
)

build(
    'validate-five-hundred-twenty-nine-valid-list-cases.py',
    'validate-five-hundred-thirty-valid-list-cases.py',
    [
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('497, 498, 499, 500, 501, 502, 503', '497, 498, 499, 500, 501, 502, 503, 504'),
        ('all_cases[:514]', 'all_cases[:515]'),
        ('len(valid_cases) != 514', 'len(valid_cases) != 515'),
    ],
)

build(
    'validate-five-hundred-twenty-nine-valid-mixed.py',
    'validate-five-hundred-thirty-valid-mixed.py',
    [
        ('vijfhonderdnegenentwintig', 'vijfhonderddertig'),
        ('497, 498, 499, 500, 501, 502, 503', '497, 498, 499, 500, 501, 502, 503, 504'),
        ('][:514]', '][:515]'),
        ('len(valid_cases) != 514', 'len(valid_cases) != 515'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-nine', 'five-hundred-thirty')
(ROOT / 'verify-five-hundred-thirty.py').write_text(verify_text)
print('verify-five-hundred-thirty.py')
