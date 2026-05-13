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
    'create-five-hundred-sixty-five-assets.py',
    'create-five-hundred-sixty-six-assets.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('[:550]', '[:551]'),
        ('!= 550', '!= 551'),
        ('kreeg 550', 'kreeg 551'),
        ('537, 538, 539, 540, 541', '538, 539, 540, 541, 542'),
    ],
)

build(
    'create-five-hundred-sixty-five-bootstrap.py',
    'create-five-hundred-sixty-six-bootstrap.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('all_cases[:550]', 'all_cases[:551]'),
        ('{UNKNOWN, TYPO}][:550]', '{UNKNOWN, TYPO}][:551]'),
        ('!= 550', '!= 551'),
        ('kreeg 550', 'kreeg 551'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'create-five-hundred-sixty-five-minimal.py',
    'create-five-hundred-sixty-six-minimal.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('!= 550', '!= 551'),
        ('kreeg 550', 'kreeg 551'),
        ('533, 534, 535, 536, 537', '534, 535, 536, 537, 538'),
    ],
)

build(
    'make-five-hundred-sixty-five.py',
    'make-five-hundred-sixty-six.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('all_cases[:550]', 'all_cases[:551]'),
        ('{UNKNOWN, TYPO}][:550]', '{UNKNOWN, TYPO}][:551]'),
        ('!= 550', '!= 551'),
        ('473, 474, 475, 476, 477', '474, 475, 476, 477, 478'),
    ],
)

build(
    'create-five-hundred-sixty-five-files.py',
    'create-five-hundred-sixty-six-files.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('all_cases[:550]', 'all_cases[:551]'),
        ('{UNKNOWN, TYPO}][:550]', '{UNKNOWN, TYPO}][:551]'),
        ('!= 550', '!= 551'),
        ('473, 474, 475, 476, 477', '474, 475, 476, 477, 478'),
    ],
)

build(
    'create-five-hundred-sixty-five.py',
    'create-five-hundred-sixty-six.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('all_cases[:550]', 'all_cases[:551]'),
        ('{UNKNOWN, TYPO}][:550]', '{UNKNOWN, TYPO}][:551]'),
        ('!= 550', '!= 551'),
        ('476, 477, 478, 479, 480', '477, 478, 479, 480, 481'),
    ],
)

build(
    'generate-validate-five-hundred-sixty-five.py',
    'generate-validate-five-hundred-sixty-six.py',
    [
        ('five-hundred-sixty-five', 'five-hundred-sixty-six'),
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('all_cases[:550]', 'all_cases[:551]'),
        ('{UNKNOWN, TYPO}][:550]', '{UNKNOWN, TYPO}][:551]'),
        ('!= 550', '!= 551'),
        ('473, 474, 475, 476, 477', '474, 475, 476, 477, 478'),
    ],
)

build(
    'validate-five-hundred-sixty-five-valid-list-cases.py',
    'validate-five-hundred-sixty-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
        ('all_cases[:550]', 'all_cases[:551]'),
        ('len(valid_cases) != 550', 'len(valid_cases) != 551'),
    ],
)

build(
    'validate-five-hundred-sixty-five-valid-mixed.py',
    'validate-five-hundred-sixty-six-valid-mixed.py',
    [
        ('vijfhonderdvijfenzestig', 'vijfhonderdzesenzestig'),
        ('535, 536, 537, 538, 539', '536, 537, 538, 539, 540'),
        ('][:550]', '][:551]'),
        ('len(valid_cases) != 550', 'len(valid_cases) != 551'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-sixty-five.py').read_text()
verify_text = verify_src.replace('five-hundred-sixty-five', 'five-hundred-sixty-six')
(ROOT / 'verify-five-hundred-sixty-six.py').write_text(verify_text)
print('verify-five-hundred-sixty-six.py')
