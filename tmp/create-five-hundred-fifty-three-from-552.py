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
    'create-five-hundred-fifty-two-assets.py',
    'create-five-hundred-fifty-three-assets.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('[:537]', '[:538]'),
        ('!= 537', '!= 538'),
        ('kreeg 537', 'kreeg 538'),
        ('524, 525, 526, 527, 528]', '525, 526, 527, 528, 529]'),
    ],
)

build(
    'create-five-hundred-fifty-two-bootstrap.py',
    'create-five-hundred-fifty-three-bootstrap.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('all_cases[:537]', 'all_cases[:538]'),
        ('{UNKNOWN, TYPO}][:537]', '{UNKNOWN, TYPO}][:538]'),
        ('!= 537', '!= 538'),
        ('kreeg 537', 'kreeg 538'),
        ('520, 521, 522, 523, 524]', '521, 522, 523, 524, 525]'),
    ],
)

build(
    'create-five-hundred-fifty-two-minimal.py',
    'create-five-hundred-fifty-three-minimal.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('!= 537', '!= 538'),
        ('kreeg 537', 'kreeg 538'),
        ('520, 521, 522, 523, 524]', '521, 522, 523, 524, 525]'),
    ],
)

build(
    'make-five-hundred-fifty-two.py',
    'make-five-hundred-fifty-three.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('all_cases[:537]', 'all_cases[:538]'),
        ('{UNKNOWN, TYPO}][:537]', '{UNKNOWN, TYPO}][:538]'),
        ('!= 537', '!= 538'),
        ('460, 461, 462, 463, 464]', '461, 462, 463, 464, 465]'),
    ],
)

build(
    'create-five-hundred-fifty-two-files.py',
    'create-five-hundred-fifty-three-files.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('all_cases[:537]', 'all_cases[:538]'),
        ('{UNKNOWN, TYPO}][:537]', '{UNKNOWN, TYPO}][:538]'),
        ('!= 537', '!= 538'),
        ('460, 461, 462, 463, 464]', '461, 462, 463, 464, 465]'),
    ],
)

build(
    'create-five-hundred-fifty-two.py',
    'create-five-hundred-fifty-three.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('all_cases[:537]', 'all_cases[:538]'),
        ('{UNKNOWN, TYPO}][:537]', '{UNKNOWN, TYPO}][:538]'),
        ('!= 537', '!= 538'),
        ('463, 464, 465, 466, 467]', '464, 465, 466, 467, 468]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-two.py',
    'generate-validate-five-hundred-fifty-three.py',
    [
        ('five-hundred-fifty-two', 'five-hundred-fifty-three'),
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('all_cases[:537]', 'all_cases[:538]'),
        ('{UNKNOWN, TYPO}][:537]', '{UNKNOWN, TYPO}][:538]'),
        ('!= 537', '!= 538'),
        ('460, 461, 462, 463, 464]', '461, 462, 463, 464, 465]'),
    ],
)

build(
    'validate-five-hundred-fifty-two-valid-list-cases.py',
    'validate-five-hundred-fifty-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('522, 523, 524, 525, 526', '523, 524, 525, 526, 527'),
        ('all_cases[:537]', 'all_cases[:538]'),
        ('len(valid_cases) != 537', 'len(valid_cases) != 538'),
    ],
)

build(
    'validate-five-hundred-fifty-two-valid-mixed.py',
    'validate-five-hundred-fifty-three-valid-mixed.py',
    [
        ('vijfhonderdtweeënvijftig', 'vijfhonderddrieënvijftig'),
        ('522, 523, 524, 525, 526', '523, 524, 525, 526, 527'),
        ('][:537]', '][:538]'),
        ('len(valid_cases) != 537', 'len(valid_cases) != 538'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-two.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-two', 'five-hundred-fifty-three')
(ROOT / 'verify-five-hundred-fifty-three.py').write_text(verify_text)
print('verify-five-hundred-fifty-three.py')
