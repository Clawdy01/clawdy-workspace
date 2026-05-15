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
    'create-six-hundred-fifty-two-assets.py',
    'create-six-hundred-fifty-three-assets.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('[:637]', '[:638]'),
        ('!= 637', '!= 638'),
        ('kreeg 637', 'kreeg 638'),
        ('624, 625, 626, 627, 628', '625, 626, 627, 628, 629'),
    ],
)

build(
    'create-six-hundred-fifty-two-bootstrap.py',
    'create-six-hundred-fifty-three-bootstrap.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('all_cases[:637]', 'all_cases[:638]'),
        ('{UNKNOWN, TYPO}][:637]', '{UNKNOWN, TYPO}][:638]'),
        ('!= 637', '!= 638'),
        ('kreeg 637', 'kreeg 638'),
        ('620, 621, 622, 623, 624', '621, 622, 623, 624, 625'),
    ],
)

build(
    'create-six-hundred-fifty-two-minimal.py',
    'create-six-hundred-fifty-three-minimal.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('!= 637', '!= 638'),
        ('kreeg 637', 'kreeg 638'),
        ('620, 621, 622, 623, 624', '621, 622, 623, 624, 625'),
    ],
)

build(
    'make-six-hundred-fifty-two.py',
    'make-six-hundred-fifty-three.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('all_cases[:637]', 'all_cases[:638]'),
        ('{UNKNOWN, TYPO}][:637]', '{UNKNOWN, TYPO}][:638]'),
        ('!= 637', '!= 638'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'create-six-hundred-fifty-two-files.py',
    'create-six-hundred-fifty-three-files.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('all_cases[:637]', 'all_cases[:638]'),
        ('{UNKNOWN, TYPO}][:637]', '{UNKNOWN, TYPO}][:638]'),
        ('!= 637', '!= 638'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'create-six-hundred-fifty-two.py',
    'create-six-hundred-fifty-three.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('all_cases[:637]', 'all_cases[:638]'),
        ('{UNKNOWN, TYPO}][:637]', '{UNKNOWN, TYPO}][:638]'),
        ('!= 637', '!= 638'),
        ('563, 564, 565, 566, 567', '564, 565, 566, 567, 568'),
    ],
)

build(
    'generate-validate-six-hundred-fifty-two.py',
    'generate-validate-six-hundred-fifty-three.py',
    [
        ('six-hundred-fifty-two', 'six-hundred-fifty-three'),
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('all_cases[:637]', 'all_cases[:638]'),
        ('{UNKNOWN, TYPO}][:637]', '{UNKNOWN, TYPO}][:638]'),
        ('!= 637', '!= 638'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'validate-six-hundred-fifty-two-valid-list-cases.py',
    'validate-six-hundred-fifty-three-valid-list-cases.py',
    [
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('622, 623, 624, 625, 626', '623, 624, 625, 626, 627'),
        ('all_cases[:637]', 'all_cases[:638]'),
        ('len(valid_cases) != 637', 'len(valid_cases) != 638'),
    ],
)

build(
    'validate-six-hundred-fifty-two-valid-mixed.py',
    'validate-six-hundred-fifty-three-valid-mixed.py',
    [
        ('zeshonderdtweeënvijftig', 'zeshonderddrieënvijftig'),
        ('622, 623, 624, 625, 626', '623, 624, 625, 626, 627'),
        ('][:637]', '][:638]'),
        ('len(valid_cases) != 637', 'len(valid_cases) != 638'),
        ('plain stderr noemt niet alle zeshonderdzevenendertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdachtendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-fifty-two.py').read_text()
verify_text = verify_src.replace('six-hundred-fifty-two', 'six-hundred-fifty-three')
(ROOT / 'verify-six-hundred-fifty-three.py').write_text(verify_text)
print('verify-six-hundred-fifty-three.py')
