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
    'create-five-hundred-eighty-five-assets.py',
    'create-five-hundred-eighty-six-assets.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('[:570]', '[:571]'),
        ('!= 570', '!= 571'),
        ('kreeg 570', 'kreeg 571'),
        ('557, 558, 559, 560, 561', '558, 559, 560, 561, 562'),
    ],
)

build(
    'create-five-hundred-eighty-five-bootstrap.py',
    'create-five-hundred-eighty-six-bootstrap.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('all_cases[:570]', 'all_cases[:571]'),
        ('{UNKNOWN, TYPO}][:570]', '{UNKNOWN, TYPO}][:571]'),
        ('!= 570', '!= 571'),
        ('kreeg 570', 'kreeg 571'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'create-five-hundred-eighty-five-minimal.py',
    'create-five-hundred-eighty-six-minimal.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('!= 570', '!= 571'),
        ('kreeg 570', 'kreeg 571'),
        ('553, 554, 555, 556, 557', '554, 555, 556, 557, 558'),
    ],
)

build(
    'make-five-hundred-eighty-five.py',
    'make-five-hundred-eighty-six.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('all_cases[:570]', 'all_cases[:571]'),
        ('{UNKNOWN, TYPO}][:570]', '{UNKNOWN, TYPO}][:571]'),
        ('!= 570', '!= 571'),
        ('493, 494, 495, 496, 497', '494, 495, 496, 497, 498'),
    ],
)

build(
    'create-five-hundred-eighty-five-files.py',
    'create-five-hundred-eighty-six-files.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('all_cases[:570]', 'all_cases[:571]'),
        ('{UNKNOWN, TYPO}][:570]', '{UNKNOWN, TYPO}][:571]'),
        ('!= 570', '!= 571'),
        ('493, 494, 495, 496, 497', '494, 495, 496, 497, 498'),
    ],
)

build(
    'create-five-hundred-eighty-five.py',
    'create-five-hundred-eighty-six.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('all_cases[:570]', 'all_cases[:571]'),
        ('{UNKNOWN, TYPO}][:570]', '{UNKNOWN, TYPO}][:571]'),
        ('!= 570', '!= 571'),
        ('496, 497, 498, 499, 500', '497, 498, 499, 500, 501'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-five.py',
    'generate-validate-five-hundred-eighty-six.py',
    [
        ('five-hundred-eighty-five', 'five-hundred-eighty-six'),
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('all_cases[:570]', 'all_cases[:571]'),
        ('{UNKNOWN, TYPO}][:570]', '{UNKNOWN, TYPO}][:571]'),
        ('!= 570', '!= 571'),
        ('493, 494, 495, 496, 497', '494, 495, 496, 497, 498'),
    ],
)

build(
    'validate-five-hundred-eighty-five-valid-list-cases.py',
    'validate-five-hundred-eighty-six-valid-list-cases.py',
    [
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
        ('all_cases[:570]', 'all_cases[:571]'),
        ('len(valid_cases) != 570', 'len(valid_cases) != 571'),
    ],
)

build(
    'validate-five-hundred-eighty-five-valid-mixed.py',
    'validate-five-hundred-eighty-six-valid-mixed.py',
    [
        ('vijfhonderdvijfentachtig', 'vijfhonderdzesentachtig'),
        ('555, 556, 557, 558, 559', '556, 557, 558, 559, 560'),
        ('][:570]', '][:571]'),
        ('len(valid_cases) != 570', 'len(valid_cases) != 571'),
        ('plain stderr noemt niet alle vijfhonderdzeventig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdeenenzeventig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-five.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-five', 'five-hundred-eighty-six')
(ROOT / 'verify-five-hundred-eighty-six.py').write_text(verify_text)
print('verify-five-hundred-eighty-six.py')
