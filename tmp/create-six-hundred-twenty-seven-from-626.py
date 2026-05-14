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
    'create-six-hundred-twenty-six-assets.py',
    'create-six-hundred-twenty-seven-assets.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('[:611]', '[:612]'),
        ('!= 611', '!= 612'),
        ('kreeg 611', 'kreeg 612'),
        ('598, 599, 600, 601, 602', '599, 600, 601, 602, 603'),
    ],
)

build(
    'create-six-hundred-twenty-six-bootstrap.py',
    'create-six-hundred-twenty-seven-bootstrap.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('all_cases[:611]', 'all_cases[:612]'),
        ('{UNKNOWN, TYPO}][:611]', '{UNKNOWN, TYPO}][:612]'),
        ('!= 611', '!= 612'),
        ('kreeg 611', 'kreeg 612'),
        ('594, 595, 596, 597, 598', '595, 596, 597, 598, 599'),
    ],
)

build(
    'create-six-hundred-twenty-six-minimal.py',
    'create-six-hundred-twenty-seven-minimal.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('!= 611', '!= 612'),
        ('kreeg 611', 'kreeg 612'),
        ('594, 595, 596, 597, 598', '595, 596, 597, 598, 599'),
    ],
)

build(
    'make-six-hundred-twenty-six.py',
    'make-six-hundred-twenty-seven.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('all_cases[:611]', 'all_cases[:612]'),
        ('{UNKNOWN, TYPO}][:611]', '{UNKNOWN, TYPO}][:612]'),
        ('!= 611', '!= 612'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'create-six-hundred-twenty-six-files.py',
    'create-six-hundred-twenty-seven-files.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('all_cases[:611]', 'all_cases[:612]'),
        ('{UNKNOWN, TYPO}][:611]', '{UNKNOWN, TYPO}][:612]'),
        ('!= 611', '!= 612'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'create-six-hundred-twenty-six.py',
    'create-six-hundred-twenty-seven.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('all_cases[:611]', 'all_cases[:612]'),
        ('{UNKNOWN, TYPO}][:611]', '{UNKNOWN, TYPO}][:612]'),
        ('!= 611', '!= 612'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-six.py',
    'generate-validate-six-hundred-twenty-seven.py',
    [
        ('six-hundred-twenty-six', 'six-hundred-twenty-seven'),
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('all_cases[:611]', 'all_cases[:612]'),
        ('{UNKNOWN, TYPO}][:611]', '{UNKNOWN, TYPO}][:612]'),
        ('!= 611', '!= 612'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'validate-six-hundred-twenty-six-valid-list-cases.py',
    'validate-six-hundred-twenty-seven-valid-list-cases.py',
    [
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('596, 597, 598, 599, 600', '597, 598, 599, 600, 601'),
        ('all_cases[:611]', 'all_cases[:612]'),
        ('len(valid_cases) != 611', 'len(valid_cases) != 612'),
    ],
)

build(
    'validate-six-hundred-twenty-six-valid-mixed.py',
    'validate-six-hundred-twenty-seven-valid-mixed.py',
    [
        ('zeshonderdzesentwintig', 'zeshonderdzevenentwintig'),
        ('596, 597, 598, 599, 600', '597, 598, 599, 600, 601'),
        ('][:611]', '][:612]'),
        ('len(valid_cases) != 611', 'len(valid_cases) != 612'),
        ('plain stderr noemt niet alle zeshonderdelf geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdtwaalf geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-six.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-six', 'six-hundred-twenty-seven')
(ROOT / 'verify-six-hundred-twenty-seven.py').write_text(verify_text)
print('verify-six-hundred-twenty-seven.py')
