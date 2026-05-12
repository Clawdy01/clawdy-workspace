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
    'create-five-hundred-twelve-assets.py',
    'create-five-hundred-thirteen-assets.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('[:497]', '[:498]'),
        ('!= 497', '!= 498'),
        ('kreeg 497', 'kreeg 498'),
        ('487, 488]', '487, 488, 489]'),
    ],
)

build(
    'create-five-hundred-twelve-bootstrap.py',
    'create-five-hundred-thirteen-bootstrap.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('all_cases[:497]', 'all_cases[:498]'),
        ('{UNKNOWN, TYPO}][:497]', '{UNKNOWN, TYPO}][:498]'),
        ('!= 497', '!= 498'),
        ('kreeg 497', 'kreeg 498'),
        ('483, 484]', '483, 484, 485]'),
    ],
)

build(
    'create-five-hundred-twelve-minimal.py',
    'create-five-hundred-thirteen-minimal.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('!= 497', '!= 498'),
        ('kreeg 497', 'kreeg 498'),
        (' 438)', ' 439)'),
        ('483, 484]', '483, 484, 485]'),
    ],
)

build(
    'make-five-hundred-twelve.py',
    'make-five-hundred-thirteen.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('all_cases[:497]', 'all_cases[:498]'),
        ('{UNKNOWN, TYPO}][:497]', '{UNKNOWN, TYPO}][:498]'),
        ('!= 497', '!= 498'),
        ('423, 424]', '423, 424, 425]'),
    ],
)

build(
    'create-five-hundred-twelve-files.py',
    'create-five-hundred-thirteen-files.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('all_cases[:497]', 'all_cases[:498]'),
        ('{UNKNOWN, TYPO}][:497]', '{UNKNOWN, TYPO}][:498]'),
        ('!= 497', '!= 498'),
        ('423, 424]', '423, 424, 425]'),
    ],
)

build(
    'create-five-hundred-twelve.py',
    'create-five-hundred-thirteen.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('all_cases[:497]', 'all_cases[:498]'),
        ('{UNKNOWN, TYPO}][:497]', '{UNKNOWN, TYPO}][:498]'),
        ('!= 497', '!= 498'),
        ('427]', '427, 428]'),
    ],
)

build(
    'generate-validate-five-hundred-twelve.py',
    'generate-validate-five-hundred-thirteen.py',
    [
        ('five-hundred-twelve', 'five-hundred-thirteen'),
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('all_cases[:497]', 'all_cases[:498]'),
        ('{UNKNOWN, TYPO}][:497]', '{UNKNOWN, TYPO}][:498]'),
        ('!= 497', '!= 498'),
        ('423, 424]', '423, 424, 425]'),
    ],
)

build(
    'validate-five-hundred-twelve-valid-list-cases.py',
    'validate-five-hundred-thirteen-valid-list-cases.py',
    [
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('485, 486]', '485, 486, 487]'),
        ('all_cases[:497]', 'all_cases[:498]'),
        ('len(valid_cases) != 497', 'len(valid_cases) != 498'),
    ],
)

build(
    'validate-five-hundred-twelve-valid-mixed.py',
    'validate-five-hundred-thirteen-valid-mixed.py',
    [
        ('vijfhonderdtwaalf', 'vijfhonderddertien'),
        ('485, 486]', '485, 486, 487]'),
        ('][:497]', '][:498]'),
        ('len(valid_cases) != 497', 'len(valid_cases) != 498'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twelve.py').read_text()
verify_text = verify_src.replace('five-hundred-twelve', 'five-hundred-thirteen')
(ROOT / 'verify-five-hundred-thirteen.py').write_text(verify_text)
print('verify-five-hundred-thirteen.py')
