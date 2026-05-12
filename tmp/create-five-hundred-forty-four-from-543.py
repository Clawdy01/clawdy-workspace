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
    'create-five-hundred-forty-three-assets.py',
    'create-five-hundred-forty-four-assets.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('[:528]', '[:529]'),
        ('!= 528', '!= 529'),
        ('kreeg 528', 'kreeg 529'),
        ('515, 516, 517, 518, 519]', '516, 517, 518, 519, 520]'),
    ],
)

build(
    'create-five-hundred-forty-three-bootstrap.py',
    'create-five-hundred-forty-four-bootstrap.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('all_cases[:528]', 'all_cases[:529]'),
        ('{UNKNOWN, TYPO}][:528]', '{UNKNOWN, TYPO}][:529]'),
        ('!= 528', '!= 529'),
        ('kreeg 528', 'kreeg 529'),
        ('511, 512, 513, 514, 515]', '512, 513, 514, 515, 516]'),
    ],
)

build(
    'create-five-hundred-forty-three-minimal.py',
    'create-five-hundred-forty-four-minimal.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('!= 528', '!= 529'),
        ('kreeg 528', 'kreeg 529'),
        ('511, 512, 513, 514, 515]', '512, 513, 514, 515, 516]'),
    ],
)

build(
    'make-five-hundred-forty-three.py',
    'make-five-hundred-forty-four.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('all_cases[:528]', 'all_cases[:529]'),
        ('{UNKNOWN, TYPO}][:528]', '{UNKNOWN, TYPO}][:529]'),
        ('!= 528', '!= 529'),
        ('451, 452, 453, 454, 455]', '452, 453, 454, 455, 456]'),
    ],
)

build(
    'create-five-hundred-forty-three-files.py',
    'create-five-hundred-forty-four-files.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('all_cases[:528]', 'all_cases[:529]'),
        ('{UNKNOWN, TYPO}][:528]', '{UNKNOWN, TYPO}][:529]'),
        ('!= 528', '!= 529'),
        ('451, 452, 453, 454, 455]', '452, 453, 454, 455, 456]'),
    ],
)

build(
    'create-five-hundred-forty-three.py',
    'create-five-hundred-forty-four.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('all_cases[:528]', 'all_cases[:529]'),
        ('{UNKNOWN, TYPO}][:528]', '{UNKNOWN, TYPO}][:529]'),
        ('!= 528', '!= 529'),
        ('454, 455, 456, 457, 458]', '455, 456, 457, 458, 459]'),
    ],
)

build(
    'generate-validate-five-hundred-forty-three.py',
    'generate-validate-five-hundred-forty-four.py',
    [
        ('five-hundred-forty-three', 'five-hundred-forty-four'),
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('all_cases[:528]', 'all_cases[:529]'),
        ('{UNKNOWN, TYPO}][:528]', '{UNKNOWN, TYPO}][:529]'),
        ('!= 528', '!= 529'),
        ('451, 452, 453, 454, 455]', '452, 453, 454, 455, 456]'),
    ],
)

build(
    'validate-five-hundred-forty-three-valid-list-cases.py',
    'validate-five-hundred-forty-four-valid-list-cases.py',
    [
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('513, 514, 515, 516, 517', '514, 515, 516, 517, 518'),
        ('all_cases[:528]', 'all_cases[:529]'),
        ('len(valid_cases) != 528', 'len(valid_cases) != 529'),
    ],
)

build(
    'validate-five-hundred-forty-three-valid-mixed.py',
    'validate-five-hundred-forty-four-valid-mixed.py',
    [
        ('vijfhonderddrieënveertig', 'vijfhonderdvierenveertig'),
        ('513, 514, 515, 516, 517', '514, 515, 516, 517, 518'),
        ('][:528]', '][:529]'),
        ('len(valid_cases) != 528', 'len(valid_cases) != 529'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-forty-three.py').read_text()
verify_text = verify_src.replace('five-hundred-forty-three', 'five-hundred-forty-four')
(ROOT / 'verify-five-hundred-forty-four.py').write_text(verify_text)
print('verify-five-hundred-forty-four.py')
