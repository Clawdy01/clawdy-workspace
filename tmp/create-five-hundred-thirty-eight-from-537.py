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
    'create-five-hundred-thirty-seven-assets.py',
    'create-five-hundred-thirty-eight-assets.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('[:522]', '[:523]'),
        ('!= 522', '!= 523'),
        ('kreeg 522', 'kreeg 523'),
        ('510, 511, 512, 513]', '510, 511, 512, 513, 514]'),
    ],
)

build(
    'create-five-hundred-thirty-seven-bootstrap.py',
    'create-five-hundred-thirty-eight-bootstrap.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('all_cases[:522]', 'all_cases[:523]'),
        ('{UNKNOWN, TYPO}][:522]', '{UNKNOWN, TYPO}][:523]'),
        ('!= 522', '!= 523'),
        ('kreeg 522', 'kreeg 523'),
        ('506, 507, 508, 509]', '506, 507, 508, 509, 510]'),
    ],
)

build(
    'create-five-hundred-thirty-seven-minimal.py',
    'create-five-hundred-thirty-eight-minimal.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('!= 522', '!= 523'),
        ('kreeg 522', 'kreeg 523'),
        (' 507, 508, 509]', ' 507, 508, 509, 510]'),
    ],
)

build(
    'make-five-hundred-thirty-seven.py',
    'make-five-hundred-thirty-eight.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('all_cases[:522]', 'all_cases[:523]'),
        ('{UNKNOWN, TYPO}][:522]', '{UNKNOWN, TYPO}][:523]'),
        ('!= 522', '!= 523'),
        ('446, 447, 448, 449]', '446, 447, 448, 449, 450]'),
    ],
)

build(
    'create-five-hundred-thirty-seven-files.py',
    'create-five-hundred-thirty-eight-files.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('all_cases[:522]', 'all_cases[:523]'),
        ('{UNKNOWN, TYPO}][:522]', '{UNKNOWN, TYPO}][:523]'),
        ('!= 522', '!= 523'),
        ('446, 447, 448, 449]', '446, 447, 448, 449, 450]'),
    ],
)

build(
    'create-five-hundred-thirty-seven.py',
    'create-five-hundred-thirty-eight.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('all_cases[:522]', 'all_cases[:523]'),
        ('{UNKNOWN, TYPO}][:522]', '{UNKNOWN, TYPO}][:523]'),
        ('!= 522', '!= 523'),
        ('449, 450, 451, 452]', '449, 450, 451, 452, 453]'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-seven.py',
    'generate-validate-five-hundred-thirty-eight.py',
    [
        ('five-hundred-thirty-seven', 'five-hundred-thirty-eight'),
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('all_cases[:522]', 'all_cases[:523]'),
        ('{UNKNOWN, TYPO}][:522]', '{UNKNOWN, TYPO}][:523]'),
        ('!= 522', '!= 523'),
        ('446, 447, 448, 449]', '446, 447, 448, 449, 450]'),
    ],
)

build(
    'validate-five-hundred-thirty-seven-valid-list-cases.py',
    'validate-five-hundred-thirty-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('508, 509, 510, 511', '508, 509, 510, 511, 512'),
        ('all_cases[:522]', 'all_cases[:523]'),
        ('len(valid_cases) != 522', 'len(valid_cases) != 523'),
    ],
)

build(
    'validate-five-hundred-thirty-seven-valid-mixed.py',
    'validate-five-hundred-thirty-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenendertig', 'vijfhonderdachtendertig'),
        ('508, 509, 510, 511', '508, 509, 510, 511, 512'),
        ('][:522]', '][:523]'),
        ('len(valid_cases) != 522', 'len(valid_cases) != 523'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-seven', 'five-hundred-thirty-eight')
(ROOT / 'verify-five-hundred-thirty-eight.py').write_text(verify_text)
print('verify-five-hundred-thirty-eight.py')
