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
    'create-six-hundred-twenty-five-assets.py',
    'create-six-hundred-twenty-six-assets.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('[:610]', '[:611]'),
        ('!= 610', '!= 611'),
        ('kreeg 610', 'kreeg 611'),
        ('597, 598, 599, 600, 601', '598, 599, 600, 601, 602'),
    ],
)

build(
    'create-six-hundred-twenty-five-bootstrap.py',
    'create-six-hundred-twenty-six-bootstrap.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('all_cases[:610]', 'all_cases[:611]'),
        ('{UNKNOWN, TYPO}][:610]', '{UNKNOWN, TYPO}][:611]'),
        ('!= 610', '!= 611'),
        ('kreeg 610', 'kreeg 611'),
        ('593, 594, 595, 596, 597', '594, 595, 596, 597, 598'),
    ],
)

build(
    'create-six-hundred-twenty-five-minimal.py',
    'create-six-hundred-twenty-six-minimal.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('!= 610', '!= 611'),
        ('kreeg 610', 'kreeg 611'),
        ('593, 594, 595, 596, 597', '594, 595, 596, 597, 598'),
    ],
)

build(
    'make-six-hundred-twenty-five.py',
    'make-six-hundred-twenty-six.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('all_cases[:610]', 'all_cases[:611]'),
        ('{UNKNOWN, TYPO}][:610]', '{UNKNOWN, TYPO}][:611]'),
        ('!= 610', '!= 611'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'create-six-hundred-twenty-five-files.py',
    'create-six-hundred-twenty-six-files.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('all_cases[:610]', 'all_cases[:611]'),
        ('{UNKNOWN, TYPO}][:610]', '{UNKNOWN, TYPO}][:611]'),
        ('!= 610', '!= 611'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'create-six-hundred-twenty-five.py',
    'create-six-hundred-twenty-six.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('all_cases[:610]', 'all_cases[:611]'),
        ('{UNKNOWN, TYPO}][:610]', '{UNKNOWN, TYPO}][:611]'),
        ('!= 610', '!= 611'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'generate-validate-six-hundred-twenty-five.py',
    'generate-validate-six-hundred-twenty-six.py',
    [
        ('six-hundred-twenty-five', 'six-hundred-twenty-six'),
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('all_cases[:610]', 'all_cases[:611]'),
        ('{UNKNOWN, TYPO}][:610]', '{UNKNOWN, TYPO}][:611]'),
        ('!= 610', '!= 611'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'validate-six-hundred-twenty-five-valid-list-cases.py',
    'validate-six-hundred-twenty-six-valid-list-cases.py',
    [
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('595, 596, 597, 598, 599', '596, 597, 598, 599, 600'),
        ('all_cases[:610]', 'all_cases[:611]'),
        ('len(valid_cases) != 610', 'len(valid_cases) != 611'),
    ],
)

build(
    'validate-six-hundred-twenty-five-valid-mixed.py',
    'validate-six-hundred-twenty-six-valid-mixed.py',
    [
        ('zeshonderdvijfentwintig', 'zeshonderdzesentwintig'),
        ('595, 596, 597, 598, 599', '596, 597, 598, 599, 600'),
        ('][:610]', '][:611]'),
        ('len(valid_cases) != 610', 'len(valid_cases) != 611'),
        ('plain stderr noemt niet alle zeshonderdtien geldige first-seen cases', 'plain stderr noemt niet alle zeshonderdelf geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-six-hundred-twenty-five.py').read_text()
verify_text = verify_src.replace('six-hundred-twenty-five', 'six-hundred-twenty-six')
(ROOT / 'verify-six-hundred-twenty-six.py').write_text(verify_text)
print('verify-six-hundred-twenty-six.py')
