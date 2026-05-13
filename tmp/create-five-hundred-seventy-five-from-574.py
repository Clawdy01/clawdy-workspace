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
    'create-five-hundred-seventy-four-assets.py',
    'create-five-hundred-seventy-five-assets.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('[:559]', '[:560]'),
        ('!= 559', '!= 560'),
        ('kreeg 559', 'kreeg 560'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'create-five-hundred-seventy-four-bootstrap.py',
    'create-five-hundred-seventy-five-bootstrap.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('all_cases[:559]', 'all_cases[:560]'),
        ('{UNKNOWN, TYPO}][:559]', '{UNKNOWN, TYPO}][:560]'),
        ('!= 559', '!= 560'),
        ('kreeg 559', 'kreeg 560'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'create-five-hundred-seventy-four-minimal.py',
    'create-five-hundred-seventy-five-minimal.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('!= 559', '!= 560'),
        ('kreeg 559', 'kreeg 560'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
    ],
)

build(
    'make-five-hundred-seventy-four.py',
    'make-five-hundred-seventy-five.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('all_cases[:559]', 'all_cases[:560]'),
        ('{UNKNOWN, TYPO}][:559]', '{UNKNOWN, TYPO}][:560]'),
        ('!= 559', '!= 560'),
        ('482, 483, 484, 485, 486', '483, 484, 485, 486, 487'),
    ],
)

build(
    'create-five-hundred-seventy-four-files.py',
    'create-five-hundred-seventy-five-files.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('all_cases[:559]', 'all_cases[:560]'),
        ('{UNKNOWN, TYPO}][:559]', '{UNKNOWN, TYPO}][:560]'),
        ('!= 559', '!= 560'),
        ('482, 483, 484, 485, 486', '483, 484, 485, 486, 487'),
    ],
)

build(
    'create-five-hundred-seventy-four.py',
    'create-five-hundred-seventy-five.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('all_cases[:559]', 'all_cases[:560]'),
        ('{UNKNOWN, TYPO}][:559]', '{UNKNOWN, TYPO}][:560]'),
        ('!= 559', '!= 560'),
        ('485, 486, 487, 488, 489', '486, 487, 488, 489, 490'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-four.py',
    'generate-validate-five-hundred-seventy-five.py',
    [
        ('five-hundred-seventy-four', 'five-hundred-seventy-five'),
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('all_cases[:559]', 'all_cases[:560]'),
        ('{UNKNOWN, TYPO}][:559]', '{UNKNOWN, TYPO}][:560]'),
        ('!= 559', '!= 560'),
        ('482, 483, 484, 485, 486', '483, 484, 485, 486, 487'),
    ],
)

build(
    'validate-five-hundred-seventy-four-valid-list-cases.py',
    'validate-five-hundred-seventy-five-valid-list-cases.py',
    [
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
        ('all_cases[:559]', 'all_cases[:560]'),
        ('len(valid_cases) != 559', 'len(valid_cases) != 560'),
    ],
)

build(
    'validate-five-hundred-seventy-four-valid-mixed.py',
    'validate-five-hundred-seventy-five-valid-mixed.py',
    [
        ('vijfhonderdvierenzeventig', 'vijfhonderdvijfenzeventig'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
        ('][:559]', '][:560]'),
        ('len(valid_cases) != 559', 'len(valid_cases) != 560'),
        ('plain stderr noemt niet alle vijfhonderdnegenenvijftig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-four.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-four', 'five-hundred-seventy-five')
(ROOT / 'verify-five-hundred-seventy-five.py').write_text(verify_text)
print('verify-five-hundred-seventy-five.py')
