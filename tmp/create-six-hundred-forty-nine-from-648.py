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
    'create-six-hundred-forty-eight-assets.py',
    'create-six-hundred-forty-nine-assets.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('[:633]', '[:634]'),
        ('!= 633', '!= 634'),
        ('kreeg 633', 'kreeg 634'),
        ('620, 621, 622, 623, 624', '621, 622, 623, 624, 625'),
    ],
)

build(
    'create-six-hundred-forty-eight-bootstrap.py',
    'create-six-hundred-forty-nine-bootstrap.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('all_cases[:633]', 'all_cases[:634]'),
        ('{UNKNOWN, TYPO}][:633]', '{UNKNOWN, TYPO}][:634]'),
        ('!= 633', '!= 634'),
        ('kreeg 633', 'kreeg 634'),
        ('616, 617, 618, 619, 620', '617, 618, 619, 620, 621'),
    ],
)

build(
    'create-six-hundred-forty-eight-minimal.py',
    'create-six-hundred-forty-nine-minimal.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('!= 633', '!= 634'),
        ('kreeg 633', 'kreeg 634'),
        ('616, 617, 618, 619, 620', '617, 618, 619, 620, 621'),
    ],
)

build(
    'make-six-hundred-forty-eight.py',
    'make-six-hundred-forty-nine.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('all_cases[:633]', 'all_cases[:634]'),
        ('{UNKNOWN, TYPO}][:633]', '{UNKNOWN, TYPO}][:634]'),
        ('!= 633', '!= 634'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'create-six-hundred-forty-eight-files.py',
    'create-six-hundred-forty-nine-files.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('all_cases[:633]', 'all_cases[:634]'),
        ('{UNKNOWN, TYPO}][:633]', '{UNKNOWN, TYPO}][:634]'),
        ('!= 633', '!= 634'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'create-six-hundred-forty-eight.py',
    'create-six-hundred-forty-nine.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('all_cases[:633]', 'all_cases[:634]'),
        ('{UNKNOWN, TYPO}][:633]', '{UNKNOWN, TYPO}][:634]'),
        ('!= 633', '!= 634'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'generate-validate-six-hundred-forty-eight.py',
    'generate-validate-six-hundred-forty-nine.py',
    [
        ('six-hundred-forty-eight', 'six-hundred-forty-nine'),
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('all_cases[:633]', 'all_cases[:634]'),
        ('{UNKNOWN, TYPO}][:633]', '{UNKNOWN, TYPO}][:634]'),
        ('!= 633', '!= 634'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'validate-six-hundred-forty-eight-valid-list-cases.py',
    'validate-six-hundred-forty-nine-valid-list-cases.py',
    [
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('618, 619, 620, 621, 622', '619, 620, 621, 622, 623'),
        ('all_cases[:633]', 'all_cases[:634]'),
        ('len(valid_cases) != 633', 'len(valid_cases) != 634'),
    ],
)

build(
    'validate-six-hundred-forty-eight-valid-mixed.py',
    'validate-six-hundred-forty-nine-valid-mixed.py',
    [
        ('zeshonderdachtenveertig', 'zeshonderdnegenenveertig'),
        ('618, 619, 620, 621, 622', '619, 620, 621, 622, 623'),
        ('][:633]', '][:634]'),
        ('len(valid_cases) != 633', 'len(valid_cases) != 634'),
        ('plain stderr noemt niet alle zeshonderddrieëndertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvierendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-eight.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-eight', 'six-hundred-forty-nine')
(ROOT / 'verify-six-hundred-forty-nine.py').write_text(verify_text)
print('verify-six-hundred-forty-nine.py')
