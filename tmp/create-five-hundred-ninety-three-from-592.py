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
    'create-five-hundred-ninety-two-assets.py',
    'create-five-hundred-ninety-three-assets.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('[:577]', '[:578]'),
        ('!= 577', '!= 578'),
        ('kreeg 577', 'kreeg 578'),
        ('564, 565, 566, 567, 568', '565, 566, 567, 568, 569'),
    ],
)

build(
    'create-five-hundred-ninety-two-bootstrap.py',
    'create-five-hundred-ninety-three-bootstrap.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('all_cases[:577]', 'all_cases[:578]'),
        ('{UNKNOWN, TYPO}][:577]', '{UNKNOWN, TYPO}][:578]'),
        ('!= 577', '!= 578'),
        ('kreeg 577', 'kreeg 578'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'create-five-hundred-ninety-two-minimal.py',
    'create-five-hundred-ninety-three-minimal.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('!= 577', '!= 578'),
        ('kreeg 577', 'kreeg 578'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'make-five-hundred-ninety-two.py',
    'make-five-hundred-ninety-three.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('all_cases[:577]', 'all_cases[:578]'),
        ('{UNKNOWN, TYPO}][:577]', '{UNKNOWN, TYPO}][:578]'),
        ('!= 577', '!= 578'),
        ('500, 501, 502, 503, 504', '501, 502, 503, 504, 505'),
    ],
)

build(
    'create-five-hundred-ninety-two-files.py',
    'create-five-hundred-ninety-three-files.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('all_cases[:577]', 'all_cases[:578]'),
        ('{UNKNOWN, TYPO}][:577]', '{UNKNOWN, TYPO}][:578]'),
        ('!= 577', '!= 578'),
        ('500, 501, 502, 503, 504', '501, 502, 503, 504, 505'),
    ],
)

build(
    'create-five-hundred-ninety-two.py',
    'create-five-hundred-ninety-three.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('all_cases[:577]', 'all_cases[:578]'),
        ('{UNKNOWN, TYPO}][:577]', '{UNKNOWN, TYPO}][:578]'),
        ('!= 577', '!= 578'),
        ('503, 504, 505, 506, 507', '504, 505, 506, 507, 508'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-two.py',
    'generate-validate-five-hundred-ninety-three.py',
    [
        ('five-hundred-ninety-two', 'five-hundred-ninety-three'),
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('all_cases[:577]', 'all_cases[:578]'),
        ('{UNKNOWN, TYPO}][:577]', '{UNKNOWN, TYPO}][:578]'),
        ('!= 577', '!= 578'),
        ('500, 501, 502, 503, 504', '501, 502, 503, 504, 505'),
    ],
)

build(
    'validate-five-hundred-ninety-two-valid-list-cases.py',
    'validate-five-hundred-ninety-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('562, 563, 564, 565, 566', '563, 564, 565, 566, 567'),
        ('all_cases[:577]', 'all_cases[:578]'),
        ('len(valid_cases) != 577', 'len(valid_cases) != 578'),
    ],
)

build(
    'validate-five-hundred-ninety-two-valid-mixed.py',
    'validate-five-hundred-ninety-three-valid-mixed.py',
    [
        ('vijfhonderdtweeënnegentig', 'vijfhonderddrieënnegentig'),
        ('562, 563, 564, 565, 566', '563, 564, 565, 566, 567'),
        ('][:577]', '][:578]'),
        ('len(valid_cases) != 577', 'len(valid_cases) != 578'),
        ('plain stderr noemt niet alle vijfhonderdzevenenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdachtenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-two.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-two', 'five-hundred-ninety-three')
(ROOT / 'verify-five-hundred-ninety-three.py').write_text(verify_text)
print('verify-five-hundred-ninety-three.py')
