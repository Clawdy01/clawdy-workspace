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
    'create-five-hundred-thirty-eight-assets.py',
    'create-five-hundred-thirty-nine-assets.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('[:523]', '[:524]'),
        ('!= 523', '!= 524'),
        ('kreeg 523', 'kreeg 524'),
        ('512, 513, 514]', '512, 513, 514, 515]'),
    ],
)

build(
    'create-five-hundred-thirty-eight-bootstrap.py',
    'create-five-hundred-thirty-nine-bootstrap.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('all_cases[:523]', 'all_cases[:524]'),
        ('{UNKNOWN, TYPO}][:523]', '{UNKNOWN, TYPO}][:524]'),
        ('!= 523', '!= 524'),
        ('kreeg 523', 'kreeg 524'),
        ('508, 509, 510]', '508, 509, 510, 511]'),
    ],
)

build(
    'create-five-hundred-thirty-eight-minimal.py',
    'create-five-hundred-thirty-nine-minimal.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('!= 523', '!= 524'),
        ('kreeg 523', 'kreeg 524'),
        ('508, 509, 510]', '508, 509, 510, 511]'),
    ],
)

build(
    'make-five-hundred-thirty-eight.py',
    'make-five-hundred-thirty-nine.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('all_cases[:523]', 'all_cases[:524]'),
        ('{UNKNOWN, TYPO}][:523]', '{UNKNOWN, TYPO}][:524]'),
        ('!= 523', '!= 524'),
        ('448, 449, 450]', '448, 449, 450, 451]'),
    ],
)

build(
    'create-five-hundred-thirty-eight-files.py',
    'create-five-hundred-thirty-nine-files.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('all_cases[:523]', 'all_cases[:524]'),
        ('{UNKNOWN, TYPO}][:523]', '{UNKNOWN, TYPO}][:524]'),
        ('!= 523', '!= 524'),
        ('448, 449, 450]', '448, 449, 450, 451]'),
    ],
)

build(
    'create-five-hundred-thirty-eight.py',
    'create-five-hundred-thirty-nine.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('all_cases[:523]', 'all_cases[:524]'),
        ('{UNKNOWN, TYPO}][:523]', '{UNKNOWN, TYPO}][:524]'),
        ('!= 523', '!= 524'),
        ('451, 452, 453]', '451, 452, 453, 454]'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-eight.py',
    'generate-validate-five-hundred-thirty-nine.py',
    [
        ('five-hundred-thirty-eight', 'five-hundred-thirty-nine'),
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('all_cases[:523]', 'all_cases[:524]'),
        ('{UNKNOWN, TYPO}][:523]', '{UNKNOWN, TYPO}][:524]'),
        ('!= 523', '!= 524'),
        ('448, 449, 450]', '448, 449, 450, 451]'),
    ],
)

build(
    'validate-five-hundred-thirty-eight-valid-list-cases.py',
    'validate-five-hundred-thirty-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('510, 511, 512', '510, 511, 512, 513'),
        ('all_cases[:523]', 'all_cases[:524]'),
        ('len(valid_cases) != 523', 'len(valid_cases) != 524'),
    ],
)

build(
    'validate-five-hundred-thirty-eight-valid-mixed.py',
    'validate-five-hundred-thirty-nine-valid-mixed.py',
    [
        ('vijfhonderdachtendertig', 'vijfhonderdnegenendertig'),
        ('510, 511, 512', '510, 511, 512, 513'),
        ('][:523]', '][:524]'),
        ('len(valid_cases) != 523', 'len(valid_cases) != 524'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-eight', 'five-hundred-thirty-nine')
(ROOT / 'verify-five-hundred-thirty-nine.py').write_text(verify_text)
print('verify-five-hundred-thirty-nine.py')
