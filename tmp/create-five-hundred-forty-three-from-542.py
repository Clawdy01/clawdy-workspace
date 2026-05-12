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
    'create-five-hundred-forty-two-assets.py',
    'create-five-hundred-forty-three-assets.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('[:527]', '[:528]'),
        ('!= 527', '!= 528'),
        ('kreeg 527', 'kreeg 528'),
        ('514, 515, 516, 517, 518]', '515, 516, 517, 518, 519]'),
    ],
)

build(
    'create-five-hundred-forty-two-bootstrap.py',
    'create-five-hundred-forty-three-bootstrap.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('all_cases[:527]', 'all_cases[:528]'),
        ('{UNKNOWN, TYPO}][:527]', '{UNKNOWN, TYPO}][:528]'),
        ('!= 527', '!= 528'),
        ('kreeg 527', 'kreeg 528'),
        ('510, 511, 512, 513, 514]', '511, 512, 513, 514, 515]'),
    ],
)

build(
    'create-five-hundred-forty-two-minimal.py',
    'create-five-hundred-forty-three-minimal.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('!= 527', '!= 528'),
        ('kreeg 527', 'kreeg 528'),
        ('510, 511, 512, 513, 514]', '511, 512, 513, 514, 515]'),
    ],
)

build(
    'make-five-hundred-forty-two.py',
    'make-five-hundred-forty-three.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('all_cases[:527]', 'all_cases[:528]'),
        ('{UNKNOWN, TYPO}][:527]', '{UNKNOWN, TYPO}][:528]'),
        ('!= 527', '!= 528'),
        ('450, 451, 452, 453, 454]', '451, 452, 453, 454, 455]'),
    ],
)

build(
    'create-five-hundred-forty-two-files.py',
    'create-five-hundred-forty-three-files.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('all_cases[:527]', 'all_cases[:528]'),
        ('{UNKNOWN, TYPO}][:527]', '{UNKNOWN, TYPO}][:528]'),
        ('!= 527', '!= 528'),
        ('450, 451, 452, 453, 454]', '451, 452, 453, 454, 455]'),
    ],
)

build(
    'create-five-hundred-forty-two.py',
    'create-five-hundred-forty-three.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('all_cases[:527]', 'all_cases[:528]'),
        ('{UNKNOWN, TYPO}][:527]', '{UNKNOWN, TYPO}][:528]'),
        ('!= 527', '!= 528'),
        ('453, 454, 455, 456, 457]', '454, 455, 456, 457, 458]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-two.py',
    'generate-validate-five-hundred-forty-three.py',
    [
        ('five-hundred-forty-two', 'five-hundred-forty-three'),
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('all_cases[:527]', 'all_cases[:528]'),
        ('{UNKNOWN, TYPO}][:527]', '{UNKNOWN, TYPO}][:528]'),
        ('!= 527', '!= 528'),
        ('450, 451, 452, 453, 454]', '451, 452, 453, 454, 455]'),
    ],
)

build(
    'validate-five-hundred-forty-two-valid-list-cases.py',
    'validate-five-hundred-forty-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('512, 513, 514, 515, 516', '513, 514, 515, 516, 517'),
        ('all_cases[:527]', 'all_cases[:528]'),
        ('len(valid_cases) != 527', 'len(valid_cases) != 528'),
    ],
)

build(
    'validate-five-hundred-forty-two-valid-mixed.py',
    'validate-five-hundred-forty-three-valid-mixed.py',
    [
        ('vijfhonderdtweeënveertig', 'vijfhonderddrieënveertig'),
        ('512, 513, 514, 515, 516', '513, 514, 515, 516, 517'),
        ('][:527]', '][:528]'),
        ('len(valid_cases) != 527', 'len(valid_cases) != 528'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-two.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-two', 'five-hundred-forty-three')
(ROOT / 'verify-five-hundred-forty-three.py').write_text(verify_text)
print('verify-five-hundred-forty-three.py')
