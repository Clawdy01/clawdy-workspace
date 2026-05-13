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
    'create-five-hundred-eighty-three-assets.py',
    'create-five-hundred-eighty-four-assets.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('[:568]', '[:569]'),
        ('!= 568', '!= 569'),
        ('kreeg 568', 'kreeg 569'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'create-five-hundred-eighty-three-bootstrap.py',
    'create-five-hundred-eighty-four-bootstrap.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('all_cases[:568]', 'all_cases[:569]'),
        ('{UNKNOWN, TYPO}][:568]', '{UNKNOWN, TYPO}][:569]'),
        ('!= 568', '!= 569'),
        ('kreeg 568', 'kreeg 569'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'create-five-hundred-eighty-three-minimal.py',
    'create-five-hundred-eighty-four-minimal.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('!= 568', '!= 569'),
        ('kreeg 568', 'kreeg 569'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'make-five-hundred-eighty-three.py',
    'make-five-hundred-eighty-four.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('all_cases[:568]', 'all_cases[:569]'),
        ('{UNKNOWN, TYPO}][:568]', '{UNKNOWN, TYPO}][:569]'),
        ('!= 568', '!= 569'),
        ('491, 492, 493, 494, 495', '492, 493, 494, 495, 496'),
    ],
)

build(
    'create-five-hundred-eighty-three-files.py',
    'create-five-hundred-eighty-four-files.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('all_cases[:568]', 'all_cases[:569]'),
        ('{UNKNOWN, TYPO}][:568]', '{UNKNOWN, TYPO}][:569]'),
        ('!= 568', '!= 569'),
        ('491, 492, 493, 494, 495', '492, 493, 494, 495, 496'),
    ],
)

build(
    'create-five-hundred-eighty-three.py',
    'create-five-hundred-eighty-four.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('all_cases[:568]', 'all_cases[:569]'),
        ('{UNKNOWN, TYPO}][:568]', '{UNKNOWN, TYPO}][:569]'),
        ('!= 568', '!= 569'),
        ('494, 495, 496, 497, 498', '495, 496, 497, 498, 499'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-three.py',
    'generate-validate-five-hundred-eighty-four.py',
    [
        ('five-hundred-eighty-three', 'five-hundred-eighty-four'),
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('all_cases[:568]', 'all_cases[:569]'),
        ('{UNKNOWN, TYPO}][:568]', '{UNKNOWN, TYPO}][:569]'),
        ('!= 568', '!= 569'),
        ('491, 492, 493, 494, 495', '492, 493, 494, 495, 496'),
    ],
)

build(
    'validate-five-hundred-eighty-three-valid-list-cases.py',
    'validate-five-hundred-eighty-four-valid-list-cases.py',
    [
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
        ('all_cases[:568]', 'all_cases[:569]'),
        ('len(valid_cases) != 568', 'len(valid_cases) != 569'),
    ],
)

build(
    'validate-five-hundred-eighty-three-valid-mixed.py',
    'validate-five-hundred-eighty-four-valid-mixed.py',
    [
        ('vijfhonderddrieëntachtig', 'vijfhonderdvierentachtig'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
        ('][:568]', '][:569]'),
        ('len(valid_cases) != 568', 'len(valid_cases) != 569'),
        ('plain stderr noemt niet alle vijfhonderdachtenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdnegenenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-three.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-three', 'five-hundred-eighty-four')
(ROOT / 'verify-five-hundred-eighty-four.py').write_text(verify_text)
print('verify-five-hundred-eighty-four.py')
