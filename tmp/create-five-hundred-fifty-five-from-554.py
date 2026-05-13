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
    'create-five-hundred-fifty-four-assets.py',
    'create-five-hundred-fifty-five-assets.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('[:539]', '[:540]'),
        ('!= 539', '!= 540'),
        ('kreeg 539', 'kreeg 540'),
        ('526, 527, 528, 529, 530]', '527, 528, 529, 530, 531]'),
    ],
)

build(
    'create-five-hundred-fifty-four-bootstrap.py',
    'create-five-hundred-fifty-five-bootstrap.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('all_cases[:539]', 'all_cases[:540]'),
        ('{UNKNOWN, TYPO}][:539]', '{UNKNOWN, TYPO}][:540]'),
        ('!= 539', '!= 540'),
        ('kreeg 539', 'kreeg 540'),
        ('522, 523, 524, 525, 526]', '523, 524, 525, 526, 527]'),
    ],
)

build(
    'create-five-hundred-fifty-four-minimal.py',
    'create-five-hundred-fifty-five-minimal.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('!= 539', '!= 540'),
        ('kreeg 539', 'kreeg 540'),
        ('522, 523, 524, 525, 526]', '523, 524, 525, 526, 527]'),
    ],
)

build(
    'make-five-hundred-fifty-four.py',
    'make-five-hundred-fifty-five.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('all_cases[:539]', 'all_cases[:540]'),
        ('{UNKNOWN, TYPO}][:539]', '{UNKNOWN, TYPO}][:540]'),
        ('!= 539', '!= 540'),
        ('462, 463, 464, 465, 466]', '463, 464, 465, 466, 467]'),
    ],
)

build(
    'create-five-hundred-fifty-four-files.py',
    'create-five-hundred-fifty-five-files.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('all_cases[:539]', 'all_cases[:540]'),
        ('{UNKNOWN, TYPO}][:539]', '{UNKNOWN, TYPO}][:540]'),
        ('!= 539', '!= 540'),
        ('462, 463, 464, 465, 466]', '463, 464, 465, 466, 467]'),
    ],
)

build(
    'create-five-hundred-fifty-four.py',
    'create-five-hundred-fifty-five.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('all_cases[:539]', 'all_cases[:540]'),
        ('{UNKNOWN, TYPO}][:539]', '{UNKNOWN, TYPO}][:540]'),
        ('!= 539', '!= 540'),
        ('465, 466, 467, 468, 469]', '466, 467, 468, 469, 470]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-four.py',
    'generate-validate-five-hundred-fifty-five.py',
    [
        ('five-hundred-fifty-four', 'five-hundred-fifty-five'),
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('all_cases[:539]', 'all_cases[:540]'),
        ('{UNKNOWN, TYPO}][:539]', '{UNKNOWN, TYPO}][:540]'),
        ('!= 539', '!= 540'),
        ('462, 463, 464, 465, 466]', '463, 464, 465, 466, 467]'),
    ],
)

build(
    'validate-five-hundred-fifty-four-valid-list-cases.py',
    'validate-five-hundred-fifty-five-valid-list-cases.py',
    [
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('524, 525, 526, 527, 528', '525, 526, 527, 528, 529'),
        ('all_cases[:539]', 'all_cases[:540]'),
        ('len(valid_cases) != 539', 'len(valid_cases) != 540'),
    ],
)

build(
    'validate-five-hundred-fifty-four-valid-mixed.py',
    'validate-five-hundred-fifty-five-valid-mixed.py',
    [
        ('vijfhonderdvierenvijftig', 'vijfhonderdvijfenvijftig'),
        ('524, 525, 526, 527, 528', '525, 526, 527, 528, 529'),
        ('][:539]', '][:540]'),
        ('len(valid_cases) != 539', 'len(valid_cases) != 540'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-four.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-four', 'five-hundred-fifty-five')
(ROOT / 'verify-five-hundred-fifty-five.py').write_text(verify_text)
print('verify-five-hundred-fifty-five.py')
