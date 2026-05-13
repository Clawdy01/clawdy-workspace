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
    'create-five-hundred-seventy-three-assets.py',
    'create-five-hundred-seventy-four-assets.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('[:558]', '[:559]'),
        ('!= 558', '!= 559'),
        ('kreeg 558', 'kreeg 559'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'create-five-hundred-seventy-three-bootstrap.py',
    'create-five-hundred-seventy-four-bootstrap.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('all_cases[:558]', 'all_cases[:559]'),
        ('{UNKNOWN, TYPO}][:558]', '{UNKNOWN, TYPO}][:559]'),
        ('!= 558', '!= 559'),
        ('kreeg 558', 'kreeg 559'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'create-five-hundred-seventy-three-minimal.py',
    'create-five-hundred-seventy-four-minimal.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('!= 558', '!= 559'),
        ('kreeg 558', 'kreeg 559'),
        ('541, 542, 543, 544, 545', '542, 543, 544, 545, 546'),
    ],
)

build(
    'make-five-hundred-seventy-three.py',
    'make-five-hundred-seventy-four.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('all_cases[:558]', 'all_cases[:559]'),
        ('{UNKNOWN, TYPO}][:558]', '{UNKNOWN, TYPO}][:559]'),
        ('!= 558', '!= 559'),
        ('481, 482, 483, 484, 485', '482, 483, 484, 485, 486'),
    ],
)

build(
    'create-five-hundred-seventy-three-files.py',
    'create-five-hundred-seventy-four-files.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('all_cases[:558]', 'all_cases[:559]'),
        ('{UNKNOWN, TYPO}][:558]', '{UNKNOWN, TYPO}][:559]'),
        ('!= 558', '!= 559'),
        ('481, 482, 483, 484, 485', '482, 483, 484, 485, 486'),
    ],
)

build(
    'create-five-hundred-seventy-three.py',
    'create-five-hundred-seventy-four.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('all_cases[:558]', 'all_cases[:559]'),
        ('{UNKNOWN, TYPO}][:558]', '{UNKNOWN, TYPO}][:559]'),
        ('!= 558', '!= 559'),
        ('484, 485, 486, 487, 488', '485, 486, 487, 488, 489'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-three.py',
    'generate-validate-five-hundred-seventy-four.py',
    [
        ('five-hundred-seventy-three', 'five-hundred-seventy-four'),
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('all_cases[:558]', 'all_cases[:559]'),
        ('{UNKNOWN, TYPO}][:558]', '{UNKNOWN, TYPO}][:559]'),
        ('!= 558', '!= 559'),
        ('481, 482, 483, 484, 485', '482, 483, 484, 485, 486'),
    ],
)

build(
    'validate-five-hundred-seventy-three-valid-list-cases.py',
    'validate-five-hundred-seventy-four-valid-list-cases.py',
    [
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
        ('all_cases[:558]', 'all_cases[:559]'),
        ('len(valid_cases) != 558', 'len(valid_cases) != 559'),
    ],
)

build(
    'validate-five-hundred-seventy-three-valid-mixed.py',
    'validate-five-hundred-seventy-four-valid-mixed.py',
    [
        ('vijfhonderddrieënzeventig', 'vijfhonderdvierenzeventig'),
        ('543, 544, 545, 546, 547', '544, 545, 546, 547, 548'),
        ('][:558]', '][:559]'),
        ('len(valid_cases) != 558', 'len(valid_cases) != 559'),
        ('plain stderr noemt niet alle vijfhonderdachtenvijftig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdnegenenvijftig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-three.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-three', 'five-hundred-seventy-four')
(ROOT / 'verify-five-hundred-seventy-four.py').write_text(verify_text)
print('verify-five-hundred-seventy-four.py')
