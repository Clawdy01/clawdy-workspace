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
    'create-five-hundred-ninety-three-assets.py',
    'create-five-hundred-ninety-four-assets.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('[:578]', '[:579]'),
        ('!= 578', '!= 579'),
        ('kreeg 578', 'kreeg 579'),
        ('565, 566, 567, 568, 569', '566, 567, 568, 569, 570'),
    ],
)

build(
    'create-five-hundred-ninety-three-bootstrap.py',
    'create-five-hundred-ninety-four-bootstrap.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('all_cases[:578]', 'all_cases[:579]'),
        ('{UNKNOWN, TYPO}][:578]', '{UNKNOWN, TYPO}][:579]'),
        ('!= 578', '!= 579'),
        ('kreeg 578', 'kreeg 579'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'create-five-hundred-ninety-three-minimal.py',
    'create-five-hundred-ninety-four-minimal.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('!= 578', '!= 579'),
        ('kreeg 578', 'kreeg 579'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'make-five-hundred-ninety-three.py',
    'make-five-hundred-ninety-four.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('all_cases[:578]', 'all_cases[:579]'),
        ('{UNKNOWN, TYPO}][:578]', '{UNKNOWN, TYPO}][:579]'),
        ('!= 578', '!= 579'),
        ('501, 502, 503, 504, 505', '502, 503, 504, 505, 506'),
    ],
)

build(
    'create-five-hundred-ninety-three-files.py',
    'create-five-hundred-ninety-four-files.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('all_cases[:578]', 'all_cases[:579]'),
        ('{UNKNOWN, TYPO}][:578]', '{UNKNOWN, TYPO}][:579]'),
        ('!= 578', '!= 579'),
        ('501, 502, 503, 504, 505', '502, 503, 504, 505, 506'),
    ],
)

build(
    'create-five-hundred-ninety-three.py',
    'create-five-hundred-ninety-four.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('all_cases[:578]', 'all_cases[:579]'),
        ('{UNKNOWN, TYPO}][:578]', '{UNKNOWN, TYPO}][:579]'),
        ('!= 578', '!= 579'),
        ('504, 505, 506, 507, 508', '505, 506, 507, 508, 509'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-three.py',
    'generate-validate-five-hundred-ninety-four.py',
    [
        ('five-hundred-ninety-three', 'five-hundred-ninety-four'),
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('all_cases[:578]', 'all_cases[:579]'),
        ('{UNKNOWN, TYPO}][:578]', '{UNKNOWN, TYPO}][:579]'),
        ('!= 578', '!= 579'),
        ('501, 502, 503, 504, 505', '502, 503, 504, 505, 506'),
    ],
)

build(
    'validate-five-hundred-ninety-three-valid-list-cases.py',
    'validate-five-hundred-ninety-four-valid-list-cases.py',
    [
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('563, 564, 565, 566, 567', '564, 565, 566, 567, 568'),
        ('all_cases[:578]', 'all_cases[:579]'),
        ('len(valid_cases) != 578', 'len(valid_cases) != 579'),
    ],
)

build(
    'validate-five-hundred-ninety-three-valid-mixed.py',
    'validate-five-hundred-ninety-four-valid-mixed.py',
    [
        ('vijfhonderddrieënnegentig', 'vijfhonderdvierennegentig'),
        ('563, 564, 565, 566, 567', '564, 565, 566, 567, 568'),
        ('][:578]', '][:579]'),
        ('len(valid_cases) != 578', 'len(valid_cases) != 579'),
        ('plain stderr noemt niet alle vijfhonderdachtenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdnegenenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-three.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-three', 'five-hundred-ninety-four')
(ROOT / 'verify-five-hundred-ninety-four.py').write_text(verify_text)
print('verify-five-hundred-ninety-four.py')
