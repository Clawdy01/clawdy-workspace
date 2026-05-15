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
    'create-six-hundred-forty-six-assets.py',
    'create-six-hundred-forty-seven-assets.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('[:631]', '[:632]'),
        ('!= 631', '!= 632'),
        ('kreeg 631', 'kreeg 632'),
        ('618, 619, 620, 621, 622', '619, 620, 621, 622, 623'),
    ],
)

build(
    'create-six-hundred-forty-six-bootstrap.py',
    'create-six-hundred-forty-seven-bootstrap.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('all_cases[:631]', 'all_cases[:632]'),
        ('{UNKNOWN, TYPO}][:631]', '{UNKNOWN, TYPO}][:632]'),
        ('!= 631', '!= 632'),
        ('kreeg 631', 'kreeg 632'),
        ('614, 615, 616, 617, 618', '615, 616, 617, 618, 619'),
    ],
)

build(
    'create-six-hundred-forty-six-minimal.py',
    'create-six-hundred-forty-seven-minimal.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('!= 631', '!= 632'),
        ('kreeg 631', 'kreeg 632'),
        ('614, 615, 616, 617, 618', '615, 616, 617, 618, 619'),
    ],
)

build(
    'make-six-hundred-forty-six.py',
    'make-six-hundred-forty-seven.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('all_cases[:631]', 'all_cases[:632]'),
        ('{UNKNOWN, TYPO}][:631]', '{UNKNOWN, TYPO}][:632]'),
        ('!= 631', '!= 632'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'create-six-hundred-forty-six-files.py',
    'create-six-hundred-forty-seven-files.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('all_cases[:631]', 'all_cases[:632]'),
        ('{UNKNOWN, TYPO}][:631]', '{UNKNOWN, TYPO}][:632]'),
        ('!= 631', '!= 632'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'create-six-hundred-forty-six.py',
    'create-six-hundred-forty-seven.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('all_cases[:631]', 'all_cases[:632]'),
        ('{UNKNOWN, TYPO}][:631]', '{UNKNOWN, TYPO}][:632]'),
        ('!= 631', '!= 632'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'generate-validate-six-hundred-forty-six.py',
    'generate-validate-six-hundred-forty-seven.py',
    [
        ('six-hundred-forty-six', 'six-hundred-forty-seven'),
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('all_cases[:631]', 'all_cases[:632]'),
        ('{UNKNOWN, TYPO}][:631]', '{UNKNOWN, TYPO}][:632]'),
        ('!= 631', '!= 632'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'validate-six-hundred-forty-six-valid-list-cases.py',
    'validate-six-hundred-forty-seven-valid-list-cases.py',
    [
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('616, 617, 618, 619, 620', '617, 618, 619, 620, 621'),
        ('all_cases[:631]', 'all_cases[:632]'),
        ('len(valid_cases) != 631', 'len(valid_cases) != 632'),
    ],
)

build(
    'validate-six-hundred-forty-six-valid-mixed.py',
    'validate-six-hundred-forty-seven-valid-mixed.py',
    [
        ('zeshonderdzesenveertig', 'zeshonderdzevenenveertig'),
        ('616, 617, 618, 619, 620', '617, 618, 619, 620, 621'),
        ('][:631]', '][:632]'),
        ('len(valid_cases) != 631', 'len(valid_cases) != 632'),
        ('plain stderr noemt niet alle zeshonderdeenendertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdtweeëndertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-six.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-six', 'six-hundred-forty-seven')
(ROOT / 'verify-six-hundred-forty-seven.py').write_text(verify_text)
print('verify-six-hundred-forty-seven.py')
