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
    'create-six-hundred-twelve-assets.py',
    'create-six-hundred-thirteen-assets.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('[:597]', '[:598]'),
        ('!= 597', '!= 598'),
        ('kreeg 597', 'kreeg 598'),
        ('584, 585, 586, 587, 588', '585, 586, 587, 588, 589'),
    ],
)

build(
    'create-six-hundred-twelve-bootstrap.py',
    'create-six-hundred-thirteen-bootstrap.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('all_cases[:597]', 'all_cases[:598]'),
        ('{UNKNOWN, TYPO}][:597]', '{UNKNOWN, TYPO}][:598]'),
        ('!= 597', '!= 598'),
        ('kreeg 597', 'kreeg 598'),
        ('580, 581, 582, 583, 584', '581, 582, 583, 584, 585'),
    ],
)

build(
    'create-six-hundred-twelve-minimal.py',
    'create-six-hundred-thirteen-minimal.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('!= 597', '!= 598'),
        ('kreeg 597', 'kreeg 598'),
        ('580, 581, 582, 583, 584', '581, 582, 583, 584, 585'),
    ],
)

build(
    'make-six-hundred-twelve.py',
    'make-six-hundred-thirteen.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('all_cases[:597]', 'all_cases[:598]'),
        ('{UNKNOWN, TYPO}][:597]', '{UNKNOWN, TYPO}][:598]'),
        ('!= 597', '!= 598'),
        ('520, 521, 522, 523, 524', '521, 522, 523, 524, 525'),
    ],
)

build(
    'create-six-hundred-twelve-files.py',
    'create-six-hundred-thirteen-files.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('all_cases[:597]', 'all_cases[:598]'),
        ('{UNKNOWN, TYPO}][:597]', '{UNKNOWN, TYPO}][:598]'),
        ('!= 597', '!= 598'),
        ('520, 521, 522, 523, 524', '521, 522, 523, 524, 525'),
    ],
)

build(
    'create-six-hundred-twelve.py',
    'create-six-hundred-thirteen.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('all_cases[:597]', 'all_cases[:598]'),
        ('{UNKNOWN, TYPO}][:597]', '{UNKNOWN, TYPO}][:598]'),
        ('!= 597', '!= 598'),
        ('523, 524, 525, 526, 527', '524, 525, 526, 527, 528'),
    ],
)

build(
    'generate-validate-six-hundred-twelve.py',
    'generate-validate-six-hundred-thirteen.py',
    [
        ('six-hundred-twelve', 'six-hundred-thirteen'),
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('all_cases[:597]', 'all_cases[:598]'),
        ('{UNKNOWN, TYPO}][:597]', '{UNKNOWN, TYPO}][:598]'),
        ('!= 597', '!= 598'),
        ('520, 521, 522, 523, 524', '521, 522, 523, 524, 525'),
    ],
)

build(
    'validate-six-hundred-twelve-valid-list-cases.py',
    'validate-six-hundred-thirteen-valid-list-cases.py',
    [
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('582, 583, 584, 585, 586', '583, 584, 585, 586, 587'),
        ('all_cases[:597]', 'all_cases[:598]'),
        ('len(valid_cases) != 597', 'len(valid_cases) != 598'),
    ],
)

build(
    'validate-six-hundred-twelve-valid-mixed.py',
    'validate-six-hundred-thirteen-valid-mixed.py',
    [
        ('zeshonderdtwaalf', 'zeshonderddertien'),
        ('582, 583, 584, 585, 586', '583, 584, 585, 586, 587'),
        ('][:597]', '][:598]'),
        ('len(valid_cases) != 597', 'len(valid_cases) != 598'),
        ('plain stderr noemt niet alle vijfhonderdzevenennegentig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdachtennegentig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twelve.py').read_text()
verify_text = verify_src.replace('six-hundred-twelve', 'six-hundred-thirteen')
(ROOT / 'verify-six-hundred-thirteen.py').write_text(verify_text)
print('verify-six-hundred-thirteen.py')
