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
    'create-five-hundred-sixty-six-assets.py',
    'create-five-hundred-sixty-seven-assets.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('[:551]', '[:552]'),
        ('!= 551', '!= 552'),
        ('kreeg 551', 'kreeg 552'),
        ('538, 539, 540, 541, 542', '539, 540, 541, 542, 543'),
    ],
)

build(
    'create-five-hundred-sixty-six-bootstrap.py',
    'create-five-hundred-sixty-seven-bootstrap.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('all_cases[:551]', 'all_cases[:552]'),
        ('{UNKNOWN, TYPO}][:551]', '{UNKNOWN, TYPO}][:552]'),
        ('!= 551', '!= 552'),
        ('kreeg 551', 'kreeg 552'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'create-five-hundred-sixty-six-minimal.py',
    'create-five-hundred-sixty-seven-minimal.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('!= 551', '!= 552'),
        ('kreeg 551', 'kreeg 552'),
        ('534, 535, 536, 537, 538', '535, 536, 537, 538, 539'),
    ],
)

build(
    'make-five-hundred-sixty-six.py',
    'make-five-hundred-sixty-seven.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('all_cases[:551]', 'all_cases[:552]'),
        ('{UNKNOWN, TYPO}][:551]', '{UNKNOWN, TYPO}][:552]'),
        ('!= 551', '!= 552'),
        ('474, 475, 476, 477, 478', '475, 476, 477, 478, 479'),
    ],
)

build(
    'create-five-hundred-sixty-six-files.py',
    'create-five-hundred-sixty-seven-files.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('all_cases[:551]', 'all_cases[:552]'),
        ('{UNKNOWN, TYPO}][:551]', '{UNKNOWN, TYPO}][:552]'),
        ('!= 551', '!= 552'),
        ('474, 475, 476, 477, 478', '475, 476, 477, 478, 479'),
    ],
)

build(
    'create-five-hundred-sixty-six.py',
    'create-five-hundred-sixty-seven.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('all_cases[:551]', 'all_cases[:552]'),
        ('{UNKNOWN, TYPO}][:551]', '{UNKNOWN, TYPO}][:552]'),
        ('!= 551', '!= 552'),
        ('477, 478, 479, 480, 481', '478, 479, 480, 481, 482'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-six.py',
    'generate-validate-five-hundred-sixty-seven.py',
    [
        ('five-hundred-sixty-six', 'five-hundred-sixty-seven'),
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('all_cases[:551]', 'all_cases[:552]'),
        ('{UNKNOWN, TYPO}][:551]', '{UNKNOWN, TYPO}][:552]'),
        ('!= 551', '!= 552'),
        ('474, 475, 476, 477, 478', '475, 476, 477, 478, 479'),
    ],
)

build(
    'validate-five-hundred-sixty-six-valid-list-cases.py',
    'validate-five-hundred-sixty-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
        ('all_cases[:551]', 'all_cases[:552]'),
        ('len(valid_cases) != 551', 'len(valid_cases) != 552'),
    ],
)

build(
    'validate-five-hundred-sixty-six-valid-mixed.py',
    'validate-five-hundred-sixty-seven-valid-mixed.py',
    [
        ('vijfhonderdzesenzestig', 'vijfhonderdzevenenzestig'),
        ('536, 537, 538, 539, 540', '537, 538, 539, 540, 541'),
        ('][:551]', '][:552]'),
        ('len(valid_cases) != 551', 'len(valid_cases) != 552'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-six.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-six', 'five-hundred-sixty-seven')
(ROOT / 'verify-five-hundred-sixty-seven.py').write_text(verify_text)
print('verify-five-hundred-sixty-seven.py')
