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
    'create-five-hundred-eighty-assets.py',
    'create-five-hundred-eighty-one-assets.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('[:565]', '[:566]'),
        ('!= 565', '!= 566'),
        ('kreeg 565', 'kreeg 566'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'create-five-hundred-eighty-bootstrap.py',
    'create-five-hundred-eighty-one-bootstrap.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('all_cases[:565]', 'all_cases[:566]'),
        ('{UNKNOWN, TYPO}][:565]', '{UNKNOWN, TYPO}][:566]'),
        ('!= 565', '!= 566'),
        ('kreeg 565', 'kreeg 566'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'create-five-hundred-eighty-minimal.py',
    'create-five-hundred-eighty-one-minimal.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('!= 565', '!= 566'),
        ('kreeg 565', 'kreeg 566'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'make-five-hundred-eighty.py',
    'make-five-hundred-eighty-one.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('all_cases[:565]', 'all_cases[:566]'),
        ('{UNKNOWN, TYPO}][:565]', '{UNKNOWN, TYPO}][:566]'),
        ('!= 565', '!= 566'),
        ('488, 489, 490, 491, 492', '489, 490, 491, 492, 493'),
    ],
)

build(
    'create-five-hundred-eighty-files.py',
    'create-five-hundred-eighty-one-files.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('all_cases[:565]', 'all_cases[:566]'),
        ('{UNKNOWN, TYPO}][:565]', '{UNKNOWN, TYPO}][:566]'),
        ('!= 565', '!= 566'),
        ('488, 489, 490, 491, 492', '489, 490, 491, 492, 493'),
    ],
)

build(
    'create-five-hundred-eighty.py',
    'create-five-hundred-eighty-one.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('all_cases[:565]', 'all_cases[:566]'),
        ('{UNKNOWN, TYPO}][:565]', '{UNKNOWN, TYPO}][:566]'),
        ('!= 565', '!= 566'),
        ('491, 492, 493, 494, 495', '492, 493, 494, 495, 496'),
    ],
)

build(
    'generate-validate-five-hundred-eighty.py',
    'generate-validate-five-hundred-eighty-one.py',
    [
        ('five-hundred-eighty', 'five-hundred-eighty-one'),
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('all_cases[:565]', 'all_cases[:566]'),
        ('{UNKNOWN, TYPO}][:565]', '{UNKNOWN, TYPO}][:566]'),
        ('!= 565', '!= 566'),
        ('488, 489, 490, 491, 492', '489, 490, 491, 492, 493'),
    ],
)

build(
    'validate-five-hundred-eighty-valid-list-cases.py',
    'validate-five-hundred-eighty-one-valid-list-cases.py',
    [
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
        ('all_cases[:565]', 'all_cases[:566]'),
        ('len(valid_cases) != 565', 'len(valid_cases) != 566'),
    ],
)

build(
    'validate-five-hundred-eighty-valid-mixed.py',
    'validate-five-hundred-eighty-one-valid-mixed.py',
    [
        ('vijfhonderdtachtig', 'vijfhonderdeenentachtig'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
        ('][:565]', '][:566]'),
        ('len(valid_cases) != 565', 'len(valid_cases) != 566'),
        ('plain stderr noemt niet alle vijfhonderdvijfenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzesenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty', 'five-hundred-eighty-one')
(ROOT / 'verify-five-hundred-eighty-one.py').write_text(verify_text)
print('verify-five-hundred-eighty-one.py')
