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
    'create-five-hundred-thirteen-assets.py',
    'create-five-hundred-fourteen-assets.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('[:498]', '[:499]'),
        ('!= 498', '!= 499'),
        ('kreeg 498', 'kreeg 499'),
        ('487, 488, 489]', '487, 488, 489, 490]'),
    ],
)

build(
    'create-five-hundred-thirteen-bootstrap.py',
    'create-five-hundred-fourteen-bootstrap.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('all_cases[:498]', 'all_cases[:499]'),
        ('{UNKNOWN, TYPO}][:498]', '{UNKNOWN, TYPO}][:499]'),
        ('!= 498', '!= 499'),
        ('kreeg 498', 'kreeg 499'),
        ('483, 484, 485]', '483, 484, 485, 486]'),
    ],
)

build(
    'create-five-hundred-thirteen-minimal.py',
    'create-five-hundred-fourteen-minimal.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('!= 498', '!= 499'),
        ('kreeg 498', 'kreeg 499'),
        (' 439)', ' 440)'),
        ('483, 484, 485]', '483, 484, 485, 486]'),
    ],
)

build(
    'make-five-hundred-thirteen.py',
    'make-five-hundred-fourteen.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('all_cases[:498]', 'all_cases[:499]'),
        ('{UNKNOWN, TYPO}][:498]', '{UNKNOWN, TYPO}][:499]'),
        ('!= 498', '!= 499'),
        ('423, 424, 425]', '423, 424, 425, 426]'),
    ],
)

build(
    'create-five-hundred-thirteen-files.py',
    'create-five-hundred-fourteen-files.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('all_cases[:498]', 'all_cases[:499]'),
        ('{UNKNOWN, TYPO}][:498]', '{UNKNOWN, TYPO}][:499]'),
        ('!= 498', '!= 499'),
        ('423, 424, 425]', '423, 424, 425, 426]'),
    ],
)

build(
    'create-five-hundred-thirteen.py',
    'create-five-hundred-fourteen.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('all_cases[:498]', 'all_cases[:499]'),
        ('{UNKNOWN, TYPO}][:498]', '{UNKNOWN, TYPO}][:499]'),
        ('!= 498', '!= 499'),
        ('427, 428]', '427, 428, 429]'),
    ],
)

build(
    'generate-validate-five-hundred-thirteen.py',
    'generate-validate-five-hundred-fourteen.py',
    [
        ('five-hundred-thirteen', 'five-hundred-fourteen'),
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('all_cases[:498]', 'all_cases[:499]'),
        ('{UNKNOWN, TYPO}][:498]', '{UNKNOWN, TYPO}][:499]'),
        ('!= 498', '!= 499'),
        ('423, 424, 425]', '423, 424, 425, 426]'),
    ],
)

build(
    'validate-five-hundred-thirteen-valid-list-cases.py',
    'validate-five-hundred-fourteen-valid-list-cases.py',
    [
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('485, 486, 487]', '485, 486, 487, 488]'),
        ('all_cases[:498]', 'all_cases[:499]'),
        ('len(valid_cases) != 498', 'len(valid_cases) != 499'),
    ],
)

build(
    'validate-five-hundred-thirteen-valid-mixed.py',
    'validate-five-hundred-fourteen-valid-mixed.py',
    [
        ('vijfhonderddertien', 'vijfhonderdveertien'),
        ('485, 486, 487]', '485, 486, 487, 488]'),
        ('][:498]', '][:499]'),
        ('len(valid_cases) != 498', 'len(valid_cases) != 499'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirteen.py').read_text()
verify_text = verify_src.replace('five-hundred-thirteen', 'five-hundred-fourteen')
(ROOT / 'verify-five-hundred-fourteen.py').write_text(verify_text)
print('verify-five-hundred-fourteen.py')
