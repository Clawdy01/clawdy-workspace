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
    'create-five-hundred-sixty-three-assets.py',
    'create-five-hundred-sixty-four-assets.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('[:548]', '[:549]'),
        ('!= 548', '!= 549'),
        ('kreeg 548', 'kreeg 549'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
    ],
)

build(
    'create-five-hundred-sixty-three-bootstrap.py',
    'create-five-hundred-sixty-four-bootstrap.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('all_cases[:548]', 'all_cases[:549]'),
        ('{UNKNOWN, TYPO}][:548]', '{UNKNOWN, TYPO}][:549]'),
        ('!= 548', '!= 549'),
        ('kreeg 548', 'kreeg 549'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
    ],
)

build(
    'create-five-hundred-sixty-three-minimal.py',
    'create-five-hundred-sixty-four-minimal.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('!= 548', '!= 549'),
        ('kreeg 548', 'kreeg 549'),
        ('531, 532, 533, 534, 535', '532, 533, 534, 535, 536'),
    ],
)

build(
    'make-five-hundred-sixty-three.py',
    'make-five-hundred-sixty-four.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('all_cases[:548]', 'all_cases[:549]'),
        ('{UNKNOWN, TYPO}][:548]', '{UNKNOWN, TYPO}][:549]'),
        ('!= 548', '!= 549'),
        ('471, 472, 473, 474, 475', '472, 473, 474, 475, 476'),
    ],
)

build(
    'create-five-hundred-sixty-three-files.py',
    'create-five-hundred-sixty-four-files.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('all_cases[:548]', 'all_cases[:549]'),
        ('{UNKNOWN, TYPO}][:548]', '{UNKNOWN, TYPO}][:549]'),
        ('!= 548', '!= 549'),
        ('471, 472, 473, 474, 475', '472, 473, 474, 475, 476'),
    ],
)

build(
    'create-five-hundred-sixty-three.py',
    'create-five-hundred-sixty-four.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('all_cases[:548]', 'all_cases[:549]'),
        ('{UNKNOWN, TYPO}][:548]', '{UNKNOWN, TYPO}][:549]'),
        ('!= 548', '!= 549'),
        ('474, 475, 476, 477, 478', '475, 476, 477, 478, 479'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-three.py',
    'generate-validate-five-hundred-sixty-four.py',
    [
        ('five-hundred-sixty-three', 'five-hundred-sixty-four'),
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('all_cases[:548]', 'all_cases[:549]'),
        ('{UNKNOWN, TYPO}][:548]', '{UNKNOWN, TYPO}][:549]'),
        ('!= 548', '!= 549'),
        ('471, 472, 473, 474, 475', '472, 473, 474, 475, 476'),
    ],
)

build(
    'validate-five-hundred-sixty-three-valid-list-cases.py',
    'validate-five-hundred-sixty-four-valid-list-cases.py',
    [
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
        ('all_cases[:548]', 'all_cases[:549]'),
        ('len(valid_cases) != 548', 'len(valid_cases) != 549'),
    ],
)

build(
    'validate-five-hundred-sixty-three-valid-mixed.py',
    'validate-five-hundred-sixty-four-valid-mixed.py',
    [
        ('vijfhonderddrieënzestig', 'vijfhonderdvierenzestig'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
        ('][:548]', '][:549]'),
        ('len(valid_cases) != 548', 'len(valid_cases) != 549'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-three.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-three', 'five-hundred-sixty-four')
(ROOT / 'verify-five-hundred-sixty-four.py').write_text(verify_text)
print('verify-five-hundred-sixty-four.py')
