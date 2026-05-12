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
    'create-five-hundred-thirty-nine-assets.py',
    'create-five-hundred-forty-assets.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('[:524]', '[:525]'),
        ('!= 524', '!= 525'),
        ('kreeg 524', 'kreeg 525'),
        ('512, 513, 514, 515]', '512, 513, 514, 515, 516]'),
    ],
)

build(
    'create-five-hundred-thirty-nine-bootstrap.py',
    'create-five-hundred-forty-bootstrap.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('all_cases[:524]', 'all_cases[:525]'),
        ('{UNKNOWN, TYPO}][:524]', '{UNKNOWN, TYPO}][:525]'),
        ('!= 524', '!= 525'),
        ('kreeg 524', 'kreeg 525'),
        ('508, 509, 510, 511]', '508, 509, 510, 511, 512]'),
    ],
)

build(
    'create-five-hundred-thirty-nine-minimal.py',
    'create-five-hundred-forty-minimal.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('!= 524', '!= 525'),
        ('kreeg 524', 'kreeg 525'),
        ('508, 509, 510, 511]', '508, 509, 510, 511, 512]'),
    ],
)

build(
    'make-five-hundred-thirty-nine.py',
    'make-five-hundred-forty.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('all_cases[:524]', 'all_cases[:525]'),
        ('{UNKNOWN, TYPO}][:524]', '{UNKNOWN, TYPO}][:525]'),
        ('!= 524', '!= 525'),
        ('448, 449, 450, 451]', '448, 449, 450, 451, 452]'),
    ],
)

build(
    'create-five-hundred-thirty-nine-files.py',
    'create-five-hundred-forty-files.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('all_cases[:524]', 'all_cases[:525]'),
        ('{UNKNOWN, TYPO}][:524]', '{UNKNOWN, TYPO}][:525]'),
        ('!= 524', '!= 525'),
        ('448, 449, 450, 451]', '448, 449, 450, 451, 452]'),
    ],
)

build(
    'create-five-hundred-thirty-nine.py',
    'create-five-hundred-forty.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('all_cases[:524]', 'all_cases[:525]'),
        ('{UNKNOWN, TYPO}][:524]', '{UNKNOWN, TYPO}][:525]'),
        ('!= 524', '!= 525'),
        ('451, 452, 453, 454]', '451, 452, 453, 454, 455]'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-nine.py',
    'generate-validate-five-hundred-forty.py',
    [
        ('five-hundred-thirty-nine', 'five-hundred-forty'),
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('all_cases[:524]', 'all_cases[:525]'),
        ('{UNKNOWN, TYPO}][:524]', '{UNKNOWN, TYPO}][:525]'),
        ('!= 524', '!= 525'),
        ('448, 449, 450, 451]', '448, 449, 450, 451, 452]'),
    ],
)

build(
    'validate-five-hundred-thirty-nine-valid-list-cases.py',
    'validate-five-hundred-forty-valid-list-cases.py',
    [
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('510, 511, 512, 513', '510, 511, 512, 513, 514'),
        ('all_cases[:524]', 'all_cases[:525]'),
        ('len(valid_cases) != 524', 'len(valid_cases) != 525'),
    ],
)

build(
    'validate-five-hundred-thirty-nine-valid-mixed.py',
    'validate-five-hundred-forty-valid-mixed.py',
    [
        ('vijfhonderdnegenendertig', 'vijfhonderdveertig'),
        ('510, 511, 512, 513', '510, 511, 512, 513, 514'),
        ('][:524]', '][:525]'),
        ('len(valid_cases) != 524', 'len(valid_cases) != 525'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-nine', 'five-hundred-forty')
(ROOT / 'verify-five-hundred-forty.py').write_text(verify_text)
print('verify-five-hundred-forty.py')
