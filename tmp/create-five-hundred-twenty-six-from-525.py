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
    'create-five-hundred-twenty-five-assets.py',
    'create-five-hundred-twenty-six-assets.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('[:510]', '[:511]'),
        ('!= 510', '!= 511'),
        ('kreeg 510', 'kreeg 511'),
        ('498, 499, 500, 501', '498, 499, 500, 501, 502'),
    ],
)

build(
    'create-five-hundred-twenty-five-bootstrap.py',
    'create-five-hundred-twenty-six-bootstrap.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('all_cases[:510]', 'all_cases[:511]'),
        ('{UNKNOWN, TYPO}][:510]', '{UNKNOWN, TYPO}][:511]'),
        ('!= 510', '!= 511'),
        ('kreeg 510', 'kreeg 511'),
        ('494, 495, 496, 497', '494, 495, 496, 497, 498'),
    ],
)

build(
    'create-five-hundred-twenty-five-minimal.py',
    'create-five-hundred-twenty-six-minimal.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('!= 510', '!= 511'),
        ('kreeg 510', 'kreeg 511'),
        (' 451)', ' 452)'),
        ('494, 495, 496, 497', '494, 495, 496, 497, 498'),
    ],
)

build(
    'make-five-hundred-twenty-five.py',
    'make-five-hundred-twenty-six.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('all_cases[:510]', 'all_cases[:511]'),
        ('{UNKNOWN, TYPO}][:510]', '{UNKNOWN, TYPO}][:511]'),
        ('!= 510', '!= 511'),
        ('434, 435, 436, 437', '434, 435, 436, 437, 438'),
    ],
)

build(
    'create-five-hundred-twenty-five-files.py',
    'create-five-hundred-twenty-six-files.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('all_cases[:510]', 'all_cases[:511]'),
        ('{UNKNOWN, TYPO}][:510]', '{UNKNOWN, TYPO}][:511]'),
        ('!= 510', '!= 511'),
        ('434, 435, 436, 437', '434, 435, 436, 437, 438'),
    ],
)

build(
    'create-five-hundred-twenty-five.py',
    'create-five-hundred-twenty-six.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('all_cases[:510]', 'all_cases[:511]'),
        ('{UNKNOWN, TYPO}][:510]', '{UNKNOWN, TYPO}][:511]'),
        ('!= 510', '!= 511'),
        ('437, 438, 439, 440', '437, 438, 439, 440, 441'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-five.py',
    'generate-validate-five-hundred-twenty-six.py',
    [
        ('five-hundred-twenty-five', 'five-hundred-twenty-six'),
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('all_cases[:510]', 'all_cases[:511]'),
        ('{UNKNOWN, TYPO}][:510]', '{UNKNOWN, TYPO}][:511]'),
        ('!= 510', '!= 511'),
        ('434, 435, 436, 437', '434, 435, 436, 437, 438'),
    ],
)

build(
    'validate-five-hundred-twenty-five-valid-list-cases.py',
    'validate-five-hundred-twenty-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('497, 498, 499', '497, 498, 499, 500'),
        ('all_cases[:510]', 'all_cases[:511]'),
        ('len(valid_cases) != 510', 'len(valid_cases) != 511'),
    ],
)

build(
    'validate-five-hundred-twenty-five-valid-mixed.py',
    'validate-five-hundred-twenty-six-valid-mixed.py',
    [
        ('vijfhonderdvijfentwintig', 'vijfhonderdzesentwintig'),
        ('497, 498, 499', '497, 498, 499, 500'),
        ('][:510]', '][:511]'),
        ('len(valid_cases) != 510', 'len(valid_cases) != 511'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-five.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-five', 'five-hundred-twenty-six')
(ROOT / 'verify-five-hundred-twenty-six.py').write_text(verify_text)
print('verify-five-hundred-twenty-six.py')
