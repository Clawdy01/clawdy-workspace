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
    'create-five-hundred-seventy-two-assets.py',
    'create-five-hundred-seventy-three-assets.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('[:557]', '[:558]'),
        ('!= 557', '!= 558'),
        ('kreeg 557', 'kreeg 558'),
        ('544, 545, 546, 547, 548', '545, 546, 547, 548, 549'),
    ],
)

build(
    'create-five-hundred-seventy-two-bootstrap.py',
    'create-five-hundred-seventy-three-bootstrap.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('all_cases[:557]', 'all_cases[:558]'),
        ('{UNKNOWN, TYPO}][:557]', '{UNKNOWN, TYPO}][:558]'),
        ('!= 557', '!= 558'),
        ('kreeg 557', 'kreeg 558'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'create-five-hundred-seventy-two-minimal.py',
    'create-five-hundred-seventy-three-minimal.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('!= 557', '!= 558'),
        ('kreeg 557', 'kreeg 558'),
        ('540, 541, 542, 543, 544', '541, 542, 543, 544, 545'),
    ],
)

build(
    'make-five-hundred-seventy-two.py',
    'make-five-hundred-seventy-three.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('all_cases[:557]', 'all_cases[:558]'),
        ('{UNKNOWN, TYPO}][:557]', '{UNKNOWN, TYPO}][:558]'),
        ('!= 557', '!= 558'),
        ('480, 481, 482, 483, 484', '481, 482, 483, 484, 485'),
    ],
)

build(
    'create-five-hundred-seventy-two-files.py',
    'create-five-hundred-seventy-three-files.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('all_cases[:557]', 'all_cases[:558]'),
        ('{UNKNOWN, TYPO}][:557]', '{UNKNOWN, TYPO}][:558]'),
        ('!= 557', '!= 558'),
        ('480, 481, 482, 483, 484', '481, 482, 483, 484, 485'),
    ],
)

build(
    'create-five-hundred-seventy-two.py',
    'create-five-hundred-seventy-three.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('all_cases[:557]', 'all_cases[:558]'),
        ('{UNKNOWN, TYPO}][:557]', '{UNKNOWN, TYPO}][:558]'),
        ('!= 557', '!= 558'),
        ('483, 484, 485, 486, 487', '484, 485, 486, 487, 488'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-two.py',
    'generate-validate-five-hundred-seventy-three.py',
    [
        ('five-hundred-seventy-two', 'five-hundred-seventy-three'),
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('all_cases[:557]', 'all_cases[:558]'),
        ('{UNKNOWN, TYPO}][:557]', '{UNKNOWN, TYPO}][:558]'),
        ('!= 557', '!= 558'),
        ('480, 481, 482, 483, 484', '481, 482, 483, 484, 485'),
    ],
)

build(
    'validate-five-hundred-seventy-two-valid-list-cases.py',
    'validate-five-hundred-seventy-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
        ('all_cases[:557]', 'all_cases[:558]'),
        ('len(valid_cases) != 557', 'len(valid_cases) != 558'),
    ],
)

build(
    'validate-five-hundred-seventy-two-valid-mixed.py',
    'validate-five-hundred-seventy-three-valid-mixed.py',
    [
        ('vijfhonderdtweeënzeventig', 'vijfhonderddrieënzeventig'),
        ('542, 543, 544, 545, 546', '543, 544, 545, 546, 547'),
        ('][:557]', '][:558]'),
        ('len(valid_cases) != 557', 'len(valid_cases) != 558'),
        ('plain stderr noemt niet alle vijfhonderdzevenenvijftig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdachtenvijftig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-two.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-two', 'five-hundred-seventy-three')
(ROOT / 'verify-five-hundred-seventy-three.py').write_text(verify_text)
print('verify-five-hundred-seventy-three.py')
