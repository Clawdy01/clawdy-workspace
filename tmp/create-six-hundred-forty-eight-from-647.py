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
    'create-six-hundred-forty-seven-assets.py',
    'create-six-hundred-forty-eight-assets.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('[:632]', '[:633]'),
        ('!= 632', '!= 633'),
        ('kreeg 632', 'kreeg 633'),
        ('619, 620, 621, 622, 623', '620, 621, 622, 623, 624'),
    ],
)

build(
    'create-six-hundred-forty-seven-bootstrap.py',
    'create-six-hundred-forty-eight-bootstrap.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('all_cases[:632]', 'all_cases[:633]'),
        ('{UNKNOWN, TYPO}][:632]', '{UNKNOWN, TYPO}][:633]'),
        ('!= 632', '!= 633'),
        ('kreeg 632', 'kreeg 633'),
        ('615, 616, 617, 618, 619', '616, 617, 618, 619, 620'),
    ],
)

build(
    'create-six-hundred-forty-seven-minimal.py',
    'create-six-hundred-forty-eight-minimal.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('!= 632', '!= 633'),
        ('kreeg 632', 'kreeg 633'),
        ('615, 616, 617, 618, 619', '616, 617, 618, 619, 620'),
    ],
)

build(
    'make-six-hundred-forty-seven.py',
    'make-six-hundred-forty-eight.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('all_cases[:632]', 'all_cases[:633]'),
        ('{UNKNOWN, TYPO}][:632]', '{UNKNOWN, TYPO}][:633]'),
        ('!= 632', '!= 633'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'create-six-hundred-forty-seven-files.py',
    'create-six-hundred-forty-eight-files.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('all_cases[:632]', 'all_cases[:633]'),
        ('{UNKNOWN, TYPO}][:632]', '{UNKNOWN, TYPO}][:633]'),
        ('!= 632', '!= 633'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'create-six-hundred-forty-seven.py',
    'create-six-hundred-forty-eight.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('all_cases[:632]', 'all_cases[:633]'),
        ('{UNKNOWN, TYPO}][:632]', '{UNKNOWN, TYPO}][:633]'),
        ('!= 632', '!= 633'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'generate-validate-six-hundred-forty-seven.py',
    'generate-validate-six-hundred-forty-eight.py',
    [
        ('six-hundred-forty-seven', 'six-hundred-forty-eight'),
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('all_cases[:632]', 'all_cases[:633]'),
        ('{UNKNOWN, TYPO}][:632]', '{UNKNOWN, TYPO}][:633]'),
        ('!= 632', '!= 633'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'validate-six-hundred-forty-seven-valid-list-cases.py',
    'validate-six-hundred-forty-eight-valid-list-cases.py',
    [
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('617, 618, 619, 620, 621', '618, 619, 620, 621, 622'),
        ('all_cases[:632]', 'all_cases[:633]'),
        ('len(valid_cases) != 632', 'len(valid_cases) != 633'),
    ],
)

build(
    'validate-six-hundred-forty-seven-valid-mixed.py',
    'validate-six-hundred-forty-eight-valid-mixed.py',
    [
        ('zeshonderdzevenenveertig', 'zeshonderdachtenveertig'),
        ('617, 618, 619, 620, 621', '618, 619, 620, 621, 622'),
        ('][:632]', '][:633]'),
        ('len(valid_cases) != 632', 'len(valid_cases) != 633'),
        ('plain stderr noemt niet alle zeshonderdtweeëndertig geldige first-seen cases', 'plain stderr noemt niet alle zeshonderddrieëndertig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-forty-seven.py').read_text()
verify_text = verify_src.replace('six-hundred-forty-seven', 'six-hundred-forty-eight')
(ROOT / 'verify-six-hundred-forty-eight.py').write_text(verify_text)
print('verify-six-hundred-forty-eight.py')
