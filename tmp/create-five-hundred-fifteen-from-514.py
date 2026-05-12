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
    'create-five-hundred-fourteen-assets.py',
    'create-five-hundred-fifteen-assets.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('[:499]', '[:500]'),
        ('!= 499', '!= 500'),
        ('kreeg 499', 'kreeg 500'),
        ('487, 488, 489, 490]', '487, 488, 489, 490, 491]'),
    ],
)

build(
    'create-five-hundred-fourteen-bootstrap.py',
    'create-five-hundred-fifteen-bootstrap.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('all_cases[:499]', 'all_cases[:500]'),
        ('{UNKNOWN, TYPO}][:499]', '{UNKNOWN, TYPO}][:500]'),
        ('!= 499', '!= 500'),
        ('kreeg 499', 'kreeg 500'),
        ('483, 484, 485, 486]', '483, 484, 485, 486, 487]'),
    ],
)

build(
    'create-five-hundred-fourteen-minimal.py',
    'create-five-hundred-fifteen-minimal.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('!= 499', '!= 500'),
        ('kreeg 499', 'kreeg 500'),
        (' 440)', ' 441)'),
        ('483, 484, 485, 486]', '483, 484, 485, 486, 487]'),
    ],
)

build(
    'make-five-hundred-fourteen.py',
    'make-five-hundred-fifteen.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('all_cases[:499]', 'all_cases[:500]'),
        ('{UNKNOWN, TYPO}][:499]', '{UNKNOWN, TYPO}][:500]'),
        ('!= 499', '!= 500'),
        ('423, 424, 425, 426]', '423, 424, 425, 426, 427]'),
    ],
)

build(
    'create-five-hundred-fourteen-files.py',
    'create-five-hundred-fifteen-files.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('all_cases[:499]', 'all_cases[:500]'),
        ('{UNKNOWN, TYPO}][:499]', '{UNKNOWN, TYPO}][:500]'),
        ('!= 499', '!= 500'),
        ('423, 424, 425, 426]', '423, 424, 425, 426, 427]'),
    ],
)

build(
    'create-five-hundred-fourteen.py',
    'create-five-hundred-fifteen.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('all_cases[:499]', 'all_cases[:500]'),
        ('{UNKNOWN, TYPO}][:499]', '{UNKNOWN, TYPO}][:500]'),
        ('!= 499', '!= 500'),
        ('427, 428, 429]', '427, 428, 429, 430]'),
    ],
)

build(
    'generate-validate-five-hundred-fourteen.py',
    'generate-validate-five-hundred-fifteen.py',
    [
        ('five-hundred-fourteen', 'five-hundred-fifteen'),
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('all_cases[:499]', 'all_cases[:500]'),
        ('{UNKNOWN, TYPO}][:499]', '{UNKNOWN, TYPO}][:500]'),
        ('!= 499', '!= 500'),
        ('423, 424, 425, 426]', '423, 424, 425, 426, 427]'),
    ],
)

build(
    'validate-five-hundred-fourteen-valid-list-cases.py',
    'validate-five-hundred-fifteen-valid-list-cases.py',
    [
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('485, 486, 487, 488]', '485, 486, 487, 488, 489]'),
        ('all_cases[:499]', 'all_cases[:500]'),
        ('len(valid_cases) != 499', 'len(valid_cases) != 500'),
    ],
)

build(
    'validate-five-hundred-fourteen-valid-mixed.py',
    'validate-five-hundred-fifteen-valid-mixed.py',
    [
        ('vijfhonderdveertien', 'vijfhonderdvijftien'),
        ('485, 486, 487, 488]', '485, 486, 487, 488, 489]'),
        ('][:499]', '][:500]'),
        ('len(valid_cases) != 499', 'len(valid_cases) != 500'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fourteen.py').read_text()
verify_text = verify_src.replace('five-hundred-fourteen', 'five-hundred-fifteen')
(ROOT / 'verify-five-hundred-fifteen.py').write_text(verify_text)
print('verify-five-hundred-fifteen.py')
