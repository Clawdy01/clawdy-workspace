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
    'create-five-hundred-seventy-nine-assets.py',
    'create-five-hundred-eighty-assets.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('[:564]', '[:565]'),
        ('!= 564', '!= 565'),
        ('kreeg 564', 'kreeg 565'),
        ('551, 552, 553, 554, 555', '552, 553, 554, 555, 556'),
    ],
)

build(
    'create-five-hundred-seventy-nine-bootstrap.py',
    'create-five-hundred-eighty-bootstrap.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('all_cases[:564]', 'all_cases[:565]'),
        ('{UNKNOWN, TYPO}][:564]', '{UNKNOWN, TYPO}][:565]'),
        ('!= 564', '!= 565'),
        ('kreeg 564', 'kreeg 565'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'create-five-hundred-seventy-nine-minimal.py',
    'create-five-hundred-eighty-minimal.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('!= 564', '!= 565'),
        ('kreeg 564', 'kreeg 565'),
        ('547, 548, 549, 550, 551', '548, 549, 550, 551, 552'),
    ],
)

build(
    'make-five-hundred-seventy-nine.py',
    'make-five-hundred-eighty.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('all_cases[:564]', 'all_cases[:565]'),
        ('{UNKNOWN, TYPO}][:564]', '{UNKNOWN, TYPO}][:565]'),
        ('!= 564', '!= 565'),
        ('487, 488, 489, 490, 491', '488, 489, 490, 491, 492'),
    ],
)

build(
    'create-five-hundred-seventy-nine-files.py',
    'create-five-hundred-eighty-files.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('all_cases[:564]', 'all_cases[:565]'),
        ('{UNKNOWN, TYPO}][:564]', '{UNKNOWN, TYPO}][:565]'),
        ('!= 564', '!= 565'),
        ('487, 488, 489, 490, 491', '488, 489, 490, 491, 492'),
    ],
)

build(
    'create-five-hundred-seventy-nine.py',
    'create-five-hundred-eighty.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('all_cases[:564]', 'all_cases[:565]'),
        ('{UNKNOWN, TYPO}][:564]', '{UNKNOWN, TYPO}][:565]'),
        ('!= 564', '!= 565'),
        ('490, 491, 492, 493, 494', '491, 492, 493, 494, 495'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-nine.py',
    'generate-validate-five-hundred-eighty.py',
    [
        ('five-hundred-seventy-nine', 'five-hundred-eighty'),
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('all_cases[:564]', 'all_cases[:565]'),
        ('{UNKNOWN, TYPO}][:564]', '{UNKNOWN, TYPO}][:565]'),
        ('!= 564', '!= 565'),
        ('487, 488, 489, 490, 491', '488, 489, 490, 491, 492'),
    ],
)

build(
    'validate-five-hundred-seventy-nine-valid-list-cases.py',
    'validate-five-hundred-eighty-valid-list-cases.py',
    [
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
        ('all_cases[:564]', 'all_cases[:565]'),
        ('len(valid_cases) != 564', 'len(valid_cases) != 565'),
    ],
)

build(
    'validate-five-hundred-seventy-nine-valid-mixed.py',
    'validate-five-hundred-eighty-valid-mixed.py',
    [
        ('vijfhonderdnegenenzeventig', 'vijfhonderdtachtig'),
        ('549, 550, 551, 552, 553', '550, 551, 552, 553, 554'),
        ('][:564]', '][:565]'),
        ('len(valid_cases) != 564', 'len(valid_cases) != 565'),
        ('plain stderr noemt niet alle vijfhonderdvierenzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvijfenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-nine.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-nine', 'five-hundred-eighty')
(ROOT / 'verify-five-hundred-eighty.py').write_text(verify_text)
print('verify-five-hundred-eighty.py')
