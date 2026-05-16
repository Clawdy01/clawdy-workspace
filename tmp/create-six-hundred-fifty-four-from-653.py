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
    'create-six-hundred-fifty-three-assets.py',
    'create-six-hundred-fifty-four-assets.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('[:638]', '[:639]'),
        ('!= 638', '!= 639'),
        ('kreeg 638', 'kreeg 639'),
        ('625, 626, 627, 628, 629', '626, 627, 628, 629, 630'),
    ],
)

build(
    'create-six-hundred-fifty-three-bootstrap.py',
    'create-six-hundred-fifty-four-bootstrap.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('all_cases[:638]', 'all_cases[:639]'),
        ('{UNKNOWN, TYPO}][:638]', '{UNKNOWN, TYPO}][:639]'),
        ('!= 638', '!= 639'),
        ('kreeg 638', 'kreeg 639'),
        ('621, 622, 623, 624, 625', '622, 623, 624, 625, 626'),
    ],
)

build(
    'create-six-hundred-fifty-three-minimal.py',
    'create-six-hundred-fifty-four-minimal.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('!= 638', '!= 639'),
        ('kreeg 638', 'kreeg 639'),
        ('621, 622, 623, 624, 625', '622, 623, 624, 625, 626'),
    ],
)

build(
    'make-six-hundred-fifty-three.py',
    'make-six-hundred-fifty-four.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('all_cases[:638]', 'all_cases[:639]'),
        ('{UNKNOWN, TYPO}][:638]', '{UNKNOWN, TYPO}][:639]'),
        ('!= 638', '!= 639'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'create-six-hundred-fifty-three-files.py',
    'create-six-hundred-fifty-four-files.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('all_cases[:638]', 'all_cases[:639]'),
        ('{UNKNOWN, TYPO}][:638]', '{UNKNOWN, TYPO}][:639]'),
        ('!= 638', '!= 639'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'create-six-hundred-fifty-three.py',
    'create-six-hundred-fifty-four.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('all_cases[:638]', 'all_cases[:639]'),
        ('{UNKNOWN, TYPO}][:638]', '{UNKNOWN, TYPO}][:639]'),
        ('!= 638', '!= 639'),
        ('564, 565, 566, 567, 568', '565, 566, 567, 568, 569'),
    ],
)

build(
    'generate-validate-six-hundred-fifty-three.py',
    'generate-validate-six-hundred-fifty-four.py',
    [
        ('six-hundred-fifty-three', 'six-hundred-fifty-four'),
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('all_cases[:638]', 'all_cases[:639]'),
        ('{UNKNOWN, TYPO}][:638]', '{UNKNOWN, TYPO}][:639]'),
        ('!= 638', '!= 639'),
        ('561, 562, 563, 564, 565', '562, 563, 564, 565, 566'),
    ],
)

build(
    'validate-six-hundred-fifty-three-valid-list-cases.py',
    'validate-six-hundred-fifty-four-valid-list-cases.py',
    [
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('623, 624, 625, 626, 627', '624, 625, 626, 627, 628'),
        ('all_cases[:638]', 'all_cases[:639]'),
        ('len(valid_cases) != 638', 'len(valid_cases) != 639'),
    ],
)

build(
    'validate-six-hundred-fifty-three-valid-mixed.py',
    'validate-six-hundred-fifty-four-valid-mixed.py',
    [
        ('zeshonderddrieënvijftig', 'zeshonderdvierenvijftig'),
        ('623, 624, 625, 626, 627', '624, 625, 626, 627, 628'),
        ('][:638]', '][:639]'),
        ('len(valid_cases) != 638', 'len(valid_cases) != 639'),
        ('plain stderr noemt niet alle zeshonderdachtendertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdnegenendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-fifty-three.py').read_text()
verify_text = verify_src.replace('six-hundred-fifty-three', 'six-hundred-fifty-four')
(ROOT / 'verify-six-hundred-fifty-four.py').write_text(verify_text)
print('verify-six-hundred-fifty-four.py')
