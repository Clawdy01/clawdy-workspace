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
    'create-five-hundred-eighty-seven-assets.py',
    'create-five-hundred-eighty-eight-assets.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('[:572]', '[:573]'),
        ('!= 572', '!= 573'),
        ('kreeg 572', 'kreeg 573'),
        ('559, 560, 561, 562, 563', '560, 561, 562, 563, 564'),
    ],
)

build(
    'create-five-hundred-eighty-seven-bootstrap.py',
    'create-five-hundred-eighty-eight-bootstrap.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('all_cases[:572]', 'all_cases[:573]'),
        ('{UNKNOWN, TYPO}][:572]', '{UNKNOWN, TYPO}][:573]'),
        ('!= 572', '!= 573'),
        ('kreeg 572', 'kreeg 573'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'create-five-hundred-eighty-seven-minimal.py',
    'create-five-hundred-eighty-eight-minimal.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('!= 572', '!= 573'),
        ('kreeg 572', 'kreeg 573'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
    ],
)

build(
    'make-five-hundred-eighty-seven.py',
    'make-five-hundred-eighty-eight.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('all_cases[:572]', 'all_cases[:573]'),
        ('{UNKNOWN, TYPO}][:572]', '{UNKNOWN, TYPO}][:573]'),
        ('!= 572', '!= 573'),
        ('495, 496, 497, 498, 499', '496, 497, 498, 499, 500'),
    ],
)

build(
    'create-five-hundred-eighty-seven-files.py',
    'create-five-hundred-eighty-eight-files.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('all_cases[:572]', 'all_cases[:573]'),
        ('{UNKNOWN, TYPO}][:572]', '{UNKNOWN, TYPO}][:573]'),
        ('!= 572', '!= 573'),
        ('495, 496, 497, 498, 499', '496, 497, 498, 499, 500'),
    ],
)

build(
    'create-five-hundred-eighty-seven.py',
    'create-five-hundred-eighty-eight.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('all_cases[:572]', 'all_cases[:573]'),
        ('{UNKNOWN, TYPO}][:572]', '{UNKNOWN, TYPO}][:573]'),
        ('!= 572', '!= 573'),
        ('498, 499, 500, 501, 502', '499, 500, 501, 502, 503'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-seven.py',
    'generate-validate-five-hundred-eighty-eight.py',
    [
        ('five-hundred-eighty-seven', 'five-hundred-eighty-eight'),
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('all_cases[:572]', 'all_cases[:573]'),
        ('{UNKNOWN, TYPO}][:572]', '{UNKNOWN, TYPO}][:573]'),
        ('!= 572', '!= 573'),
        ('495, 496, 497, 498, 499', '496, 497, 498, 499, 500'),
    ],
)

build(
    'validate-five-hundred-eighty-seven-valid-list-cases.py',
    'validate-five-hundred-eighty-eight-valid-list-cases.py',
    [
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
        ('all_cases[:572]', 'all_cases[:573]'),
        ('len(valid_cases) != 572', 'len(valid_cases) != 573'),
    ],
)

build(
    'validate-five-hundred-eighty-seven-valid-mixed.py',
    'validate-five-hundred-eighty-eight-valid-mixed.py',
    [
        ('vijfhonderdzevenentachtig', 'vijfhonderdachtentachtig'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
        ('][:572]', '][:573]'),
        ('len(valid_cases) != 572', 'len(valid_cases) != 573'),
        ('plain stderr noemt niet alle vijfhonderdtweeënzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderddrieënzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-seven.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-seven', 'five-hundred-eighty-eight')
(ROOT / 'verify-five-hundred-eighty-eight.py').write_text(verify_text)
print('verify-five-hundred-eighty-eight.py')
