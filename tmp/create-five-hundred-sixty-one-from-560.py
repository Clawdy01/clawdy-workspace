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
    'create-five-hundred-sixty-assets.py',
    'create-five-hundred-sixty-one-assets.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('[:545]', '[:546]'),
        ('!= 545', '!= 546'),
        ('kreeg 545', 'kreeg 546'),
        ('532, 533, 534, 535, 536]', '533, 534, 535, 536, 537]'),
    ],
)

build(
    'create-five-hundred-sixty-bootstrap.py',
    'create-five-hundred-sixty-one-bootstrap.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('all_cases[:545]', 'all_cases[:546]'),
        ('{UNKNOWN, TYPO}][:545]', '{UNKNOWN, TYPO}][:546]'),
        ('!= 545', '!= 546'),
        ('kreeg 545', 'kreeg 546'),
        ('528, 529, 530, 531, 532]', '529, 530, 531, 532, 533]'),
    ],
)

build(
    'create-five-hundred-sixty-minimal.py',
    'create-five-hundred-sixty-one-minimal.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('!= 545', '!= 546'),
        ('kreeg 545', 'kreeg 546'),
        ('528, 529, 530, 531, 532]', '529, 530, 531, 532, 533]'),
    ],
)

build(
    'make-five-hundred-sixty.py',
    'make-five-hundred-sixty-one.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('all_cases[:545]', 'all_cases[:546]'),
        ('{UNKNOWN, TYPO}][:545]', '{UNKNOWN, TYPO}][:546]'),
        ('!= 545', '!= 546'),
        ('468, 469, 470, 471, 472]', '469, 470, 471, 472, 473]'),
    ],
)

build(
    'create-five-hundred-sixty-files.py',
    'create-five-hundred-sixty-one-files.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('all_cases[:545]', 'all_cases[:546]'),
        ('{UNKNOWN, TYPO}][:545]', '{UNKNOWN, TYPO}][:546]'),
        ('!= 545', '!= 546'),
        ('468, 469, 470, 471, 472]', '469, 470, 471, 472, 473]'),
    ],
)

build(
    'create-five-hundred-sixty.py',
    'create-five-hundred-sixty-one.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('all_cases[:545]', 'all_cases[:546]'),
        ('{UNKNOWN, TYPO}][:545]', '{UNKNOWN, TYPO}][:546]'),
        ('!= 545', '!= 546'),
        ('471, 472, 473, 474, 475]', '472, 473, 474, 475, 476]'),
    ],
)

build(
    'generate-validate-five-hundred-sixty.py',
    'generate-validate-five-hundred-sixty-one.py',
    [
        ('five-hundred-sixty', 'five-hundred-sixty-one'),
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('all_cases[:545]', 'all_cases[:546]'),
        ('{UNKNOWN, TYPO}][:545]', '{UNKNOWN, TYPO}][:546]'),
        ('!= 545', '!= 546'),
        ('468, 469, 470, 471, 472]', '469, 470, 471, 472, 473]'),
    ],
)

build(
    'validate-five-hundred-sixty-valid-list-cases.py',
    'validate-five-hundred-sixty-one-valid-list-cases.py',
    [
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
        ('all_cases[:545]', 'all_cases[:546]'),
        ('len(valid_cases) != 545', 'len(valid_cases) != 546'),
    ],
)

build(
    'validate-five-hundred-sixty-valid-mixed.py',
    'validate-five-hundred-sixty-one-valid-mixed.py',
    [
        ('vijfhonderdzestig', 'vijfhonderdeenenzestig'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
        ('][:545]', '][:546]'),
        ('len(valid_cases) != 545', 'len(valid_cases) != 546'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty', 'five-hundred-sixty-one')
(ROOT / 'verify-five-hundred-sixty-one.py').write_text(verify_text)
print('verify-five-hundred-sixty-one.py')
