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
    'create-six-hundred-eighteen-assets.py',
    'create-six-hundred-nineteen-assets.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('[:603]', '[:604]'),
        ('!= 603', '!= 604'),
        ('kreeg 603', 'kreeg 604'),
        ('590, 591, 592, 593, 594', '591, 592, 593, 594, 595'),
    ],
)

build(
    'create-six-hundred-eighteen-bootstrap.py',
    'create-six-hundred-nineteen-bootstrap.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('all_cases[:603]', 'all_cases[:604]'),
        ('{UNKNOWN, TYPO}][:603]', '{UNKNOWN, TYPO}][:604]'),
        ('!= 603', '!= 604'),
        ('kreeg 603', 'kreeg 604'),
        ('586, 587, 588, 589, 590', '587, 588, 589, 590, 591'),
    ],
)

build(
    'create-six-hundred-eighteen-minimal.py',
    'create-six-hundred-nineteen-minimal.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('!= 603', '!= 604'),
        ('kreeg 603', 'kreeg 604'),
        ('586, 587, 588, 589, 590', '587, 588, 589, 590, 591'),
    ],
)

build(
    'make-six-hundred-eighteen.py',
    'make-six-hundred-nineteen.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('all_cases[:603]', 'all_cases[:604]'),
        ('{UNKNOWN, TYPO}][:603]', '{UNKNOWN, TYPO}][:604]'),
        ('!= 603', '!= 604'),
        ('526, 527, 528, 529, 530', '527, 528, 529, 530, 531'),
    ],
)

build(
    'create-six-hundred-eighteen-files.py',
    'create-six-hundred-nineteen-files.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('all_cases[:603]', 'all_cases[:604]'),
        ('{UNKNOWN, TYPO}][:603]', '{UNKNOWN, TYPO}][:604]'),
        ('!= 603', '!= 604'),
        ('526, 527, 528, 529, 530', '527, 528, 529, 530, 531'),
    ],
)

build(
    'create-six-hundred-eighteen.py',
    'create-six-hundred-nineteen.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('all_cases[:603]', 'all_cases[:604]'),
        ('{UNKNOWN, TYPO}][:603]', '{UNKNOWN, TYPO}][:604]'),
        ('!= 603', '!= 604'),
        ('529, 530, 531, 532, 533', '530, 531, 532, 533, 534'),
    ],
)

build(
    'generate-validate-six-hundred-eighteen.py',
    'generate-validate-six-hundred-nineteen.py',
    [
        ('six-hundred-eighteen', 'six-hundred-nineteen'),
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('all_cases[:603]', 'all_cases[:604]'),
        ('{UNKNOWN, TYPO}][:603]', '{UNKNOWN, TYPO}][:604]'),
        ('!= 603', '!= 604'),
        ('526, 527, 528, 529, 530', '527, 528, 529, 530, 531'),
    ],
)

build(
    'validate-six-hundred-eighteen-valid-list-cases.py',
    'validate-six-hundred-nineteen-valid-list-cases.py',
    [
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('588, 589, 590, 591, 592', '589, 590, 591, 592, 593'),
        ('all_cases[:603]', 'all_cases[:604]'),
        ('len(valid_cases) != 603', 'len(valid_cases) != 604'),
    ],
)

build(
    'validate-six-hundred-eighteen-valid-mixed.py',
    'validate-six-hundred-nineteen-valid-mixed.py',
    [
        ('zeshonderdachttien', 'zeshonderdnegentien'),
        ('588, 589, 590, 591, 592', '589, 590, 591, 592, 593'),
        ('][:603]', '][:604]'),
        ('len(valid_cases) != 603', 'len(valid_cases) != 604'),
        ('plain stderr noemt niet alle zeshonderddrie geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvier geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-eighteen.py').read_text()
verify_text = verify_src.replace('six-hundred-eighteen', 'six-hundred-nineteen')
(ROOT / 'verify-six-hundred-nineteen.py').write_text(verify_text)
print('verify-six-hundred-nineteen.py')
