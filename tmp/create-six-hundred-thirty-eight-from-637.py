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
    'create-six-hundred-thirty-seven-assets.py',
    'create-six-hundred-thirty-eight-assets.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('[:622]', '[:623]'),
        ('!= 622', '!= 623'),
        ('kreeg 622', 'kreeg 623'),
        ('609, 610, 611, 612, 613', '610, 611, 612, 613, 614'),
    ],
)

build(
    'create-six-hundred-thirty-seven-bootstrap.py',
    'create-six-hundred-thirty-eight-bootstrap.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('all_cases[:622]', 'all_cases[:623]'),
        ('{UNKNOWN, TYPO}][:622]', '{UNKNOWN, TYPO}][:623]'),
        ('!= 622', '!= 623'),
        ('kreeg 622', 'kreeg 623'),
        ('605, 606, 607, 608, 609', '606, 607, 608, 609, 610'),
    ],
)

build(
    'create-six-hundred-thirty-seven-minimal.py',
    'create-six-hundred-thirty-eight-minimal.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('!= 622', '!= 623'),
        ('kreeg 622', 'kreeg 623'),
        ('605, 606, 607, 608, 609', '606, 607, 608, 609, 610'),
    ],
)

build(
    'make-six-hundred-thirty-seven.py',
    'make-six-hundred-thirty-eight.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('all_cases[:622]', 'all_cases[:623]'),
        ('{UNKNOWN, TYPO}][:622]', '{UNKNOWN, TYPO}][:623]'),
        ('!= 622', '!= 623'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'create-six-hundred-thirty-seven-files.py',
    'create-six-hundred-thirty-eight-files.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('all_cases[:622]', 'all_cases[:623]'),
        ('{UNKNOWN, TYPO}][:622]', '{UNKNOWN, TYPO}][:623]'),
        ('!= 622', '!= 623'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'create-six-hundred-thirty-seven.py',
    'create-six-hundred-thirty-eight.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('all_cases[:622]', 'all_cases[:623]'),
        ('{UNKNOWN, TYPO}][:622]', '{UNKNOWN, TYPO}][:623]'),
        ('!= 622', '!= 623'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-seven.py',
    'generate-validate-six-hundred-thirty-eight.py',
    [
        ('six-hundred-thirty-seven', 'six-hundred-thirty-eight'),
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('all_cases[:622]', 'all_cases[:623]'),
        ('{UNKNOWN, TYPO}][:622]', '{UNKNOWN, TYPO}][:623]'),
        ('!= 622', '!= 623'),
        ('545, 546, 547, 548, 549', '546, 547, 548, 549, 550'),
    ],
)

build(
    'validate-six-hundred-thirty-seven-valid-list-cases.py',
    'validate-six-hundred-thirty-eight-valid-list-cases.py',
    [
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('607, 608, 609, 610, 611', '608, 609, 610, 611, 612'),
        ('all_cases[:622]', 'all_cases[:623]'),
        ('len(valid_cases) != 622', 'len(valid_cases) != 623'),
    ],
)

build(
    'validate-six-hundred-thirty-seven-valid-mixed.py',
    'validate-six-hundred-thirty-eight-valid-mixed.py',
    [
        ('zeshonderdzevenendertig', 'zeshonderdachtendertig'),
        ('607, 608, 609, 610, 611', '608, 609, 610, 611, 612'),
        ('][:622]', '][:623]'),
        ('len(valid_cases) != 622', 'len(valid_cases) != 623'),
        ('plain stderr noemt niet alle zeshonderdtweeëntwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderddrieëntwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-seven.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-seven', 'six-hundred-thirty-eight')
(ROOT / 'verify-six-hundred-thirty-eight.py').write_text(verify_text)
print('verify-six-hundred-thirty-eight.py')
