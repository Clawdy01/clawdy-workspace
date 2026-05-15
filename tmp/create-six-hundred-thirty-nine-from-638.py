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
    'create-six-hundred-thirty-eight-assets.py',
    'create-six-hundred-thirty-nine-assets.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('[:623]', '[:624]'),
        ('!= 623', '!= 624'),
        ('kreeg 623', 'kreeg 624'),
        ('610, 611, 612, 613, 614', '611, 612, 613, 614, 615'),
    ],
)

build(
    'create-six-hundred-thirty-eight-bootstrap.py',
    'create-six-hundred-thirty-nine-bootstrap.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('all_cases[:623]', 'all_cases[:624]'),
        ('{UNKNOWN, TYPO}][:623]', '{UNKNOWN, TYPO}][:624]'),
        ('!= 623', '!= 624'),
        ('kreeg 623', 'kreeg 624'),
        ('606, 607, 608, 609, 610', '607, 608, 609, 610, 611'),
    ],
)

build(
    'create-six-hundred-thirty-eight-minimal.py',
    'create-six-hundred-thirty-nine-minimal.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('!= 623', '!= 624'),
        ('kreeg 623', 'kreeg 624'),
        ('606, 607, 608, 609, 610', '607, 608, 609, 610, 611'),
    ],
)

build(
    'make-six-hundred-thirty-eight.py',
    'make-six-hundred-thirty-nine.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('all_cases[:623]', 'all_cases[:624]'),
        ('{UNKNOWN, TYPO}][:623]', '{UNKNOWN, TYPO}][:624]'),
        ('!= 623', '!= 624'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'create-six-hundred-thirty-eight-files.py',
    'create-six-hundred-thirty-nine-files.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('all_cases[:623]', 'all_cases[:624]'),
        ('{UNKNOWN, TYPO}][:623]', '{UNKNOWN, TYPO}][:624]'),
        ('!= 623', '!= 624'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'create-six-hundred-thirty-eight.py',
    'create-six-hundred-thirty-nine.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('all_cases[:623]', 'all_cases[:624]'),
        ('{UNKNOWN, TYPO}][:623]', '{UNKNOWN, TYPO}][:624]'),
        ('!= 623', '!= 624'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-eight.py',
    'generate-validate-six-hundred-thirty-nine.py',
    [
        ('six-hundred-thirty-eight', 'six-hundred-thirty-nine'),
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('all_cases[:623]', 'all_cases[:624]'),
        ('{UNKNOWN, TYPO}][:623]', '{UNKNOWN, TYPO}][:624]'),
        ('!= 623', '!= 624'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'validate-six-hundred-thirty-eight-valid-list-cases.py',
    'validate-six-hundred-thirty-nine-valid-list-cases.py',
    [
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('608, 609, 610, 611, 612', '609, 610, 611, 612, 613'),
        ('all_cases[:623]', 'all_cases[:624]'),
        ('len(valid_cases) != 623', 'len(valid_cases) != 624'),
    ],
)

build(
    'validate-six-hundred-thirty-eight-valid-mixed.py',
    'validate-six-hundred-thirty-nine-valid-mixed.py',
    [
        ('zeshonderdachtendertig', 'zeshonderdnegenendertig'),
        ('608, 609, 610, 611, 612', '609, 610, 611, 612, 613'),
        ('][:623]', '][:624]'),
        ('len(valid_cases) != 623', 'len(valid_cases) != 624'),
        ('plain stderr noemt niet alle zeshonderddrieëntwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvierentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-eight.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-eight', 'six-hundred-thirty-nine')
(ROOT / 'verify-six-hundred-thirty-nine.py').write_text(verify_text)
print('verify-six-hundred-thirty-nine.py')
