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
    'create-five-hundred-forty-assets.py',
    'create-five-hundred-forty-one-assets.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('[:525]', '[:526]'),
        ('!= 525', '!= 526'),
        ('kreeg 525', 'kreeg 526'),
        ('512, 513, 514, 515, 516]', '513, 514, 515, 516, 517]'),
    ],
)

build(
    'create-five-hundred-forty-bootstrap.py',
    'create-five-hundred-forty-one-bootstrap.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('all_cases[:525]', 'all_cases[:526]'),
        ('{UNKNOWN, TYPO}][:525]', '{UNKNOWN, TYPO}][:526]'),
        ('!= 525', '!= 526'),
        ('kreeg 525', 'kreeg 526'),
        ('508, 509, 510, 511, 512]', '509, 510, 511, 512, 513]'),
    ],
)

build(
    'create-five-hundred-forty-minimal.py',
    'create-five-hundred-forty-one-minimal.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('!= 525', '!= 526'),
        ('kreeg 525', 'kreeg 526'),
        ('508, 509, 510, 511, 512]', '509, 510, 511, 512, 513]'),
    ],
)

build(
    'make-five-hundred-forty.py',
    'make-five-hundred-forty-one.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('all_cases[:525]', 'all_cases[:526]'),
        ('{UNKNOWN, TYPO}][:525]', '{UNKNOWN, TYPO}][:526]'),
        ('!= 525', '!= 526'),
        ('448, 449, 450, 451, 452]', '449, 450, 451, 452, 453]'),
    ],
)

build(
    'create-five-hundred-forty-files.py',
    'create-five-hundred-forty-one-files.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('all_cases[:525]', 'all_cases[:526]'),
        ('{UNKNOWN, TYPO}][:525]', '{UNKNOWN, TYPO}][:526]'),
        ('!= 525', '!= 526'),
        ('448, 449, 450, 451, 452]', '449, 450, 451, 452, 453]'),
    ],
)

build(
    'create-five-hundred-forty.py',
    'create-five-hundred-forty-one.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('all_cases[:525]', 'all_cases[:526]'),
        ('{UNKNOWN, TYPO}][:525]', '{UNKNOWN, TYPO}][:526]'),
        ('!= 525', '!= 526'),
        ('451, 452, 453, 454, 455]', '452, 453, 454, 455, 456]'),
    ],
)

build(
    'generate-validate-five-hundred-forty.py',
    'generate-validate-five-hundred-forty-one.py',
    [
        ('five-hundred-forty', 'five-hundred-forty-one'),
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('all_cases[:525]', 'all_cases[:526]'),
        ('{UNKNOWN, TYPO}][:525]', '{UNKNOWN, TYPO}][:526]'),
        ('!= 525', '!= 526'),
        ('448, 449, 450, 451, 452]', '449, 450, 451, 452, 453]'),
    ],
)

build(
    'validate-five-hundred-forty-valid-list-cases.py',
    'validate-five-hundred-forty-one-valid-list-cases.py',
    [
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('510, 511, 512, 513, 514', '511, 512, 513, 514, 515'),
        ('all_cases[:525]', 'all_cases[:526]'),
        ('len(valid_cases) != 525', 'len(valid_cases) != 526'),
    ],
)

build(
    'validate-five-hundred-forty-valid-mixed.py',
    'validate-five-hundred-forty-one-valid-mixed.py',
    [
        ('vijfhonderdveertig', 'vijfhonderdeenenveertig'),
        ('510, 511, 512, 513, 514', '511, 512, 513, 514, 515'),
        ('][:525]', '][:526]'),
        ('len(valid_cases) != 525', 'len(valid_cases) != 526'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty.py').read_text()
verify_text = verify_src.replace('five-hundred-forty', 'five-hundred-forty-one')
(ROOT / 'verify-five-hundred-forty-one.py').write_text(verify_text)
print('verify-five-hundred-forty-one.py')
