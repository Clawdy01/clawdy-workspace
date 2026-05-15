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
    'create-six-hundred-forty-four-assets.py',
    'create-six-hundred-forty-five-assets.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('[:629]', '[:630]'),
        ('!= 629', '!= 630'),
        ('kreeg 629', 'kreeg 630'),
        ('616, 617, 618, 619, 620', '617, 618, 619, 620, 621'),
    ],
)

build(
    'create-six-hundred-forty-four-bootstrap.py',
    'create-six-hundred-forty-five-bootstrap.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('all_cases[:629]', 'all_cases[:630]'),
        ('{UNKNOWN, TYPO}][:629]', '{UNKNOWN, TYPO}][:630]'),
        ('!= 629', '!= 630'),
        ('kreeg 629', 'kreeg 630'),
        ('612, 613, 614, 615, 616', '613, 614, 615, 616, 617'),
    ],
)

build(
    'create-six-hundred-forty-four-minimal.py',
    'create-six-hundred-forty-five-minimal.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('!= 629', '!= 630'),
        ('kreeg 629', 'kreeg 630'),
        ('612, 613, 614, 615, 616', '613, 614, 615, 616, 617'),
    ],
)

build(
    'make-six-hundred-forty-four.py',
    'make-six-hundred-forty-five.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('all_cases[:629]', 'all_cases[:630]'),
        ('{UNKNOWN, TYPO}][:629]', '{UNKNOWN, TYPO}][:630]'),
        ('!= 629', '!= 630'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'create-six-hundred-forty-four-files.py',
    'create-six-hundred-forty-five-files.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('all_cases[:629]', 'all_cases[:630]'),
        ('{UNKNOWN, TYPO}][:629]', '{UNKNOWN, TYPO}][:630]'),
        ('!= 629', '!= 630'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'create-six-hundred-forty-four.py',
    'create-six-hundred-forty-five.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('all_cases[:629]', 'all_cases[:630]'),
        ('{UNKNOWN, TYPO}][:629]', '{UNKNOWN, TYPO}][:630]'),
        ('!= 629', '!= 630'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'generate-validate-six-hundred-forty-four.py',
    'generate-validate-six-hundred-forty-five.py',
    [
        ('six-hundred-forty-four', 'six-hundred-forty-five'),
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('all_cases[:629]', 'all_cases[:630]'),
        ('{UNKNOWN, TYPO}][:629]', '{UNKNOWN, TYPO}][:630]'),
        ('!= 629', '!= 630'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'validate-six-hundred-forty-four-valid-list-cases.py',
    'validate-six-hundred-forty-five-valid-list-cases.py',
    [
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('614, 615, 616, 617, 618', '615, 616, 617, 618, 619'),
        ('all_cases[:629]', 'all_cases[:630]'),
        ('len(valid_cases) != 629', 'len(valid_cases) != 630'),
    ],
)

build(
    'validate-six-hundred-forty-four-valid-mixed.py',
    'validate-six-hundred-forty-five-valid-mixed.py',
    [
        ('zeshonderdvierenveertig', 'zeshonderdvijfenveertig'),
        ('614, 615, 616, 617, 618', '615, 616, 617, 618, 619'),
        ('][:629]', '][:630]'),
        ('len(valid_cases) != 629', 'len(valid_cases) != 630'),
        ('plain stderr noemt niet alle zeshonderdnegenentwintig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderddertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-four.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-four', 'six-hundred-forty-five')
(ROOT / 'verify-six-hundred-forty-five.py').write_text(verify_text)
print('verify-six-hundred-forty-five.py')
