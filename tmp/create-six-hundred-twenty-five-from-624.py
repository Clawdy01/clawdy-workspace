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
    'create-six-hundred-twenty-four-assets.py',
    'create-six-hundred-twenty-five-assets.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('[:609]', '[:610]'),
        ('!= 609', '!= 610'),
        ('kreeg 609', 'kreeg 610'),
        ('596, 597, 598, 599, 600', '597, 598, 599, 600, 601'),
    ],
)

build(
    'create-six-hundred-twenty-four-bootstrap.py',
    'create-six-hundred-twenty-five-bootstrap.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('all_cases[:609]', 'all_cases[:610]'),
        ('{UNKNOWN, TYPO}][:609]', '{UNKNOWN, TYPO}][:610]'),
        ('!= 609', '!= 610'),
        ('kreeg 609', 'kreeg 610'),
        ('592, 593, 594, 595, 596', '593, 594, 595, 596, 597'),
    ],
)

build(
    'create-six-hundred-twenty-four-minimal.py',
    'create-six-hundred-twenty-five-minimal.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('!= 609', '!= 610'),
        ('kreeg 609', 'kreeg 610'),
        ('592, 593, 594, 595, 596', '593, 594, 595, 596, 597'),
    ],
)

build(
    'make-six-hundred-twenty-four.py',
    'make-six-hundred-twenty-five.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('all_cases[:609]', 'all_cases[:610]'),
        ('{UNKNOWN, TYPO}][:609]', '{UNKNOWN, TYPO}][:610]'),
        ('!= 609', '!= 610'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
    ],
)

build(
    'create-six-hundred-twenty-four-files.py',
    'create-six-hundred-twenty-five-files.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('all_cases[:609]', 'all_cases[:610]'),
        ('{UNKNOWN, TYPO}][:609]', '{UNKNOWN, TYPO}][:610]'),
        ('!= 609', '!= 610'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
    ],
)

build(
    'create-six-hundred-twenty-four.py',
    'create-six-hundred-twenty-five.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('all_cases[:609]', 'all_cases[:610]'),
        ('{UNKNOWN, TYPO}][:609]', '{UNKNOWN, TYPO}][:610]'),
        ('!= 609', '!= 610'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-four.py',
    'generate-validate-six-hundred-twenty-five.py',
    [
        ('six-hundred-twenty-four', 'six-hundred-twenty-five'),
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('all_cases[:609]', 'all_cases[:610]'),
        ('{UNKNOWN, TYPO}][:609]', '{UNKNOWN, TYPO}][:610]'),
        ('!= 609', '!= 610'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
    ],
)

build(
    'validate-six-hundred-twenty-four-valid-list-cases.py',
    'validate-six-hundred-twenty-five-valid-list-cases.py',
    [
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('594, 595, 596, 597, 598', '595, 596, 597, 598, 599'),
        ('all_cases[:609]', 'all_cases[:610]'),
        ('len(valid_cases) != 609', 'len(valid_cases) != 610'),
    ],
)

build(
    'validate-six-hundred-twenty-four-valid-mixed.py',
    'validate-six-hundred-twenty-five-valid-mixed.py',
    [
        ('zeshonderdvierentwintig', 'zeshonderdvijfentwintig'),
        ('594, 595, 596, 597, 598', '595, 596, 597, 598, 599'),
        ('][:609]', '][:610]'),
        ('len(valid_cases) != 609', 'len(valid_cases) != 610'),
        ('plain stderr noemt niet alle zeshonderdnegen geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdtien geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-four.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-four', 'six-hundred-twenty-five')
(ROOT / 'verify-six-hundred-twenty-five.py').write_text(verify_text)
print('verify-six-hundred-twenty-five.py')
