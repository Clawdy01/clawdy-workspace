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
    'create-five-hundred-eighty-four-assets.py',
    'create-five-hundred-eighty-five-assets.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('[:569]', '[:570]'),
        ('!= 569', '!= 570'),
        ('kreeg 569', 'kreeg 570'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'create-five-hundred-eighty-four-bootstrap.py',
    'create-five-hundred-eighty-five-bootstrap.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('all_cases[:569]', 'all_cases[:570]'),
        ('{UNKNOWN, TYPO}][:569]', '{UNKNOWN, TYPO}][:570]'),
        ('!= 569', '!= 570'),
        ('kreeg 569', 'kreeg 570'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'create-five-hundred-eighty-four-minimal.py',
    'create-five-hundred-eighty-five-minimal.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('!= 569', '!= 570'),
        ('kreeg 569', 'kreeg 570'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
    ],
)

build(
    'make-five-hundred-eighty-four.py',
    'make-five-hundred-eighty-five.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('all_cases[:569]', 'all_cases[:570]'),
        ('{UNKNOWN, TYPO}][:569]', '{UNKNOWN, TYPO}][:570]'),
        ('!= 569', '!= 570'),
        ('492, 493, 494, 495, 496', '493, 494, 495, 496, 497'),
    ],
)

build(
    'create-five-hundred-eighty-four-files.py',
    'create-five-hundred-eighty-five-files.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('all_cases[:569]', 'all_cases[:570]'),
        ('{UNKNOWN, TYPO}][:569]', '{UNKNOWN, TYPO}][:570]'),
        ('!= 569', '!= 570'),
        ('492, 493, 494, 495, 496', '493, 494, 495, 496, 497'),
    ],
)

build(
    'create-five-hundred-eighty-four.py',
    'create-five-hundred-eighty-five.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('all_cases[:569]', 'all_cases[:570]'),
        ('{UNKNOWN, TYPO}][:569]', '{UNKNOWN, TYPO}][:570]'),
        ('!= 569', '!= 570'),
        ('495, 496, 497, 498, 499', '496, 497, 498, 499, 500'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-four.py',
    'generate-validate-five-hundred-eighty-five.py',
    [
        ('five-hundred-eighty-four', 'five-hundred-eighty-five'),
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('all_cases[:569]', 'all_cases[:570]'),
        ('{UNKNOWN, TYPO}][:569]', '{UNKNOWN, TYPO}][:570]'),
        ('!= 569', '!= 570'),
        ('492, 493, 494, 495, 496', '493, 494, 495, 496, 497'),
    ],
)

build(
    'validate-five-hundred-eighty-four-valid-list-cases.py',
    'validate-five-hundred-eighty-five-valid-list-cases.py',
    [
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
        ('all_cases[:569]', 'all_cases[:570]'),
        ('len(valid_cases) != 569', 'len(valid_cases) != 570'),
    ],
)

build(
    'validate-five-hundred-eighty-four-valid-mixed.py',
    'validate-five-hundred-eighty-five-valid-mixed.py',
    [
        ('vijfhonderdvierentachtig', 'vijfhonderdvijfentachtig'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
        ('][:569]', '][:570]'),
        ('len(valid_cases) != 569', 'len(valid_cases) != 570'),
        ('plain stderr noemt niet alle vijfhonderdnegenenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-four.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-four', 'five-hundred-eighty-five')
(ROOT / 'verify-five-hundred-eighty-five.py').write_text(verify_text)
print('verify-five-hundred-eighty-five.py')
