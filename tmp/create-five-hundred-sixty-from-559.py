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
    'create-five-hundred-fifty-nine-assets.py',
    'create-five-hundred-sixty-assets.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('[:544]', '[:545]'),
        ('!= 544', '!= 545'),
        ('kreeg 544', 'kreeg 545'),
        ('531, 532, 533, 534, 535]', '532, 533, 534, 535, 536]'),
    ],
)

build(
    'create-five-hundred-fifty-nine-bootstrap.py',
    'create-five-hundred-sixty-bootstrap.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('all_cases[:544]', 'all_cases[:545]'),
        ('{UNKNOWN, TYPO}][:544]', '{UNKNOWN, TYPO}][:545]'),
        ('!= 544', '!= 545'),
        ('kreeg 544', 'kreeg 545'),
        ('527, 528, 529, 530, 531]', '528, 529, 530, 531, 532]'),
    ],
)

build(
    'create-five-hundred-fifty-nine-minimal.py',
    'create-five-hundred-sixty-minimal.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('!= 544', '!= 545'),
        ('kreeg 544', 'kreeg 545'),
        ('527, 528, 529, 530, 531]', '528, 529, 530, 531, 532]'),
    ],
)

build(
    'make-five-hundred-fifty-nine.py',
    'make-five-hundred-sixty.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('all_cases[:544]', 'all_cases[:545]'),
        ('{UNKNOWN, TYPO}][:544]', '{UNKNOWN, TYPO}][:545]'),
        ('!= 544', '!= 545'),
        ('467, 468, 469, 470, 471]', '468, 469, 470, 471, 472]'),
    ],
)

build(
    'create-five-hundred-fifty-nine-files.py',
    'create-five-hundred-sixty-files.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('all_cases[:544]', 'all_cases[:545]'),
        ('{UNKNOWN, TYPO}][:544]', '{UNKNOWN, TYPO}][:545]'),
        ('!= 544', '!= 545'),
        ('467, 468, 469, 470, 471]', '468, 469, 470, 471, 472]'),
    ],
)

build(
    'create-five-hundred-fifty-nine.py',
    'create-five-hundred-sixty.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('all_cases[:544]', 'all_cases[:545]'),
        ('{UNKNOWN, TYPO}][:544]', '{UNKNOWN, TYPO}][:545]'),
        ('!= 544', '!= 545'),
        ('470, 471, 472, 473, 474]', '471, 472, 473, 474, 475]'),
    ],
)

build(
    'generate-validate-five-hundred-fifty-nine.py',
    'generate-validate-five-hundred-sixty.py',
    [
        ('five-hundred-fifty-nine', 'five-hundred-sixty'),
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('all_cases[:544]', 'all_cases[:545]'),
        ('{UNKNOWN, TYPO}][:544]', '{UNKNOWN, TYPO}][:545]'),
        ('!= 544', '!= 545'),
        ('467, 468, 469, 470, 471]', '468, 469, 470, 471, 472]'),
    ],
)

build(
    'validate-five-hundred-fifty-nine-valid-list-cases.py',
    'validate-five-hundred-sixty-valid-list-cases.py',
    [
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
        ('all_cases[:544]', 'all_cases[:545]'),
        ('len(valid_cases) != 544', 'len(valid_cases) != 545'),
    ],
)

build(
    'validate-five-hundred-fifty-nine-valid-mixed.py',
    'validate-five-hundred-sixty-valid-mixed.py',
    [
        ('vijfhonderdnegenenvijftig', 'vijfhonderdzestig'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
        ('][:544]', '][:545]'),
        ('len(valid_cases) != 544', 'len(valid_cases) != 545'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-fifty-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-fifty-nine', 'five-hundred-sixty')
(ROOT / 'verify-five-hundred-sixty.py').write_text(verify_text)
print('verify-five-hundred-sixty.py')
