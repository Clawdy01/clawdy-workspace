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
    'create-five-hundred-sixty-four-assets.py',
    'create-five-hundred-sixty-five-assets.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('[:549]', '[:550]'),
        ('!= 549', '!= 550'),
        ('kreeg 549', 'kreeg 550'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
    ],
)

build(
    'create-five-hundred-sixty-four-bootstrap.py',
    'create-five-hundred-sixty-five-bootstrap.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('all_cases[:549]', 'all_cases[:550]'),
        ('{UNKNOWN, TYPO}][:549]', '{UNKNOWN, TYPO}][:550]'),
        ('!= 549', '!= 550'),
        ('kreeg 549', 'kreeg 550'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
    ],
)

build(
    'create-five-hundred-sixty-four-minimal.py',
    'create-five-hundred-sixty-five-minimal.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('!= 549', '!= 550'),
        ('kreeg 549', 'kreeg 550'),
        ('532, 533, 534, 535, 536', '533, 534, 535, 536, 537'),
    ],
)

build(
    'make-five-hundred-sixty-four.py',
    'make-five-hundred-sixty-five.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('all_cases[:549]', 'all_cases[:550]'),
        ('{UNKNOWN, TYPO}][:549]', '{UNKNOWN, TYPO}][:550]'),
        ('!= 549', '!= 550'),
        ('472, 473, 474, 475, 476', '473, 474, 475, 476, 477'),
    ],
)

build(
    'create-five-hundred-sixty-four-files.py',
    'create-five-hundred-sixty-five-files.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('all_cases[:549]', 'all_cases[:550]'),
        ('{UNKNOWN, TYPO}][:549]', '{UNKNOWN, TYPO}][:550]'),
        ('!= 549', '!= 550'),
        ('472, 473, 474, 475, 476', '473, 474, 475, 476, 477'),
    ],
)

build(
    'create-five-hundred-sixty-four.py',
    'create-five-hundred-sixty-five.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('all_cases[:549]', 'all_cases[:550]'),
        ('{UNKNOWN, TYPO}][:549]', '{UNKNOWN, TYPO}][:550]'),
        ('!= 549', '!= 550'),
        ('475, 476, 477, 478, 479', '476, 477, 478, 479, 480'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-four.py',
    'generate-validate-five-hundred-sixty-five.py',
    [
        ('five-hundred-sixty-four', 'five-hundred-sixty-five'),
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('all_cases[:549]', 'all_cases[:550]'),
        ('{UNKNOWN, TYPO}][:549]', '{UNKNOWN, TYPO}][:550]'),
        ('!= 549', '!= 550'),
        ('472, 473, 474, 475, 476', '473, 474, 475, 476, 477'),
    ],
)

build(
    'validate-five-hundred-sixty-four-valid-list-cases.py',
    'validate-five-hundred-sixty-five-valid-list-cases.py',
    [
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
        ('all_cases[:549]', 'all_cases[:550]'),
        ('len(valid_cases) != 549', 'len(valid_cases) != 550'),
    ],
)

build(
    'validate-five-hundred-sixty-four-valid-mixed.py',
    'validate-five-hundred-sixty-five-valid-mixed.py',
    [
        ('vijfhonderdvierenzestig', 'vijfhonderdvijfenzestig'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
        ('][:549]', '][:550]'),
        ('len(valid_cases) != 549', 'len(valid_cases) != 550'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-four.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-four', 'five-hundred-sixty-five')
(ROOT / 'verify-five-hundred-sixty-five.py').write_text(verify_text)
print('verify-five-hundred-sixty-five.py')
