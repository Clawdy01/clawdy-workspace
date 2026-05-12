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
    'create-five-hundred-fifteen-assets.py',
    'create-five-hundred-sixteen-assets.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('[:500]', '[:501]'),
        ('!= 500', '!= 501'),
        ('kreeg 500', 'kreeg 501'),
        ('488, 489, 490, 491]', '488, 489, 490, 491, 492]'),
    ],
)

build(
    'create-five-hundred-fifteen-bootstrap.py',
    'create-five-hundred-sixteen-bootstrap.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('all_cases[:500]', 'all_cases[:501]'),
        ('{UNKNOWN, TYPO}][:500]', '{UNKNOWN, TYPO}][:501]'),
        ('!= 500', '!= 501'),
        ('kreeg 500', 'kreeg 501'),
        ('484, 485, 486, 487]', '484, 485, 486, 487, 488]'),
    ],
)

build(
    'create-five-hundred-fifteen-minimal.py',
    'create-five-hundred-sixteen-minimal.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('!= 500', '!= 501'),
        ('kreeg 500', 'kreeg 501'),
        (' 441)', ' 442)'),
        ('484, 485, 486, 487]', '484, 485, 486, 487, 488]'),
    ],
)

build(
    'make-five-hundred-fifteen.py',
    'make-five-hundred-sixteen.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('all_cases[:500]', 'all_cases[:501]'),
        ('{UNKNOWN, TYPO}][:500]', '{UNKNOWN, TYPO}][:501]'),
        ('!= 500', '!= 501'),
        ('424, 425, 426, 427]', '424, 425, 426, 427, 428]'),
    ],
)

build(
    'create-five-hundred-fifteen-files.py',
    'create-five-hundred-sixteen-files.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('all_cases[:500]', 'all_cases[:501]'),
        ('{UNKNOWN, TYPO}][:500]', '{UNKNOWN, TYPO}][:501]'),
        ('!= 500', '!= 501'),
        ('424, 425, 426, 427]', '424, 425, 426, 427, 428]'),
    ],
)

build(
    'create-five-hundred-fifteen.py',
    'create-five-hundred-sixteen.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('all_cases[:500]', 'all_cases[:501]'),
        ('{UNKNOWN, TYPO}][:500]', '{UNKNOWN, TYPO}][:501]'),
        ('!= 500', '!= 501'),
        ('428, 429, 430]', '428, 429, 430, 431]'),
    ],
)

build(
    'generate-validate-five-hundred-fifteen.py',
    'generate-validate-five-hundred-sixteen.py',
    [
        ('five-hundred-fifteen', 'five-hundred-sixteen'),
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('all_cases[:500]', 'all_cases[:501]'),
        ('{UNKNOWN, TYPO}][:500]', '{UNKNOWN, TYPO}][:501]'),
        ('!= 500', '!= 501'),
        ('424, 425, 426, 427]', '424, 425, 426, 427, 428]'),
    ],
)

build(
    'validate-five-hundred-fifteen-valid-list-cases.py',
    'validate-five-hundred-sixteen-valid-list-cases.py',
    [
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('486, 487, 488, 489]', '486, 487, 488, 489, 490]'),
        ('all_cases[:500]', 'all_cases[:501]'),
        ('len(valid_cases) != 500', 'len(valid_cases) != 501'),
    ],
)

build(
    'validate-five-hundred-fifteen-valid-mixed.py',
    'validate-five-hundred-sixteen-valid-mixed.py',
    [
        ('vijfhonderdvijftien', 'vijfhonderdzestien'),
        ('486, 487, 488, 489]', '486, 487, 488, 489, 490]'),
        ('][:500]', '][:501]'),
        ('len(valid_cases) != 500', 'len(valid_cases) != 501'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifteen.py').read_text()
verify_text = verify_src.replace('five-hundred-fifteen', 'five-hundred-sixteen')
(ROOT / 'verify-five-hundred-sixteen.py').write_text(verify_text)
print('verify-five-hundred-sixteen.py')
