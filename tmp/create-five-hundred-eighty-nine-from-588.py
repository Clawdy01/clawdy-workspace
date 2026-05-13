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
    'create-five-hundred-eighty-eight-assets.py',
    'create-five-hundred-eighty-nine-assets.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('[:573]', '[:574]'),
        ('!= 573', '!= 574'),
        ('kreeg 573', 'kreeg 574'),
        ('560, 561, 562, 563, 564', '561, 562, 563, 564, 565'),
    ],
)

build(
    'create-five-hundred-eighty-eight-bootstrap.py',
    'create-five-hundred-eighty-nine-bootstrap.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('all_cases[:573]', 'all_cases[:574]'),
        ('{UNKNOWN, TYPO}][:573]', '{UNKNOWN, TYPO}][:574]'),
        ('!= 573', '!= 574'),
        ('kreeg 573', 'kreeg 574'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'create-five-hundred-eighty-eight-minimal.py',
    'create-five-hundred-eighty-nine-minimal.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('!= 573', '!= 574'),
        ('kreeg 573', 'kreeg 574'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
    ],
)

build(
    'make-five-hundred-eighty-eight.py',
    'make-five-hundred-eighty-nine.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('all_cases[:573]', 'all_cases[:574]'),
        ('{UNKNOWN, TYPO}][:573]', '{UNKNOWN, TYPO}][:574]'),
        ('!= 573', '!= 574'),
        ('496, 497, 498, 499, 500', '497, 498, 499, 500, 501'),
    ],
)

build(
    'create-five-hundred-eighty-eight-files.py',
    'create-five-hundred-eighty-nine-files.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('all_cases[:573]', 'all_cases[:574]'),
        ('{UNKNOWN, TYPO}][:573]', '{UNKNOWN, TYPO}][:574]'),
        ('!= 573', '!= 574'),
        ('496, 497, 498, 499, 500', '497, 498, 499, 500, 501'),
    ],
)

build(
    'create-five-hundred-eighty-eight.py',
    'create-five-hundred-eighty-nine.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('all_cases[:573]', 'all_cases[:574]'),
        ('{UNKNOWN, TYPO}][:573]', '{UNKNOWN, TYPO}][:574]'),
        ('!= 573', '!= 574'),
        ('499, 500, 501, 502, 503', '500, 501, 502, 503, 504'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-eight.py',
    'generate-validate-five-hundred-eighty-nine.py',
    [
        ('five-hundred-eighty-eight', 'five-hundred-eighty-nine'),
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('all_cases[:573]', 'all_cases[:574]'),
        ('{UNKNOWN, TYPO}][:573]', '{UNKNOWN, TYPO}][:574]'),
        ('!= 573', '!= 574'),
        ('496, 497, 498, 499, 500', '497, 498, 499, 500, 501'),
    ],
)

build(
    'validate-five-hundred-eighty-eight-valid-list-cases.py',
    'validate-five-hundred-eighty-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
        ('all_cases[:573]', 'all_cases[:574]'),
        ('len(valid_cases) != 573', 'len(valid_cases) != 574'),
    ],
)

build(
    'validate-five-hundred-eighty-eight-valid-mixed.py',
    'validate-five-hundred-eighty-nine-valid-mixed.py',
    [
        ('vijfhonderdachtentachtig', 'vijfhonderdnegenentachtig'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
        ('][:573]', '][:574]'),
        ('len(valid_cases) != 573', 'len(valid_cases) != 574'),
        ('plain stderr noemt niet alle vijfhonderddrieënzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvierenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-eight', 'five-hundred-eighty-nine')
(ROOT / 'verify-five-hundred-eighty-nine.py').write_text(verify_text)
print('verify-five-hundred-eighty-nine.py')
