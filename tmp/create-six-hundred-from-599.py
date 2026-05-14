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
    'create-five-hundred-ninety-nine-assets.py',
    'create-six-hundred-assets.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('[:584]', '[:585]'),
        ('!= 584', '!= 585'),
        ('kreeg 584', 'kreeg 585'),
        ('571, 572, 573, 574, 575', '572, 573, 574, 575, 576'),
    ],
)

build(
    'create-five-hundred-ninety-nine-bootstrap.py',
    'create-six-hundred-bootstrap.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('all_cases[:584]', 'all_cases[:585]'),
        ('{UNKNOWN, TYPO}][:584]', '{UNKNOWN, TYPO}][:585]'),
        ('!= 584', '!= 585'),
        ('kreeg 584', 'kreeg 585'),
        ('567, 568, 569, 570, 571', '568, 569, 570, 571, 572'),
    ],
)

build(
    'create-five-hundred-ninety-nine-minimal.py',
    'create-six-hundred-minimal.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('!= 584', '!= 585'),
        ('kreeg 584', 'kreeg 585'),
        ('567, 568, 569, 570, 571', '568, 569, 570, 571, 572'),
    ],
)

build(
    'make-five-hundred-ninety-nine.py',
    'make-six-hundred.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('all_cases[:584]', 'all_cases[:585]'),
        ('{UNKNOWN, TYPO}][:584]', '{UNKNOWN, TYPO}][:585]'),
        ('!= 584', '!= 585'),
        ('507, 508, 509, 510, 511', '508, 509, 510, 511, 512'),
    ],
)

build(
    'create-five-hundred-ninety-nine-files.py',
    'create-six-hundred-files.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('all_cases[:584]', 'all_cases[:585]'),
        ('{UNKNOWN, TYPO}][:584]', '{UNKNOWN, TYPO}][:585]'),
        ('!= 584', '!= 585'),
        ('507, 508, 509, 510, 511', '508, 509, 510, 511, 512'),
    ],
)

build(
    'create-five-hundred-ninety-nine.py',
    'create-six-hundred.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('all_cases[:584]', 'all_cases[:585]'),
        ('{UNKNOWN, TYPO}][:584]', '{UNKNOWN, TYPO}][:585]'),
        ('!= 584', '!= 585'),
        ('510, 511, 512, 513, 514', '511, 512, 513, 514, 515'),
    ],
)

build(
    'generate-validate-five-hundred-ninety-nine.py',
    'generate-validate-six-hundred.py',
    [
        ('five-hundred-ninety-nine', 'six-hundred'),
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('all_cases[:584]', 'all_cases[:585]'),
        ('{UNKNOWN, TYPO}][:584]', '{UNKNOWN, TYPO}][:585]'),
        ('!= 584', '!= 585'),
        ('507, 508, 509, 510, 511', '508, 509, 510, 511, 512'),
    ],
)

build(
    'validate-five-hundred-ninety-nine-valid-list-cases.py',
    'validate-six-hundred-valid-list-cases.py',
    [
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('569, 570, 571, 572, 573', '570, 571, 572, 573, 574'),
        ('all_cases[:584]', 'all_cases[:585]'),
        ('len(valid_cases) != 584', 'len(valid_cases) != 585'),
    ],
)

build(
    'validate-five-hundred-ninety-nine-valid-mixed.py',
    'validate-six-hundred-valid-mixed.py',
    [
        ('vijfhonderdnegenennegentig', 'zeshonderd'),
        ('569, 570, 571, 572, 573', '570, 571, 572, 573, 574'),
        ('][:584]', '][:585]'),
        ('len(valid_cases) != 584', 'len(valid_cases) != 585'),
        ('plain stderr noemt niet alle vijfhonderdvierentachtig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvijfentachtig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-ninety-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-ninety-nine', 'six-hundred')
(ROOT / 'verify-six-hundred.py').write_text(verify_text)
print('verify-six-hundred.py')
