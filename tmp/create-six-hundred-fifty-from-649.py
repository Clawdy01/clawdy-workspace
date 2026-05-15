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
    'create-six-hundred-forty-nine-assets.py',
    'create-six-hundred-fifty-assets.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('[:634]', '[:635]'),
        ('!= 634', '!= 635'),
        ('kreeg 634', 'kreeg 635'),
        ('621, 622, 623, 624, 625', '622, 623, 624, 625, 626'),
    ],
)

build(
    'create-six-hundred-forty-nine-bootstrap.py',
    'create-six-hundred-fifty-bootstrap.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('all_cases[:634]', 'all_cases[:635]'),
        ('{UNKNOWN, TYPO}][:634]', '{UNKNOWN, TYPO}][:635]'),
        ('!= 634', '!= 635'),
        ('kreeg 634', 'kreeg 635'),
        ('617, 618, 619, 620, 621', '618, 619, 620, 621, 622'),
    ],
)

build(
    'create-six-hundred-forty-nine-minimal.py',
    'create-six-hundred-fifty-minimal.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('!= 634', '!= 635'),
        ('kreeg 634', 'kreeg 635'),
        ('617, 618, 619, 620, 621', '618, 619, 620, 621, 622'),
    ],
)

build(
    'make-six-hundred-forty-nine.py',
    'make-six-hundred-fifty.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('all_cases[:634]', 'all_cases[:635]'),
        ('{UNKNOWN, TYPO}][:634]', '{UNKNOWN, TYPO}][:635]'),
        ('!= 634', '!= 635'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'create-six-hundred-forty-nine-files.py',
    'create-six-hundred-fifty-files.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('all_cases[:634]', 'all_cases[:635]'),
        ('{UNKNOWN, TYPO}][:634]', '{UNKNOWN, TYPO}][:635]'),
        ('!= 634', '!= 635'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'create-six-hundred-forty-nine.py',
    'create-six-hundred-fifty.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('all_cases[:634]', 'all_cases[:635]'),
        ('{UNKNOWN, TYPO}][:634]', '{UNKNOWN, TYPO}][:635]'),
        ('!= 634', '!= 635'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'generate-validate-six-hundred-forty-nine.py',
    'generate-validate-six-hundred-fifty.py',
    [
        ('six-hundred-forty-nine', 'six-hundred-fifty'),
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('all_cases[:634]', 'all_cases[:635]'),
        ('{UNKNOWN, TYPO}][:634]', '{UNKNOWN, TYPO}][:635]'),
        ('!= 634', '!= 635'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'validate-six-hundred-forty-nine-valid-list-cases.py',
    'validate-six-hundred-fifty-valid-list-cases.py',
    [
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('619, 620, 621, 622, 623', '620, 621, 622, 623, 624'),
        ('all_cases[:634]', 'all_cases[:635]'),
        ('len(valid_cases) != 634', 'len(valid_cases) != 635'),
    ],
)

build(
    'validate-six-hundred-forty-nine-valid-mixed.py',
    'validate-six-hundred-fifty-valid-mixed.py',
    [
        ('zeshonderdnegenenveertig', 'zeshonderdvijftig'),
        ('619, 620, 621, 622, 623', '620, 621, 622, 623, 624'),
        ('][:634]', '][:635]'),
        ('len(valid_cases) != 634', 'len(valid_cases) != 635'),
        ('plain stderr noemt niet alle zeshonderdvierendertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvijfendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-nine.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-nine', 'six-hundred-fifty')
(ROOT / 'verify-six-hundred-fifty.py').write_text(verify_text)
print('verify-six-hundred-fifty.py')
