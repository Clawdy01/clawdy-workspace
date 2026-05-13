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
    'create-five-hundred-fifty-one-assets.py',
    'create-five-hundred-fifty-two-assets.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('[:536]', '[:537]'),
        ('!= 536', '!= 537'),
        ('kreeg 536', 'kreeg 537'),
        ('523, 524, 525, 526, 527]', '524, 525, 526, 527, 528]'),
    ],
)

build(
    'create-five-hundred-fifty-one-bootstrap.py',
    'create-five-hundred-fifty-two-bootstrap.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('all_cases[:536]', 'all_cases[:537]'),
        ('{UNKNOWN, TYPO}][:536]', '{UNKNOWN, TYPO}][:537]'),
        ('!= 536', '!= 537'),
        ('kreeg 536', 'kreeg 537'),
        ('519, 520, 521, 522, 523]', '520, 521, 522, 523, 524]'),
    ],
)

build(
    'create-five-hundred-fifty-one-minimal.py',
    'create-five-hundred-fifty-two-minimal.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('!= 536', '!= 537'),
        ('kreeg 536', 'kreeg 537'),
        ('519, 520, 521, 522, 523]', '520, 521, 522, 523, 524]'),
    ],
)

build(
    'make-five-hundred-fifty-one.py',
    'make-five-hundred-fifty-two.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('all_cases[:536]', 'all_cases[:537]'),
        ('{UNKNOWN, TYPO}][:536]', '{UNKNOWN, TYPO}][:537]'),
        ('!= 536', '!= 537'),
        ('459, 460, 461, 462, 463]', '460, 461, 462, 463, 464]'),
    ],
)

build(
    'create-five-hundred-fifty-one-files.py',
    'create-five-hundred-fifty-two-files.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('all_cases[:536]', 'all_cases[:537]'),
        ('{UNKNOWN, TYPO}][:536]', '{UNKNOWN, TYPO}][:537]'),
        ('!= 536', '!= 537'),
        ('459, 460, 461, 462, 463]', '460, 461, 462, 463, 464]'),
    ],
)

build(
    'create-five-hundred-fifty-one.py',
    'create-five-hundred-fifty-two.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('all_cases[:536]', 'all_cases[:537]'),
        ('{UNKNOWN, TYPO}][:536]', '{UNKNOWN, TYPO}][:537]'),
        ('!= 536', '!= 537'),
        ('462, 463, 464, 465, 466]', '463, 464, 465, 466, 467]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-one.py',
    'generate-validate-five-hundred-fifty-two.py',
    [
        ('five-hundred-fifty-one', 'five-hundred-fifty-two'),
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('all_cases[:536]', 'all_cases[:537]'),
        ('{UNKNOWN, TYPO}][:536]', '{UNKNOWN, TYPO}][:537]'),
        ('!= 536', '!= 537'),
        ('459, 460, 461, 462, 463]', '460, 461, 462, 463, 464]'),
    ],
)

build(
    'validate-five-hundred-fifty-one-valid-list-cases.py',
    'validate-five-hundred-fifty-two-valid-list-cases.py',
    [
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('521, 522, 523, 524, 525', '522, 523, 524, 525, 526'),
        ('all_cases[:536]', 'all_cases[:537]'),
        ('len(valid_cases) != 536', 'len(valid_cases) != 537'),
    ],
)

build(
    'validate-five-hundred-fifty-one-valid-mixed.py',
    'validate-five-hundred-fifty-two-valid-mixed.py',
    [
        ('vijfhonderdeenenvijftig', 'vijfhonderdtweeënvijftig'),
        ('521, 522, 523, 524, 525', '522, 523, 524, 525, 526'),
        ('][:536]', '][:537]'),
        ('len(valid_cases) != 536', 'len(valid_cases) != 537'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-one.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-one', 'five-hundred-fifty-two')
(ROOT / 'verify-five-hundred-fifty-two.py').write_text(verify_text)
print('verify-five-hundred-fifty-two.py')
