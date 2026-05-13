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
    'create-five-hundred-sixty-two-assets.py',
    'create-five-hundred-sixty-three-assets.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('[:547]', '[:548]'),
        ('!= 547', '!= 548'),
        ('kreeg 547', 'kreeg 548'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'create-five-hundred-sixty-two-bootstrap.py',
    'create-five-hundred-sixty-three-bootstrap.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('all_cases[:547]', 'all_cases[:548]'),
        ('{UNKNOWN, TYPO}][:547]', '{UNKNOWN, TYPO}][:548]'),
        ('!= 547', '!= 548'),
        ('kreeg 547', 'kreeg 548'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
    ],
)

build(
    'create-five-hundred-sixty-two-minimal.py',
    'create-five-hundred-sixty-three-minimal.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('!= 547', '!= 548'),
        ('kreeg 547', 'kreeg 548'),
        ('530, 531, 532, 533, 534', '531, 532, 533, 534, 535'),
    ],
)

build(
    'make-five-hundred-sixty-two.py',
    'make-five-hundred-sixty-three.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('all_cases[:547]', 'all_cases[:548]'),
        ('{UNKNOWN, TYPO}][:547]', '{UNKNOWN, TYPO}][:548]'),
        ('!= 547', '!= 548'),
        ('470, 471, 472, 473, 474', '471, 472, 473, 474, 475'),
    ],
)

build(
    'create-five-hundred-sixty-two-files.py',
    'create-five-hundred-sixty-three-files.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('all_cases[:547]', 'all_cases[:548]'),
        ('{UNKNOWN, TYPO}][:547]', '{UNKNOWN, TYPO}][:548]'),
        ('!= 547', '!= 548'),
        ('470, 471, 472, 473, 474', '471, 472, 473, 474, 475'),
    ],
)

build(
    'create-five-hundred-sixty-two.py',
    'create-five-hundred-sixty-three.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('all_cases[:547]', 'all_cases[:548]'),
        ('{UNKNOWN, TYPO}][:547]', '{UNKNOWN, TYPO}][:548]'),
        ('!= 547', '!= 548'),
        ('473, 474, 475, 476, 477', '474, 475, 476, 477, 478'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-two.py',
    'generate-validate-five-hundred-sixty-three.py',
    [
        ('five-hundred-sixty-two', 'five-hundred-sixty-three'),
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('all_cases[:547]', 'all_cases[:548]'),
        ('{UNKNOWN, TYPO}][:547]', '{UNKNOWN, TYPO}][:548]'),
        ('!= 547', '!= 548'),
        ('470, 471, 472, 473, 474', '471, 472, 473, 474, 475'),
    ],
)

build(
    'validate-five-hundred-sixty-two-valid-list-cases.py',
    'validate-five-hundred-sixty-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
        ('all_cases[:547]', 'all_cases[:548]'),
        ('len(valid_cases) != 547', 'len(valid_cases) != 548'),
    ],
)

build(
    'validate-five-hundred-sixty-two-valid-mixed.py',
    'validate-five-hundred-sixty-three-valid-mixed.py',
    [
        ('vijfhonderdtweeënzestig', 'vijfhonderddrieënzestig'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
        ('][:547]', '][:548]'),
        ('len(valid_cases) != 547', 'len(valid_cases) != 548'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-two.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-two', 'five-hundred-sixty-three')
(ROOT / 'verify-five-hundred-sixty-three.py').write_text(verify_text)
print('verify-five-hundred-sixty-three.py')
