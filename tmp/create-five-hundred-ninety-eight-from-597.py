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
    'create-five-hundred-ninety-seven-assets.py',
    'create-five-hundred-ninety-eight-assets.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('[:582]', '[:583]'),
        ('!= 582', '!= 583'),
        ('kreeg 582', 'kreeg 583'),
        ('569, 570, 571, 572, 573', '570, 571, 572, 573, 574'),
    ],
)

build(
    'create-five-hundred-ninety-seven-bootstrap.py',
    'create-five-hundred-ninety-eight-bootstrap.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('all_cases[:582]', 'all_cases[:583]'),
        ('{UNKNOWN, TYPO}][:582]', '{UNKNOWN, TYPO}][:583]'),
        ('!= 582', '!= 583'),
        ('kreeg 582', 'kreeg 583'),
        ('565, 566, 567, 568, 569', '566, 567, 568, 569, 570'),
    ],
)

build(
    'create-five-hundred-ninety-seven-minimal.py',
    'create-five-hundred-ninety-eight-minimal.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('!= 582', '!= 583'),
        ('kreeg 582', 'kreeg 583'),
        ('565, 566, 567, 568, 569', '566, 567, 568, 569, 570'),
    ],
)

build(
    'make-five-hundred-ninety-seven.py',
    'make-five-hundred-ninety-eight.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('all_cases[:582]', 'all_cases[:583]'),
        ('{UNKNOWN, TYPO}][:582]', '{UNKNOWN, TYPO}][:583]'),
        ('!= 582', '!= 583'),
        ('505, 506, 507, 508, 509', '506, 507, 508, 509, 510'),
    ],
)

build(
    'create-five-hundred-ninety-seven-files.py',
    'create-five-hundred-ninety-eight-files.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('all_cases[:582]', 'all_cases[:583]'),
        ('{UNKNOWN, TYPO}][:582]', '{UNKNOWN, TYPO}][:583]'),
        ('!= 582', '!= 583'),
        ('505, 506, 507, 508, 509', '506, 507, 508, 509, 510'),
    ],
)

build(
    'create-five-hundred-ninety-seven.py',
    'create-five-hundred-ninety-eight.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('all_cases[:582]', 'all_cases[:583]'),
        ('{UNKNOWN, TYPO}][:582]', '{UNKNOWN, TYPO}][:583]'),
        ('!= 582', '!= 583'),
        ('508, 509, 510, 511, 512', '509, 510, 511, 512, 513'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-seven.py',
    'generate-validate-five-hundred-ninety-eight.py',
    [
        ('five-hundred-ninety-seven', 'five-hundred-ninety-eight'),
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('all_cases[:582]', 'all_cases[:583]'),
        ('{UNKNOWN, TYPO}][:582]', '{UNKNOWN, TYPO}][:583]'),
        ('!= 582', '!= 583'),
        ('505, 506, 507, 508, 509', '506, 507, 508, 509, 510'),
    ],
)

build(
    'validate-five-hundred-ninety-seven-valid-list-cases.py',
    'validate-five-hundred-ninety-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('567, 568, 569, 570, 571', '568, 569, 570, 571, 572'),
        ('all_cases[:582]', 'all_cases[:583]'),
        ('len(valid_cases) != 582', 'len(valid_cases) != 583'),
    ],
)

build(
    'validate-five-hundred-ninety-seven-valid-mixed.py',
    'validate-five-hundred-ninety-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenennegentig', 'vijfhonderdachtennegentig'),
        ('567, 568, 569, 570, 571', '568, 569, 570, 571, 572'),
        ('][:582]', '][:583]'),
        ('len(valid_cases) != 582', 'len(valid_cases) != 583'),
        ('plain stderr noemt niet alle vijfhonderdtweeëntachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderddrieëntachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-seven', 'five-hundred-ninety-eight')
(ROOT / 'verify-five-hundred-ninety-eight.py').write_text(verify_text)
print('verify-five-hundred-ninety-eight.py')
