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
    'create-five-hundred-forty-seven-assets.py',
    'create-five-hundred-forty-eight-assets.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('[:532]', '[:533]'),
        ('!= 532', '!= 533'),
        ('kreeg 532', 'kreeg 533'),
        ('519, 520, 521, 522, 523]', '520, 521, 522, 523, 524]'),
    ],
)

build(
    'create-five-hundred-forty-seven-bootstrap.py',
    'create-five-hundred-forty-eight-bootstrap.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('all_cases[:532]', 'all_cases[:533]'),
        ('{UNKNOWN, TYPO}][:532]', '{UNKNOWN, TYPO}][:533]'),
        ('!= 532', '!= 533'),
        ('kreeg 532', 'kreeg 533'),
        ('515, 516, 517, 518, 519]', '516, 517, 518, 519, 520]'),
    ],
)

build(
    'create-five-hundred-forty-seven-minimal.py',
    'create-five-hundred-forty-eight-minimal.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('!= 532', '!= 533'),
        ('kreeg 532', 'kreeg 533'),
        ('515, 516, 517, 518, 519]', '516, 517, 518, 519, 520]'),
    ],
)

build(
    'make-five-hundred-forty-seven.py',
    'make-five-hundred-forty-eight.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('all_cases[:532]', 'all_cases[:533]'),
        ('{UNKNOWN, TYPO}][:532]', '{UNKNOWN, TYPO}][:533]'),
        ('!= 532', '!= 533'),
        ('455, 456, 457, 458, 459]', '456, 457, 458, 459, 460]'),
    ],
)

build(
    'create-five-hundred-forty-seven-files.py',
    'create-five-hundred-forty-eight-files.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('all_cases[:532]', 'all_cases[:533]'),
        ('{UNKNOWN, TYPO}][:532]', '{UNKNOWN, TYPO}][:533]'),
        ('!= 532', '!= 533'),
        ('455, 456, 457, 458, 459]', '456, 457, 458, 459, 460]'),
    ],
)

build(
    'create-five-hundred-forty-seven.py',
    'create-five-hundred-forty-eight.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('all_cases[:532]', 'all_cases[:533]'),
        ('{UNKNOWN, TYPO}][:532]', '{UNKNOWN, TYPO}][:533]'),
        ('!= 532', '!= 533'),
        ('458, 459, 460, 461, 462]', '459, 460, 461, 462, 463]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-seven.py',
    'generate-validate-five-hundred-forty-eight.py',
    [
        ('five-hundred-forty-seven', 'five-hundred-forty-eight'),
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('all_cases[:532]', 'all_cases[:533]'),
        ('{UNKNOWN, TYPO}][:532]', '{UNKNOWN, TYPO}][:533]'),
        ('!= 532', '!= 533'),
        ('455, 456, 457, 458, 459]', '456, 457, 458, 459, 460]'),
    ],
)

build(
    'validate-five-hundred-forty-seven-valid-list-cases.py',
    'validate-five-hundred-forty-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('517, 518, 519, 520, 521', '518, 519, 520, 521, 522'),
        ('all_cases[:532]', 'all_cases[:533]'),
        ('len(valid_cases) != 532', 'len(valid_cases) != 533'),
    ],
)

build(
    'validate-five-hundred-forty-seven-valid-mixed.py',
    'validate-five-hundred-forty-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenenveertig', 'vijfhonderdachtenveertig'),
        ('517, 518, 519, 520, 521', '518, 519, 520, 521, 522'),
        ('][:532]', '][:533]'),
        ('len(valid_cases) != 532', 'len(valid_cases) != 533'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-seven', 'five-hundred-forty-eight')
(ROOT / 'verify-five-hundred-forty-eight.py').write_text(verify_text)
print('verify-five-hundred-forty-eight.py')
