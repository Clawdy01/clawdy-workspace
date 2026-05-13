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
    'create-five-hundred-fifty-six-assets.py',
    'create-five-hundred-fifty-seven-assets.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('[:541]', '[:542]'),
        ('!= 541', '!= 542'),
        ('kreeg 541', 'kreeg 542'),
        ('528, 529, 530, 531, 532]', '529, 530, 531, 532, 533]'),
    ],
)

build(
    'create-five-hundred-fifty-six-bootstrap.py',
    'create-five-hundred-fifty-seven-bootstrap.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('all_cases[:541]', 'all_cases[:542]'),
        ('{UNKNOWN, TYPO}][:541]', '{UNKNOWN, TYPO}][:542]'),
        ('!= 541', '!= 542'),
        ('kreeg 541', 'kreeg 542'),
        ('524, 525, 526, 527, 528]', '525, 526, 527, 528, 529]'),
    ],
)

build(
    'create-five-hundred-fifty-six-minimal.py',
    'create-five-hundred-fifty-seven-minimal.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('!= 541', '!= 542'),
        ('kreeg 541', 'kreeg 542'),
        ('524, 525, 526, 527, 528]', '525, 526, 527, 528, 529]'),
    ],
)

build(
    'make-five-hundred-fifty-six.py',
    'make-five-hundred-fifty-seven.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('all_cases[:541]', 'all_cases[:542]'),
        ('{UNKNOWN, TYPO}][:541]', '{UNKNOWN, TYPO}][:542]'),
        ('!= 541', '!= 542'),
        ('464, 465, 466, 467, 468]', '465, 466, 467, 468, 469]'),
    ],
)

build(
    'create-five-hundred-fifty-six-files.py',
    'create-five-hundred-fifty-seven-files.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('all_cases[:541]', 'all_cases[:542]'),
        ('{UNKNOWN, TYPO}][:541]', '{UNKNOWN, TYPO}][:542]'),
        ('!= 541', '!= 542'),
        ('464, 465, 466, 467, 468]', '465, 466, 467, 468, 469]'),
    ],
)

build(
    'create-five-hundred-fifty-six.py',
    'create-five-hundred-fifty-seven.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('all_cases[:541]', 'all_cases[:542]'),
        ('{UNKNOWN, TYPO}][:541]', '{UNKNOWN, TYPO}][:542]'),
        ('!= 541', '!= 542'),
        ('467, 468, 469, 470, 471]', '468, 469, 470, 471, 472]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-six.py',
    'generate-validate-five-hundred-fifty-seven.py',
    [
        ('five-hundred-fifty-six', 'five-hundred-fifty-seven'),
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('all_cases[:541]', 'all_cases[:542]'),
        ('{UNKNOWN, TYPO}][:541]', '{UNKNOWN, TYPO}][:542]'),
        ('!= 541', '!= 542'),
        ('464, 465, 466, 467, 468]', '465, 466, 467, 468, 469]'),
    ],
)

build(
    'validate-five-hundred-fifty-six-valid-list-cases.py',
    'validate-five-hundred-fifty-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('526, 527, 528, 529, 530', '527, 528, 529, 530, 531'),
        ('all_cases[:541]', 'all_cases[:542]'),
        ('len(valid_cases) != 541', 'len(valid_cases) != 542'),
    ],
)

build(
    'validate-five-hundred-fifty-six-valid-mixed.py',
    'validate-five-hundred-fifty-seven-valid-mixed.py',
    [
        ('vijfhonderdzesenvijftig', 'vijfhonderdzevenenvijftig'),
        ('526, 527, 528, 529, 530', '527, 528, 529, 530, 531'),
        ('][:541]', '][:542]'),
        ('len(valid_cases) != 541', 'len(valid_cases) != 542'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-six.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-six', 'five-hundred-fifty-seven')
(ROOT / 'verify-five-hundred-fifty-seven.py').write_text(verify_text)
print('verify-five-hundred-fifty-seven.py')
