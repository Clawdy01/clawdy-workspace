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
    'create-five-hundred-fifty-three-assets.py',
    'create-five-hundred-fifty-four-assets.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('[:538]', '[:539]'),
        ('!= 538', '!= 539'),
        ('kreeg 538', 'kreeg 539'),
        ('525, 526, 527, 528, 529]', '526, 527, 528, 529, 530]'),
    ],
)

build(
    'create-five-hundred-fifty-three-bootstrap.py',
    'create-five-hundred-fifty-four-bootstrap.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('all_cases[:538]', 'all_cases[:539]'),
        ('{UNKNOWN, TYPO}][:538]', '{UNKNOWN, TYPO}][:539]'),
        ('!= 538', '!= 539'),
        ('kreeg 538', 'kreeg 539'),
        ('521, 522, 523, 524, 525]', '522, 523, 524, 525, 526]'),
    ],
)

build(
    'create-five-hundred-fifty-three-minimal.py',
    'create-five-hundred-fifty-four-minimal.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('!= 538', '!= 539'),
        ('kreeg 538', 'kreeg 539'),
        ('521, 522, 523, 524, 525]', '522, 523, 524, 525, 526]'),
    ],
)

build(
    'make-five-hundred-fifty-three.py',
    'make-five-hundred-fifty-four.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('all_cases[:538]', 'all_cases[:539]'),
        ('{UNKNOWN, TYPO}][:538]', '{UNKNOWN, TYPO}][:539]'),
        ('!= 538', '!= 539'),
        ('461, 462, 463, 464, 465]', '462, 463, 464, 465, 466]'),
    ],
)

build(
    'create-five-hundred-fifty-three-files.py',
    'create-five-hundred-fifty-four-files.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('all_cases[:538]', 'all_cases[:539]'),
        ('{UNKNOWN, TYPO}][:538]', '{UNKNOWN, TYPO}][:539]'),
        ('!= 538', '!= 539'),
        ('461, 462, 463, 464, 465]', '462, 463, 464, 465, 466]'),
    ],
)

build(
    'create-five-hundred-fifty-three.py',
    'create-five-hundred-fifty-four.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('all_cases[:538]', 'all_cases[:539]'),
        ('{UNKNOWN, TYPO}][:538]', '{UNKNOWN, TYPO}][:539]'),
        ('!= 538', '!= 539'),
        ('464, 465, 466, 467, 468]', '465, 466, 467, 468, 469]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-three.py',
    'generate-validate-five-hundred-fifty-four.py',
    [
        ('five-hundred-fifty-three', 'five-hundred-fifty-four'),
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('all_cases[:538]', 'all_cases[:539]'),
        ('{UNKNOWN, TYPO}][:538]', '{UNKNOWN, TYPO}][:539]'),
        ('!= 538', '!= 539'),
        ('461, 462, 463, 464, 465]', '462, 463, 464, 465, 466]'),
    ],
)

build(
    'validate-five-hundred-fifty-three-valid-list-cases.py',
    'validate-five-hundred-fifty-four-valid-list-cases.py',
    [
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('523, 524, 525, 526, 527', '524, 525, 526, 527, 528'),
        ('all_cases[:538]', 'all_cases[:539]'),
        ('len(valid_cases) != 538', 'len(valid_cases) != 539'),
    ],
)

build(
    'validate-five-hundred-fifty-three-valid-mixed.py',
    'validate-five-hundred-fifty-four-valid-mixed.py',
    [
        ('vijfhonderddrieënvijftig', 'vijfhonderdvierenvijftig'),
        ('523, 524, 525, 526, 527', '524, 525, 526, 527, 528'),
        ('][:538]', '][:539]'),
        ('len(valid_cases) != 538', 'len(valid_cases) != 539'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-three.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-three', 'five-hundred-fifty-four')
(ROOT / 'verify-five-hundred-fifty-four.py').write_text(verify_text)
print('verify-five-hundred-fifty-four.py')
