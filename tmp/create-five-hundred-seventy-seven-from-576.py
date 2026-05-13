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
    'create-five-hundred-seventy-six-assets.py',
    'create-five-hundred-seventy-seven-assets.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('[:561]', '[:562]'),
        ('!= 561', '!= 562'),
        ('kreeg 561', 'kreeg 562'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'create-five-hundred-seventy-six-bootstrap.py',
    'create-five-hundred-seventy-seven-bootstrap.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('all_cases[:561]', 'all_cases[:562]'),
        ('{UNKNOWN, TYPO}][:561]', '{UNKNOWN, TYPO}][:562]'),
        ('!= 561', '!= 562'),
        ('kreeg 561', 'kreeg 562'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'create-five-hundred-seventy-six-minimal.py',
    'create-five-hundred-seventy-seven-minimal.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('!= 561', '!= 562'),
        ('kreeg 561', 'kreeg 562'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'make-five-hundred-seventy-six.py',
    'make-five-hundred-seventy-seven.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('all_cases[:561]', 'all_cases[:562]'),
        ('{UNKNOWN, TYPO}][:561]', '{UNKNOWN, TYPO}][:562]'),
        ('!= 561', '!= 562'),
        ('484, 485, 486, 487, 488', '485, 486, 487, 488, 489'),
    ],
)

build(
    'create-five-hundred-seventy-six-files.py',
    'create-five-hundred-seventy-seven-files.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('all_cases[:561]', 'all_cases[:562]'),
        ('{UNKNOWN, TYPO}][:561]', '{UNKNOWN, TYPO}][:562]'),
        ('!= 561', '!= 562'),
        ('484, 485, 486, 487, 488', '485, 486, 487, 488, 489'),
    ],
)

build(
    'create-five-hundred-seventy-six.py',
    'create-five-hundred-seventy-seven.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('all_cases[:561]', 'all_cases[:562]'),
        ('{UNKNOWN, TYPO}][:561]', '{UNKNOWN, TYPO}][:562]'),
        ('!= 561', '!= 562'),
        ('487, 488, 489, 490, 491', '488, 489, 490, 491, 492'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-six.py',
    'generate-validate-five-hundred-seventy-seven.py',
    [
        ('five-hundred-seventy-six', 'five-hundred-seventy-seven'),
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('all_cases[:561]', 'all_cases[:562]'),
        ('{UNKNOWN, TYPO}][:561]', '{UNKNOWN, TYPO}][:562]'),
        ('!= 561', '!= 562'),
        ('484, 485, 486, 487, 488', '485, 486, 487, 488, 489'),
    ],
)

build(
    'validate-five-hundred-seventy-six-valid-list-cases.py',
    'validate-five-hundred-seventy-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
        ('all_cases[:561]', 'all_cases[:562]'),
        ('len(valid_cases) != 561', 'len(valid_cases) != 562'),
    ],
)

build(
    'validate-five-hundred-seventy-six-valid-mixed.py',
    'validate-five-hundred-seventy-seven-valid-mixed.py',
    [
        ('vijfhonderdzesenzeventig', 'vijfhonderdzevenenzeventig'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
        ('][:561]', '][:562]'),
        ('len(valid_cases) != 561', 'len(valid_cases) != 562'),
        ('plain stderr noemt niet alle vijfhonderdeenenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdtweeënzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-six.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-six', 'five-hundred-seventy-seven')
(ROOT / 'verify-five-hundred-seventy-seven.py').write_text(verify_text)
print('verify-five-hundred-seventy-seven.py')
