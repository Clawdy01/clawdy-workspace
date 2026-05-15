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
    'create-six-hundred-thirty-nine-assets.py',
    'create-six-hundred-forty-assets.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('[:624]', '[:625]'),
        ('!= 624', '!= 625'),
        ('kreeg 624', 'kreeg 625'),
        ('611, 612, 613, 614, 615', '612, 613, 614, 615, 616'),
    ],
)

build(
    'create-six-hundred-thirty-nine-bootstrap.py',
    'create-six-hundred-forty-bootstrap.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('all_cases[:624]', 'all_cases[:625]'),
        ('{UNKNOWN, TYPO}][:624]', '{UNKNOWN, TYPO}][:625]'),
        ('!= 624', '!= 625'),
        ('kreeg 624', 'kreeg 625'),
        ('607, 608, 609, 610, 611', '608, 609, 610, 611, 612'),
    ],
)

build(
    'create-six-hundred-thirty-nine-minimal.py',
    'create-six-hundred-forty-minimal.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('!= 624', '!= 625'),
        ('kreeg 624', 'kreeg 625'),
        ('607, 608, 609, 610, 611', '608, 609, 610, 611, 612'),
    ],
)

build(
    'make-six-hundred-thirty-nine.py',
    'make-six-hundred-forty.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('all_cases[:624]', 'all_cases[:625]'),
        ('{UNKNOWN, TYPO}][:624]', '{UNKNOWN, TYPO}][:625]'),
        ('!= 624', '!= 625'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'create-six-hundred-thirty-nine-files.py',
    'create-six-hundred-forty-files.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('all_cases[:624]', 'all_cases[:625]'),
        ('{UNKNOWN, TYPO}][:624]', '{UNKNOWN, TYPO}][:625]'),
        ('!= 624', '!= 625'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'create-six-hundred-thirty-nine.py',
    'create-six-hundred-forty.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('all_cases[:624]', 'all_cases[:625]'),
        ('{UNKNOWN, TYPO}][:624]', '{UNKNOWN, TYPO}][:625]'),
        ('!= 624', '!= 625'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'generate-validate-six-hundred-thirty-nine.py',
    'generate-validate-six-hundred-forty.py',
    [
        ('six-hundred-thirty-nine', 'six-hundred-forty'),
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('all_cases[:624]', 'all_cases[:625]'),
        ('{UNKNOWN, TYPO}][:624]', '{UNKNOWN, TYPO}][:625]'),
        ('!= 624', '!= 625'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'validate-six-hundred-thirty-nine-valid-list-cases.py',
    'validate-six-hundred-forty-valid-list-cases.py',
    [
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('609, 610, 611, 612, 613', '610, 611, 612, 613, 614'),
        ('all_cases[:624]', 'all_cases[:625]'),
        ('len(valid_cases) != 624', 'len(valid_cases) != 625'),
    ],
)

build(
    'validate-six-hundred-thirty-nine-valid-mixed.py',
    'validate-six-hundred-forty-valid-mixed.py',
    [
        ('zeshonderdnegenendertig', 'zeshonderdveertig'),
        ('609, 610, 611, 612, 613', '610, 611, 612, 613, 614'),
        ('][:624]', '][:625]'),
        ('len(valid_cases) != 624', 'len(valid_cases) != 625'),
        ('plain stderr noemt niet alle zeshonderdvierentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdvijfentwintig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-thirty-nine.py').read_text()
verify_text = verify_src.replace('six-hundred-thirty-nine', 'six-hundred-forty')
(ROOT / 'verify-six-hundred-forty.py').write_text(verify_text)
print('verify-six-hundred-forty.py')
