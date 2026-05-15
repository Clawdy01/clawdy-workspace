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
    'create-six-hundred-forty-five-assets.py',
    'create-six-hundred-forty-six-assets.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('[:630]', '[:631]'),
        ('!= 630', '!= 631'),
        ('kreeg 630', 'kreeg 631'),
        ('617, 618, 619, 620, 621', '618, 619, 620, 621, 622'),
    ],
)

build(
    'create-six-hundred-forty-five-bootstrap.py',
    'create-six-hundred-forty-six-bootstrap.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('all_cases[:630]', 'all_cases[:631]'),
        ('{UNKNOWN, TYPO}][:630]', '{UNKNOWN, TYPO}][:631]'),
        ('!= 630', '!= 631'),
        ('kreeg 630', 'kreeg 631'),
        ('613, 614, 615, 616, 617', '614, 615, 616, 617, 618'),
    ],
)

build(
    'create-six-hundred-forty-five-minimal.py',
    'create-six-hundred-forty-six-minimal.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('!= 630', '!= 631'),
        ('kreeg 630', 'kreeg 631'),
        ('613, 614, 615, 616, 617', '614, 615, 616, 617, 618'),
    ],
)

build(
    'make-six-hundred-forty-five.py',
    'make-six-hundred-forty-six.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('all_cases[:630]', 'all_cases[:631]'),
        ('{UNKNOWN, TYPO}][:630]', '{UNKNOWN, TYPO}][:631]'),
        ('!= 630', '!= 631'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'create-six-hundred-forty-five-files.py',
    'create-six-hundred-forty-six-files.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('all_cases[:630]', 'all_cases[:631]'),
        ('{UNKNOWN, TYPO}][:630]', '{UNKNOWN, TYPO}][:631]'),
        ('!= 630', '!= 631'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'create-six-hundred-forty-five.py',
    'create-six-hundred-forty-six.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('all_cases[:630]', 'all_cases[:631]'),
        ('{UNKNOWN, TYPO}][:630]', '{UNKNOWN, TYPO}][:631]'),
        ('!= 630', '!= 631'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'generate-validate-six-hundred-forty-five.py',
    'generate-validate-six-hundred-forty-six.py',
    [
        ('six-hundred-forty-five', 'six-hundred-forty-six'),
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('all_cases[:630]', 'all_cases[:631]'),
        ('{UNKNOWN, TYPO}][:630]', '{UNKNOWN, TYPO}][:631]'),
        ('!= 630', '!= 631'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'validate-six-hundred-forty-five-valid-list-cases.py',
    'validate-six-hundred-forty-six-valid-list-cases.py',
    [
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('615, 616, 617, 618, 619', '616, 617, 618, 619, 620'),
        ('all_cases[:630]', 'all_cases[:631]'),
        ('len(valid_cases) != 630', 'len(valid_cases) != 631'),
    ],
)

build(
    'validate-six-hundred-forty-five-valid-mixed.py',
    'validate-six-hundred-forty-six-valid-mixed.py',
    [
        ('zeshonderdvijfenveertig', 'zeshonderdzesenveertig'),
        ('615, 616, 617, 618, 619', '616, 617, 618, 619, 620'),
        ('][:630]', '][:631]'),
        ('len(valid_cases) != 630', 'len(valid_cases) != 631'),
        ('plain stderr noemt niet alle zeshonderddertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdeenendertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-five.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-five', 'six-hundred-forty-six')
(ROOT / 'verify-six-hundred-forty-six.py').write_text(verify_text)
print('verify-six-hundred-forty-six.py')
