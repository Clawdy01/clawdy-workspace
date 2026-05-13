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
    'create-five-hundred-forty-nine-assets.py',
    'create-five-hundred-fifty-assets.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('[:534]', '[:535]'),
        ('!= 534', '!= 535'),
        ('kreeg 534', 'kreeg 535'),
        ('521, 522, 523, 524, 525]', '522, 523, 524, 525, 526]'),
    ],
)

build(
    'create-five-hundred-forty-nine-bootstrap.py',
    'create-five-hundred-fifty-bootstrap.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('all_cases[:534]', 'all_cases[:535]'),
        ('{UNKNOWN, TYPO}][:534]', '{UNKNOWN, TYPO}][:535]'),
        ('!= 534', '!= 535'),
        ('kreeg 534', 'kreeg 535'),
        ('517, 518, 519, 520, 521]', '518, 519, 520, 521, 522]'),
    ],
)

build(
    'create-five-hundred-forty-nine-minimal.py',
    'create-five-hundred-fifty-minimal.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('!= 534', '!= 535'),
        ('kreeg 534', 'kreeg 535'),
        ('517, 518, 519, 520, 521]', '518, 519, 520, 521, 522]'),
    ],
)

build(
    'make-five-hundred-forty-nine.py',
    'make-five-hundred-fifty.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('all_cases[:534]', 'all_cases[:535]'),
        ('{UNKNOWN, TYPO}][:534]', '{UNKNOWN, TYPO}][:535]'),
        ('!= 534', '!= 535'),
        ('457, 458, 459, 460, 461]', '458, 459, 460, 461, 462]'),
    ],
)

build(
    'create-five-hundred-forty-nine-files.py',
    'create-five-hundred-fifty-files.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('all_cases[:534]', 'all_cases[:535]'),
        ('{UNKNOWN, TYPO}][:534]', '{UNKNOWN, TYPO}][:535]'),
        ('!= 534', '!= 535'),
        ('457, 458, 459, 460, 461]', '458, 459, 460, 461, 462]'),
    ],
)

build(
    'create-five-hundred-forty-nine.py',
    'create-five-hundred-fifty.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('all_cases[:534]', 'all_cases[:535]'),
        ('{UNKNOWN, TYPO}][:534]', '{UNKNOWN, TYPO}][:535]'),
        ('!= 534', '!= 535'),
        ('460, 461, 462, 463, 464]', '461, 462, 463, 464, 465]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-nine.py',
    'generate-validate-five-hundred-fifty.py',
    [
        ('five-hundred-forty-nine', 'five-hundred-fifty'),
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('all_cases[:534]', 'all_cases[:535]'),
        ('{UNKNOWN, TYPO}][:534]', '{UNKNOWN, TYPO}][:535]'),
        ('!= 534', '!= 535'),
        ('457, 458, 459, 460, 461]', '458, 459, 460, 461, 462]'),
    ],
)

build(
    'validate-five-hundred-forty-nine-valid-list-cases.py',
    'validate-five-hundred-fifty-valid-list-cases.py',
    [
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('519, 520, 521, 522, 523', '520, 521, 522, 523, 524'),
        ('all_cases[:534]', 'all_cases[:535]'),
        ('len(valid_cases) != 534', 'len(valid_cases) != 535'),
    ],
)

build(
    'validate-five-hundred-forty-nine-valid-mixed.py',
    'validate-five-hundred-fifty-valid-mixed.py',
    [
        ('vijfhonderdnegenenveertig', 'vijfhonderdvijftig'),
        ('519, 520, 521, 522, 523', '520, 521, 522, 523, 524'),
        ('][:534]', '][:535]'),
        ('len(valid_cases) != 534', 'len(valid_cases) != 535'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-nine', 'five-hundred-fifty')
(ROOT / 'verify-five-hundred-fifty.py').write_text(verify_text)
print('verify-five-hundred-fifty.py')
