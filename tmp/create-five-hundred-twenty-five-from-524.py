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
    'create-five-hundred-twenty-four-assets.py',
    'create-five-hundred-twenty-five-assets.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('[:509]', '[:510]'),
        ('!= 509', '!= 510'),
        ('kreeg 509', 'kreeg 510'),
        ('498, 499, 500]', '498, 499, 500, 501]'),
    ],
)

build(
    'create-five-hundred-twenty-four-bootstrap.py',
    'create-five-hundred-twenty-five-bootstrap.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('all_cases[:509]', 'all_cases[:510]'),
        ('{UNKNOWN, TYPO}][:509]', '{UNKNOWN, TYPO}][:510]'),
        ('!= 509', '!= 510'),
        ('kreeg 509', 'kreeg 510'),
        ('494, 495, 496]', '494, 495, 496, 497]'),
    ],
)

build(
    'create-five-hundred-twenty-four-minimal.py',
    'create-five-hundred-twenty-five-minimal.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('!= 509', '!= 510'),
        ('kreeg 509', 'kreeg 510'),
        (' 450)', ' 451)'),
        ('494, 495, 496]', '494, 495, 496, 497]'),
    ],
)

build(
    'make-five-hundred-twenty-four.py',
    'make-five-hundred-twenty-five.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('all_cases[:509]', 'all_cases[:510]'),
        ('{UNKNOWN, TYPO}][:509]', '{UNKNOWN, TYPO}][:510]'),
        ('!= 509', '!= 510'),
        ('434, 435, 436]', '434, 435, 436, 437]'),
    ],
)

build(
    'create-five-hundred-twenty-four-files.py',
    'create-five-hundred-twenty-five-files.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('all_cases[:509]', 'all_cases[:510]'),
        ('{UNKNOWN, TYPO}][:509]', '{UNKNOWN, TYPO}][:510]'),
        ('!= 509', '!= 510'),
        ('434, 435, 436]', '434, 435, 436, 437]'),
    ],
)

build(
    'create-five-hundred-twenty-four.py',
    'create-five-hundred-twenty-five.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('all_cases[:509]', 'all_cases[:510]'),
        ('{UNKNOWN, TYPO}][:509]', '{UNKNOWN, TYPO}][:510]'),
        ('!= 509', '!= 510'),
        ('437, 438, 439]', '437, 438, 439, 440]'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-four.py',
    'generate-validate-five-hundred-twenty-five.py',
    [
        ('five-hundred-twenty-four', 'five-hundred-twenty-five'),
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('all_cases[:509]', 'all_cases[:510]'),
        ('{UNKNOWN, TYPO}][:509]', '{UNKNOWN, TYPO}][:510]'),
        ('!= 509', '!= 510'),
        ('434, 435, 436]', '434, 435, 436, 437]'),
    ],
)

build(
    'validate-five-hundred-twenty-four-valid-list-cases.py',
    'validate-five-hundred-twenty-five-valid-list-cases.py',
    [
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('497, 498]', '497, 498, 499]'),
        ('all_cases[:509]', 'all_cases[:510]'),
        ('len(valid_cases) != 509', 'len(valid_cases) != 510'),
    ],
)

build(
    'validate-five-hundred-twenty-four-valid-mixed.py',
    'validate-five-hundred-twenty-five-valid-mixed.py',
    [
        ('vijfhonderdvierentwintig', 'vijfhonderdvijfentwintig'),
        ('497, 498]', '497, 498, 499]'),
        ('][:509]', '][:510]'),
        ('len(valid_cases) != 509', 'len(valid_cases) != 510'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-four.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-four', 'five-hundred-twenty-five')
(ROOT / 'verify-five-hundred-twenty-five.py').write_text(verify_text)
print('verify-five-hundred-twenty-five.py')
