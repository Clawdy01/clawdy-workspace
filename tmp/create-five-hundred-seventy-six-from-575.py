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
    'create-five-hundred-seventy-five-assets.py',
    'create-five-hundred-seventy-six-assets.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('[:560]', '[:561]'),
        ('!= 560', '!= 561'),
        ('kreeg 560', 'kreeg 561'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'create-five-hundred-seventy-five-bootstrap.py',
    'create-five-hundred-seventy-six-bootstrap.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('all_cases[:560]', 'all_cases[:561]'),
        ('{UNKNOWN, TYPO}][:560]', '{UNKNOWN, TYPO}][:561]'),
        ('!= 560', '!= 561'),
        ('kreeg 560', 'kreeg 561'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'create-five-hundred-seventy-five-minimal.py',
    'create-five-hundred-seventy-six-minimal.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('!= 560', '!= 561'),
        ('kreeg 560', 'kreeg 561'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
    ],
)

build(
    'make-five-hundred-seventy-five.py',
    'make-five-hundred-seventy-six.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('all_cases[:560]', 'all_cases[:561]'),
        ('{UNKNOWN, TYPO}][:560]', '{UNKNOWN, TYPO}][:561]'),
        ('!= 560', '!= 561'),
        ('483, 484, 485, 486, 487', '484, 485, 486, 487, 488'),
    ],
)

build(
    'create-five-hundred-seventy-five-files.py',
    'create-five-hundred-seventy-six-files.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('all_cases[:560]', 'all_cases[:561]'),
        ('{UNKNOWN, TYPO}][:560]', '{UNKNOWN, TYPO}][:561]'),
        ('!= 560', '!= 561'),
        ('483, 484, 485, 486, 487', '484, 485, 486, 487, 488'),
    ],
)

build(
    'create-five-hundred-seventy-five.py',
    'create-five-hundred-seventy-six.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('all_cases[:560]', 'all_cases[:561]'),
        ('{UNKNOWN, TYPO}][:560]', '{UNKNOWN, TYPO}][:561]'),
        ('!= 560', '!= 561'),
        ('486, 487, 488, 489, 490', '487, 488, 489, 490, 491'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-five.py',
    'generate-validate-five-hundred-seventy-six.py',
    [
        ('five-hundred-seventy-five', 'five-hundred-seventy-six'),
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('all_cases[:560]', 'all_cases[:561]'),
        ('{UNKNOWN, TYPO}][:560]', '{UNKNOWN, TYPO}][:561]'),
        ('!= 560', '!= 561'),
        ('483, 484, 485, 486, 487', '484, 485, 486, 487, 488'),
    ],
)

build(
    'validate-five-hundred-seventy-five-valid-list-cases.py',
    'validate-five-hundred-seventy-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
        ('all_cases[:560]', 'all_cases[:561]'),
        ('len(valid_cases) != 560', 'len(valid_cases) != 561'),
    ],
)

build(
    'validate-five-hundred-seventy-five-valid-mixed.py',
    'validate-five-hundred-seventy-six-valid-mixed.py',
    [
        ('vijfhonderdvijfenzeventig', 'vijfhonderdzesenzeventig'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
        ('][:560]', '][:561]'),
        ('len(valid_cases) != 560', 'len(valid_cases) != 561'),
        ('plain stderr noemt niet alle vijfhonderdzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdeenenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-five.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-five', 'five-hundred-seventy-six')
(ROOT / 'verify-five-hundred-seventy-six.py').write_text(verify_text)
print('verify-five-hundred-seventy-six.py')
