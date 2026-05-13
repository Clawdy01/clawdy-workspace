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
    'create-five-hundred-eighty-one-assets.py',
    'create-five-hundred-eighty-two-assets.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('[:566]', '[:567]'),
        ('!= 566', '!= 567'),
        ('kreeg 566', 'kreeg 567'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'create-five-hundred-eighty-one-bootstrap.py',
    'create-five-hundred-eighty-two-bootstrap.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('all_cases[:566]', 'all_cases[:567]'),
        ('{UNKNOWN, TYPO}][:566]', '{UNKNOWN, TYPO}][:567]'),
        ('!= 566', '!= 567'),
        ('kreeg 566', 'kreeg 567'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'create-five-hundred-eighty-one-minimal.py',
    'create-five-hundred-eighty-two-minimal.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('!= 566', '!= 567'),
        ('kreeg 566', 'kreeg 567'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'make-five-hundred-eighty-one.py',
    'make-five-hundred-eighty-two.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('all_cases[:566]', 'all_cases[:567]'),
        ('{UNKNOWN, TYPO}][:566]', '{UNKNOWN, TYPO}][:567]'),
        ('!= 566', '!= 567'),
        ('489, 490, 491, 492, 493', '490, 491, 492, 493, 494'),
    ],
)

build(
    'create-five-hundred-eighty-one-files.py',
    'create-five-hundred-eighty-two-files.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('all_cases[:566]', 'all_cases[:567]'),
        ('{UNKNOWN, TYPO}][:566]', '{UNKNOWN, TYPO}][:567]'),
        ('!= 566', '!= 567'),
        ('489, 490, 491, 492, 493', '490, 491, 492, 493, 494'),
    ],
)

build(
    'create-five-hundred-eighty-one.py',
    'create-five-hundred-eighty-two.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('all_cases[:566]', 'all_cases[:567]'),
        ('{UNKNOWN, TYPO}][:566]', '{UNKNOWN, TYPO}][:567]'),
        ('!= 566', '!= 567'),
        ('492, 493, 494, 495, 496', '493, 494, 495, 496, 497'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-one.py',
    'generate-validate-five-hundred-eighty-two.py',
    [
        ('five-hundred-eighty-one', 'five-hundred-eighty-two'),
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('all_cases[:566]', 'all_cases[:567]'),
        ('{UNKNOWN, TYPO}][:566]', '{UNKNOWN, TYPO}][:567]'),
        ('!= 566', '!= 567'),
        ('489, 490, 491, 492, 493', '490, 491, 492, 493, 494'),
    ],
)

build(
    'validate-five-hundred-eighty-one-valid-list-cases.py',
    'validate-five-hundred-eighty-two-valid-list-cases.py',
    [
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
        ('all_cases[:566]', 'all_cases[:567]'),
        ('len(valid_cases) != 566', 'len(valid_cases) != 567'),
    ],
)

build(
    'validate-five-hundred-eighty-one-valid-mixed.py',
    'validate-five-hundred-eighty-two-valid-mixed.py',
    [
        ('vijfhonderdeenentachtig', 'vijfhonderdtweeëntachtig'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
        ('][:566]', '][:567]'),
        ('len(valid_cases) != 566', 'len(valid_cases) != 567'),
        ('plain stderr noemt niet alle vijfhonderdzesenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzevenenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-one.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-one', 'five-hundred-eighty-two')
(ROOT / 'verify-five-hundred-eighty-two.py').write_text(verify_text)
print('verify-five-hundred-eighty-two.py')
