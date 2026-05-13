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
    'create-five-hundred-eighty-six-assets.py',
    'create-five-hundred-eighty-seven-assets.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('[:571]', '[:572]'),
        ('!= 571', '!= 572'),
        ('kreeg 571', 'kreeg 572'),
        ('558, 559, 560, 561, 562', '559, 560, 561, 562, 563'),
    ],
)

build(
    'create-five-hundred-eighty-six-bootstrap.py',
    'create-five-hundred-eighty-seven-bootstrap.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('all_cases[:571]', 'all_cases[:572]'),
        ('{UNKNOWN, TYPO}][:571]', '{UNKNOWN, TYPO}][:572]'),
        ('!= 571', '!= 572'),
        ('kreeg 571', 'kreeg 572'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'create-five-hundred-eighty-six-minimal.py',
    'create-five-hundred-eighty-seven-minimal.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('!= 571', '!= 572'),
        ('kreeg 571', 'kreeg 572'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'make-five-hundred-eighty-six.py',
    'make-five-hundred-eighty-seven.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('all_cases[:571]', 'all_cases[:572]'),
        ('{UNKNOWN, TYPO}][:571]', '{UNKNOWN, TYPO}][:572]'),
        ('!= 571', '!= 572'),
        ('494, 495, 496, 497, 498', '495, 496, 497, 498, 499'),
    ],
)

build(
    'create-five-hundred-eighty-six-files.py',
    'create-five-hundred-eighty-seven-files.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('all_cases[:571]', 'all_cases[:572]'),
        ('{UNKNOWN, TYPO}][:571]', '{UNKNOWN, TYPO}][:572]'),
        ('!= 571', '!= 572'),
        ('494, 495, 496, 497, 498', '495, 496, 497, 498, 499'),
    ],
)

build(
    'create-five-hundred-eighty-six.py',
    'create-five-hundred-eighty-seven.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('all_cases[:571]', 'all_cases[:572]'),
        ('{UNKNOWN, TYPO}][:571]', '{UNKNOWN, TYPO}][:572]'),
        ('!= 571', '!= 572'),
        ('497, 498, 499, 500, 501', '498, 499, 500, 501, 502'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-six.py',
    'generate-validate-five-hundred-eighty-seven.py',
    [
        ('five-hundred-eighty-six', 'five-hundred-eighty-seven'),
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('all_cases[:571]', 'all_cases[:572]'),
        ('{UNKNOWN, TYPO}][:571]', '{UNKNOWN, TYPO}][:572]'),
        ('!= 571', '!= 572'),
        ('494, 495, 496, 497, 498', '495, 496, 497, 498, 499'),
    ],
)

build(
    'validate-five-hundred-eighty-six-valid-list-cases.py',
    'validate-five-hundred-eighty-seven-valid-list-cases.py',
    [
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
        ('all_cases[:571]', 'all_cases[:572]'),
        ('len(valid_cases) != 571', 'len(valid_cases) != 572'),
    ],
)

build(
    'validate-five-hundred-eighty-six-valid-mixed.py',
    'validate-five-hundred-eighty-seven-valid-mixed.py',
    [
        ('vijfhonderdzesentachtig', 'vijfhonderdzevenentachtig'),
        ('556, 557, 558, 559, 560', '557, 558, 559, 560, 561'),
        ('][:571]', '][:572]'),
        ('len(valid_cases) != 571', 'len(valid_cases) != 572'),
        ('plain stderr noemt niet alle vijfhonderdeenenzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdtweeënzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-six.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-six', 'five-hundred-eighty-seven')
(ROOT / 'verify-five-hundred-eighty-seven.py').write_text(verify_text)
print('verify-five-hundred-eighty-seven.py')
