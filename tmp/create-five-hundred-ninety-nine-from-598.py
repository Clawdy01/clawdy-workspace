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
    'create-five-hundred-ninety-eight-assets.py',
    'create-five-hundred-ninety-nine-assets.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('[:583]', '[:584]'),
        ('!= 583', '!= 584'),
        ('kreeg 583', 'kreeg 584'),
        ('570, 571, 572, 573, 574', '571, 572, 573, 574, 575'),
    ],
)

build(
    'create-five-hundred-ninety-eight-bootstrap.py',
    'create-five-hundred-ninety-nine-bootstrap.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('all_cases[:583]', 'all_cases[:584]'),
        ('{UNKNOWN, TYPO}][:583]', '{UNKNOWN, TYPO}][:584]'),
        ('!= 583', '!= 584'),
        ('kreeg 583', 'kreeg 584'),
        ('566, 567, 568, 569, 570', '567, 568, 569, 570, 571'),
    ],
)

build(
    'create-five-hundred-ninety-eight-minimal.py',
    'create-five-hundred-ninety-nine-minimal.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('!= 583', '!= 584'),
        ('kreeg 583', 'kreeg 584'),
        ('566, 567, 568, 569, 570', '567, 568, 569, 570, 571'),
    ],
)

build(
    'make-five-hundred-ninety-eight.py',
    'make-five-hundred-ninety-nine.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('all_cases[:583]', 'all_cases[:584]'),
        ('{UNKNOWN, TYPO}][:583]', '{UNKNOWN, TYPO}][:584]'),
        ('!= 583', '!= 584'),
        ('506, 507, 508, 509, 510', '507, 508, 509, 510, 511'),
    ],
)

build(
    'create-five-hundred-ninety-eight-files.py',
    'create-five-hundred-ninety-nine-files.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('all_cases[:583]', 'all_cases[:584]'),
        ('{UNKNOWN, TYPO}][:583]', '{UNKNOWN, TYPO}][:584]'),
        ('!= 583', '!= 584'),
        ('506, 507, 508, 509, 510', '507, 508, 509, 510, 511'),
    ],
)

build(
    'create-five-hundred-ninety-eight.py',
    'create-five-hundred-ninety-nine.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('all_cases[:583]', 'all_cases[:584]'),
        ('{UNKNOWN, TYPO}][:583]', '{UNKNOWN, TYPO}][:584]'),
        ('!= 583', '!= 584'),
        ('509, 510, 511, 512, 513', '510, 511, 512, 513, 514'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-eight.py',
    'generate-validate-five-hundred-ninety-nine.py',
    [
        ('five-hundred-ninety-eight', 'five-hundred-ninety-nine'),
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('all_cases[:583]', 'all_cases[:584]'),
        ('{UNKNOWN, TYPO}][:583]', '{UNKNOWN, TYPO}][:584]'),
        ('!= 583', '!= 584'),
        ('506, 507, 508, 509, 510', '507, 508, 509, 510, 511'),
    ],
)

build(
    'validate-five-hundred-ninety-eight-valid-list-cases.py',
    'validate-five-hundred-ninety-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('568, 569, 570, 571, 572', '569, 570, 571, 572, 573'),
        ('all_cases[:583]', 'all_cases[:584]'),
        ('len(valid_cases) != 583', 'len(valid_cases) != 584'),
    ],
)

build(
    'validate-five-hundred-ninety-eight-valid-mixed.py',
    'validate-five-hundred-ninety-nine-valid-mixed.py',
    [
        ('vijfhonderdachtennegentig', 'vijfhonderdnegenennegentig'),
        ('568, 569, 570, 571, 572', '569, 570, 571, 572, 573'),
        ('][:583]', '][:584]'),
        ('len(valid_cases) != 583', 'len(valid_cases) != 584'),
        ('plain stderr noemt niet alle vijfhonderddrieëntachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvierentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-eight', 'five-hundred-ninety-nine')
(ROOT / 'verify-five-hundred-ninety-nine.py').write_text(verify_text)
print('verify-five-hundred-ninety-nine.py')
