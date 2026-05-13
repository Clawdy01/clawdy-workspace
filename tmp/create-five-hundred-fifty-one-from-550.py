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
    'create-five-hundred-fifty-assets.py',
    'create-five-hundred-fifty-one-assets.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('[:535]', '[:536]'),
        ('!= 535', '!= 536'),
        ('kreeg 535', 'kreeg 536'),
        ('522, 523, 524, 525, 526]', '523, 524, 525, 526, 527]'),
    ],
)

build(
    'create-five-hundred-fifty-bootstrap.py',
    'create-five-hundred-fifty-one-bootstrap.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('all_cases[:535]', 'all_cases[:536]'),
        ('{UNKNOWN, TYPO}][:535]', '{UNKNOWN, TYPO}][:536]'),
        ('!= 535', '!= 536'),
        ('kreeg 535', 'kreeg 536'),
        ('518, 519, 520, 521, 522]', '519, 520, 521, 522, 523]'),
    ],
)

build(
    'create-five-hundred-fifty-minimal.py',
    'create-five-hundred-fifty-one-minimal.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('!= 535', '!= 536'),
        ('kreeg 535', 'kreeg 536'),
        ('518, 519, 520, 521, 522]', '519, 520, 521, 522, 523]'),
    ],
)

build(
    'make-five-hundred-fifty.py',
    'make-five-hundred-fifty-one.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('all_cases[:535]', 'all_cases[:536]'),
        ('{UNKNOWN, TYPO}][:535]', '{UNKNOWN, TYPO}][:536]'),
        ('!= 535', '!= 536'),
        ('458, 459, 460, 461, 462]', '459, 460, 461, 462, 463]'),
    ],
)

build(
    'create-five-hundred-fifty-files.py',
    'create-five-hundred-fifty-one-files.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('all_cases[:535]', 'all_cases[:536]'),
        ('{UNKNOWN, TYPO}][:535]', '{UNKNOWN, TYPO}][:536]'),
        ('!= 535', '!= 536'),
        ('458, 459, 460, 461, 462]', '459, 460, 461, 462, 463]'),
    ],
)

build(
    'create-five-hundred-fifty.py',
    'create-five-hundred-fifty-one.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('all_cases[:535]', 'all_cases[:536]'),
        ('{UNKNOWN, TYPO}][:535]', '{UNKNOWN, TYPO}][:536]'),
        ('!= 535', '!= 536'),
        ('461, 462, 463, 464, 465]', '462, 463, 464, 465, 466]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty.py',
    'generate-validate-five-hundred-fifty-one.py',
    [
        ('five-hundred-fifty', 'five-hundred-fifty-one'),
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('all_cases[:535]', 'all_cases[:536]'),
        ('{UNKNOWN, TYPO}][:535]', '{UNKNOWN, TYPO}][:536]'),
        ('!= 535', '!= 536'),
        ('458, 459, 460, 461, 462]', '459, 460, 461, 462, 463]'),
    ],
)

build(
    'validate-five-hundred-fifty-valid-list-cases.py',
    'validate-five-hundred-fifty-one-valid-list-cases.py',
    [
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('520, 521, 522, 523, 524', '521, 522, 523, 524, 525'),
        ('all_cases[:535]', 'all_cases[:536]'),
        ('len(valid_cases) != 535', 'len(valid_cases) != 536'),
    ],
)

build(
    'validate-five-hundred-fifty-valid-mixed.py',
    'validate-five-hundred-fifty-one-valid-mixed.py',
    [
        ('vijfhonderdvijftig', 'vijfhonderdeenenvijftig'),
        ('520, 521, 522, 523, 524', '521, 522, 523, 524, 525'),
        ('][:535]', '][:536]'),
        ('len(valid_cases) != 535', 'len(valid_cases) != 536'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty', 'five-hundred-fifty-one')
(ROOT / 'verify-five-hundred-fifty-one.py').write_text(verify_text)
print('verify-five-hundred-fifty-one.py')
