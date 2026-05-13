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
    'create-five-hundred-forty-eight-assets.py',
    'create-five-hundred-forty-nine-assets.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('[:533]', '[:534]'),
        ('!= 533', '!= 534'),
        ('kreeg 533', 'kreeg 534'),
        ('520, 521, 522, 523, 524]', '521, 522, 523, 524, 525]'),
    ],
)

build(
    'create-five-hundred-forty-eight-bootstrap.py',
    'create-five-hundred-forty-nine-bootstrap.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('all_cases[:533]', 'all_cases[:534]'),
        ('{UNKNOWN, TYPO}][:533]', '{UNKNOWN, TYPO}][:534]'),
        ('!= 533', '!= 534'),
        ('kreeg 533', 'kreeg 534'),
        ('516, 517, 518, 519, 520]', '517, 518, 519, 520, 521]'),
    ],
)

build(
    'create-five-hundred-forty-eight-minimal.py',
    'create-five-hundred-forty-nine-minimal.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('!= 533', '!= 534'),
        ('kreeg 533', 'kreeg 534'),
        ('516, 517, 518, 519, 520]', '517, 518, 519, 520, 521]'),
    ],
)

build(
    'make-five-hundred-forty-eight.py',
    'make-five-hundred-forty-nine.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('all_cases[:533]', 'all_cases[:534]'),
        ('{UNKNOWN, TYPO}][:533]', '{UNKNOWN, TYPO}][:534]'),
        ('!= 533', '!= 534'),
        ('456, 457, 458, 459, 460]', '457, 458, 459, 460, 461]'),
    ],
)

build(
    'create-five-hundred-forty-eight-files.py',
    'create-five-hundred-forty-nine-files.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('all_cases[:533]', 'all_cases[:534]'),
        ('{UNKNOWN, TYPO}][:533]', '{UNKNOWN, TYPO}][:534]'),
        ('!= 533', '!= 534'),
        ('456, 457, 458, 459, 460]', '457, 458, 459, 460, 461]'),
    ],
)

build(
    'create-five-hundred-forty-eight.py',
    'create-five-hundred-forty-nine.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('all_cases[:533]', 'all_cases[:534]'),
        ('{UNKNOWN, TYPO}][:533]', '{UNKNOWN, TYPO}][:534]'),
        ('!= 533', '!= 534'),
        ('459, 460, 461, 462, 463]', '460, 461, 462, 463, 464]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-eight.py',
    'generate-validate-five-hundred-forty-nine.py',
    [
        ('five-hundred-forty-eight', 'five-hundred-forty-nine'),
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('all_cases[:533]', 'all_cases[:534]'),
        ('{UNKNOWN, TYPO}][:533]', '{UNKNOWN, TYPO}][:534]'),
        ('!= 533', '!= 534'),
        ('456, 457, 458, 459, 460]', '457, 458, 459, 460, 461]'),
    ],
)

build(
    'validate-five-hundred-forty-eight-valid-list-cases.py',
    'validate-five-hundred-forty-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('518, 519, 520, 521, 522', '519, 520, 521, 522, 523'),
        ('all_cases[:533]', 'all_cases[:534]'),
        ('len(valid_cases) != 533', 'len(valid_cases) != 534'),
    ],
)

build(
    'validate-five-hundred-forty-eight-valid-mixed.py',
    'validate-five-hundred-forty-nine-valid-mixed.py',
    [
        ('vijfhonderdachtenveertig', 'vijfhonderdnegenenveertig'),
        ('518, 519, 520, 521, 522', '519, 520, 521, 522, 523'),
        ('][:533]', '][:534]'),
        ('len(valid_cases) != 533', 'len(valid_cases) != 534'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-eight', 'five-hundred-forty-nine')
(ROOT / 'verify-five-hundred-forty-nine.py').write_text(verify_text)
print('verify-five-hundred-forty-nine.py')
