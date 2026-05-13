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
    'create-five-hundred-seventy-seven-assets.py',
    'create-five-hundred-seventy-eight-assets.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('[:562]', '[:563]'),
        ('!= 562', '!= 563'),
        ('kreeg 562', 'kreeg 563'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'create-five-hundred-seventy-seven-bootstrap.py',
    'create-five-hundred-seventy-eight-bootstrap.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('all_cases[:562]', 'all_cases[:563]'),
        ('{UNKNOWN, TYPO}][:562]', '{UNKNOWN, TYPO}][:563]'),
        ('!= 562', '!= 563'),
        ('kreeg 562', 'kreeg 563'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'create-five-hundred-seventy-seven-minimal.py',
    'create-five-hundred-seventy-eight-minimal.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('!= 562', '!= 563'),
        ('kreeg 562', 'kreeg 563'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'make-five-hundred-seventy-seven.py',
    'make-five-hundred-seventy-eight.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('all_cases[:562]', 'all_cases[:563]'),
        ('{UNKNOWN, TYPO}][:562]', '{UNKNOWN, TYPO}][:563]'),
        ('!= 562', '!= 563'),
        ('485, 486, 487, 488, 489', '486, 487, 488, 489, 490'),
    ],
)

build(
    'create-five-hundred-seventy-seven-files.py',
    'create-five-hundred-seventy-eight-files.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('all_cases[:562]', 'all_cases[:563]'),
        ('{UNKNOWN, TYPO}][:562]', '{UNKNOWN, TYPO}][:563]'),
        ('!= 562', '!= 563'),
        ('485, 486, 487, 488, 489', '486, 487, 488, 489, 490'),
    ],
)

build(
    'create-five-hundred-seventy-seven.py',
    'create-five-hundred-seventy-eight.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('all_cases[:562]', 'all_cases[:563]'),
        ('{UNKNOWN, TYPO}][:562]', '{UNKNOWN, TYPO}][:563]'),
        ('!= 562', '!= 563'),
        ('488, 489, 490, 491, 492', '489, 490, 491, 492, 493'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-seven.py',
    'generate-validate-five-hundred-seventy-eight.py',
    [
        ('five-hundred-seventy-seven', 'five-hundred-seventy-eight'),
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('all_cases[:562]', 'all_cases[:563]'),
        ('{UNKNOWN, TYPO}][:562]', '{UNKNOWN, TYPO}][:563]'),
        ('!= 562', '!= 563'),
        ('485, 486, 487, 488, 489', '486, 487, 488, 489, 490'),
    ],
)

build(
    'validate-five-hundred-seventy-seven-valid-list-cases.py',
    'validate-five-hundred-seventy-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
        ('all_cases[:562]', 'all_cases[:563]'),
        ('len(valid_cases) != 562', 'len(valid_cases) != 563'),
    ],
)

build(
    'validate-five-hundred-seventy-seven-valid-mixed.py',
    'validate-five-hundred-seventy-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenenzeventig', 'vijfhonderdachtenzeventig'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
        ('][:562]', '][:563]'),
        ('len(valid_cases) != 562', 'len(valid_cases) != 563'),
        ('plain stderr noemt niet alle vijfhonderdtweeënzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderddrieënzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-seven', 'five-hundred-seventy-eight')
(ROOT / 'verify-five-hundred-seventy-eight.py').write_text(verify_text)
print('verify-five-hundred-seventy-eight.py')
