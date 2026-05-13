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
    'create-five-hundred-sixty-one-assets.py',
    'create-five-hundred-sixty-two-assets.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('[:546]', '[:547]'),
        ('!= 546', '!= 547'),
        ('kreeg 546', 'kreeg 547'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'create-five-hundred-sixty-one-bootstrap.py',
    'create-five-hundred-sixty-two-bootstrap.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('all_cases[:546]', 'all_cases[:547]'),
        ('{UNKNOWN, TYPO}][:546]', '{UNKNOWN, TYPO}][:547]'),
        ('!= 546', '!= 547'),
        ('kreeg 546', 'kreeg 547'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
    ],
)

build(
    'create-five-hundred-sixty-one-minimal.py',
    'create-five-hundred-sixty-two-minimal.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('!= 546', '!= 547'),
        ('kreeg 546', 'kreeg 547'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
    ],
)

build(
    'make-five-hundred-sixty-one.py',
    'make-five-hundred-sixty-two.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('all_cases[:546]', 'all_cases[:547]'),
        ('{UNKNOWN, TYPO}][:546]', '{UNKNOWN, TYPO}][:547]'),
        ('!= 546', '!= 547'),
        ('469, 470, 471, 472, 473', '470, 471, 472, 473, 474'),
    ],
)

build(
    'create-five-hundred-sixty-one-files.py',
    'create-five-hundred-sixty-two-files.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('all_cases[:546]', 'all_cases[:547]'),
        ('{UNKNOWN, TYPO}][:546]', '{UNKNOWN, TYPO}][:547]'),
        ('!= 546', '!= 547'),
        ('469, 470, 471, 472, 473', '470, 471, 472, 473, 474'),
    ],
)

build(
    'create-five-hundred-sixty-one.py',
    'create-five-hundred-sixty-two.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('all_cases[:546]', 'all_cases[:547]'),
        ('{UNKNOWN, TYPO}][:546]', '{UNKNOWN, TYPO}][:547]'),
        ('!= 546', '!= 547'),
        ('472, 473, 474, 475, 476', '473, 474, 475, 476, 477'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-one.py',
    'generate-validate-five-hundred-sixty-two.py',
    [
        ('five-hundred-sixty-one', 'five-hundred-sixty-two'),
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('all_cases[:546]', 'all_cases[:547]'),
        ('{UNKNOWN, TYPO}][:546]', '{UNKNOWN, TYPO}][:547]'),
        ('!= 546', '!= 547'),
        ('469, 470, 471, 472, 473', '470, 471, 472, 473, 474'),
    ],
)

build(
    'validate-five-hundred-sixty-one-valid-list-cases.py',
    'validate-five-hundred-sixty-two-valid-list-cases.py',
    [
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
        ('all_cases[:546]', 'all_cases[:547]'),
        ('len(valid_cases) != 546', 'len(valid_cases) != 547'),
    ],
)

build(
    'validate-five-hundred-sixty-one-valid-mixed.py',
    'validate-five-hundred-sixty-two-valid-mixed.py',
    [
        ('vijfhonderdeenenzestig', 'vijfhonderdtweeënzestig'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
        ('][:546]', '][:547]'),
        ('len(valid_cases) != 546', 'len(valid_cases) != 547'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-one.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-one', 'five-hundred-sixty-two')
(ROOT / 'verify-five-hundred-sixty-two.py').write_text(verify_text)
print('verify-five-hundred-sixty-two.py')
