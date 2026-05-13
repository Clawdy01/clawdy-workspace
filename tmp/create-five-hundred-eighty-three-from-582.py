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
    'create-five-hundred-eighty-two-assets.py',
    'create-five-hundred-eighty-three-assets.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('[:567]', '[:568]'),
        ('!= 567', '!= 568'),
        ('kreeg 567', 'kreeg 568'),
        ('554, 555, 556, 557, 558', '555, 556, 557, 558, 559'),
    ],
)

build(
    'create-five-hundred-eighty-two-bootstrap.py',
    'create-five-hundred-eighty-three-bootstrap.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('all_cases[:567]', 'all_cases[:568]'),
        ('{UNKNOWN, TYPO}][:567]', '{UNKNOWN, TYPO}][:568]'),
        ('!= 567', '!= 568'),
        ('kreeg 567', 'kreeg 568'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'create-five-hundred-eighty-two-minimal.py',
    'create-five-hundred-eighty-three-minimal.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('!= 567', '!= 568'),
        ('kreeg 567', 'kreeg 568'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'make-five-hundred-eighty-two.py',
    'make-five-hundred-eighty-three.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('all_cases[:567]', 'all_cases[:568]'),
        ('{UNKNOWN, TYPO}][:567]', '{UNKNOWN, TYPO}][:568]'),
        ('!= 567', '!= 568'),
        ('490, 491, 492, 493, 494', '491, 492, 493, 494, 495'),
    ],
)

build(
    'create-five-hundred-eighty-two-files.py',
    'create-five-hundred-eighty-three-files.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('all_cases[:567]', 'all_cases[:568]'),
        ('{UNKNOWN, TYPO}][:567]', '{UNKNOWN, TYPO}][:568]'),
        ('!= 567', '!= 568'),
        ('490, 491, 492, 493, 494', '491, 492, 493, 494, 495'),
    ],
)

build(
    'create-five-hundred-eighty-two.py',
    'create-five-hundred-eighty-three.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('all_cases[:567]', 'all_cases[:568]'),
        ('{UNKNOWN, TYPO}][:567]', '{UNKNOWN, TYPO}][:568]'),
        ('!= 567', '!= 568'),
        ('493, 494, 495, 496, 497', '494, 495, 496, 497, 498'),
    ],
)

build(
    'generate-validate-five-hundred-eighty-two.py',
    'generate-validate-five-hundred-eighty-three.py',
    [
        ('five-hundred-eighty-two', 'five-hundred-eighty-three'),
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('all_cases[:567]', 'all_cases[:568]'),
        ('{UNKNOWN, TYPO}][:567]', '{UNKNOWN, TYPO}][:568]'),
        ('!= 567', '!= 568'),
        ('490, 491, 492, 493, 494', '491, 492, 493, 494, 495'),
    ],
)

build(
    'validate-five-hundred-eighty-two-valid-list-cases.py',
    'validate-five-hundred-eighty-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
        ('all_cases[:567]', 'all_cases[:568]'),
        ('len(valid_cases) != 567', 'len(valid_cases) != 568'),
    ],
)

build(
    'validate-five-hundred-eighty-two-valid-mixed.py',
    'validate-five-hundred-eighty-three-valid-mixed.py',
    [
        ('vijfhonderdtweeëntachtig', 'vijfhonderddrieëntachtig'),
        ('552, 553, 554, 555, 556', '553, 554, 555, 556, 557'),
        ('][:567]', '][:568]'),
        ('len(valid_cases) != 567', 'len(valid_cases) != 568'),
        ('plain stderr noemt niet alle vijfhonderdzevenenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdachtenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-eighty-two.py').read_text()
verify_text = verify_src.replace('five-hundred-eighty-two', 'five-hundred-eighty-three')
(ROOT / 'verify-five-hundred-eighty-three.py').write_text(verify_text)
print('verify-five-hundred-eighty-three.py')
