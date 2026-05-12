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
    'create-five-hundred-sixteen-assets.py',
    'create-five-hundred-seventeen-assets.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('[:501]', '[:502]'),
        ('!= 501', '!= 502'),
        ('kreeg 501', 'kreeg 502'),
        ('488, 489, 490, 491, 492]', '488, 489, 490, 491, 492, 493]'),
    ],
)

build(
    'create-five-hundred-sixteen-bootstrap.py',
    'create-five-hundred-seventeen-bootstrap.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('all_cases[:501]', 'all_cases[:502]'),
        ('{UNKNOWN, TYPO}][:501]', '{UNKNOWN, TYPO}][:502]'),
        ('!= 501', '!= 502'),
        ('kreeg 501', 'kreeg 502'),
        ('484, 485, 486, 487, 488]', '484, 485, 486, 487, 488, 489]'),
    ],
)

build(
    'create-five-hundred-sixteen-minimal.py',
    'create-five-hundred-seventeen-minimal.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('!= 501', '!= 502'),
        ('kreeg 501', 'kreeg 502'),
        (' 442)', ' 443)'),
        ('484, 485, 486, 487, 488]', '484, 485, 486, 487, 488, 489]'),
    ],
)

build(
    'make-five-hundred-sixteen.py',
    'make-five-hundred-seventeen.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('all_cases[:501]', 'all_cases[:502]'),
        ('{UNKNOWN, TYPO}][:501]', '{UNKNOWN, TYPO}][:502]'),
        ('!= 501', '!= 502'),
        ('424, 425, 426, 427, 428]', '424, 425, 426, 427, 428, 429]'),
    ],
)

build(
    'create-five-hundred-sixteen-files.py',
    'create-five-hundred-seventeen-files.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('all_cases[:501]', 'all_cases[:502]'),
        ('{UNKNOWN, TYPO}][:501]', '{UNKNOWN, TYPO}][:502]'),
        ('!= 501', '!= 502'),
        ('424, 425, 426, 427, 428]', '424, 425, 426, 427, 428, 429]'),
    ],
)

build(
    'create-five-hundred-sixteen.py',
    'create-five-hundred-seventeen.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('all_cases[:501]', 'all_cases[:502]'),
        ('{UNKNOWN, TYPO}][:501]', '{UNKNOWN, TYPO}][:502]'),
        ('!= 501', '!= 502'),
        ('428, 429, 430, 431]', '428, 429, 430, 431, 432]'),
    ],
)

build(
    'generate-validate-five-hundred-sixteen.py',
    'generate-validate-five-hundred-seventeen.py',
    [
        ('five-hundred-sixteen', 'five-hundred-seventeen'),
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('all_cases[:501]', 'all_cases[:502]'),
        ('{UNKNOWN, TYPO}][:501]', '{UNKNOWN, TYPO}][:502]'),
        ('!= 501', '!= 502'),
        ('424, 425, 426, 427, 428]', '424, 425, 426, 427, 428, 429]'),
    ],
)

build(
    'validate-five-hundred-sixteen-valid-list-cases.py',
    'validate-five-hundred-seventeen-valid-list-cases.py',
    [
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('486, 487, 488, 489, 490]', '486, 487, 488, 489, 490, 491]'),
        ('all_cases[:501]', 'all_cases[:502]'),
        ('len(valid_cases) != 501', 'len(valid_cases) != 502'),
    ],
)

build(
    'validate-five-hundred-sixteen-valid-mixed.py',
    'validate-five-hundred-seventeen-valid-mixed.py',
    [
        ('vijfhonderdzestien', 'vijfhonderdzeventien'),
        ('486, 487, 488, 489, 490]', '486, 487, 488, 489, 490, 491]'),
        ('][:501]', '][:502]'),
        ('len(valid_cases) != 501', 'len(valid_cases) != 502'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixteen.py').read_text()
verify_text = verify_src.replace('five-hundred-sixteen', 'five-hundred-seventeen')
(ROOT / 'verify-five-hundred-seventeen.py').write_text(verify_text)
print('verify-five-hundred-seventeen.py')
