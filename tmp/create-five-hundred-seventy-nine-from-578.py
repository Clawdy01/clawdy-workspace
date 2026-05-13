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
    'create-five-hundred-seventy-eight-assets.py',
    'create-five-hundred-seventy-nine-assets.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('[:563]', '[:564]'),
        ('!= 563', '!= 564'),
        ('kreeg 563', 'kreeg 564'),
        ('550, 551, 552, 553, 554', '551, 552, 553, 554, 555'),
    ],
)

build(
    'create-five-hundred-seventy-eight-bootstrap.py',
    'create-five-hundred-seventy-nine-bootstrap.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('all_cases[:563]', 'all_cases[:564]'),
        ('{UNKNOWN, TYPO}][:563]', '{UNKNOWN, TYPO}][:564]'),
        ('!= 563', '!= 564'),
        ('kreeg 563', 'kreeg 564'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'create-five-hundred-seventy-eight-minimal.py',
    'create-five-hundred-seventy-nine-minimal.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('!= 563', '!= 564'),
        ('kreeg 563', 'kreeg 564'),
        ('546, 547, 548, 549, 550', '547, 548, 549, 550, 551'),
    ],
)

build(
    'make-five-hundred-seventy-eight.py',
    'make-five-hundred-seventy-nine.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('all_cases[:563]', 'all_cases[:564]'),
        ('{UNKNOWN, TYPO}][:563]', '{UNKNOWN, TYPO}][:564]'),
        ('!= 563', '!= 564'),
        ('486, 487, 488, 489, 490', '487, 488, 489, 490, 491'),
    ],
)

build(
    'create-five-hundred-seventy-eight-files.py',
    'create-five-hundred-seventy-nine-files.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('all_cases[:563]', 'all_cases[:564]'),
        ('{UNKNOWN, TYPO}][:563]', '{UNKNOWN, TYPO}][:564]'),
        ('!= 563', '!= 564'),
        ('486, 487, 488, 489, 490', '487, 488, 489, 490, 491'),
    ],
)

build(
    'create-five-hundred-seventy-eight.py',
    'create-five-hundred-seventy-nine.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('all_cases[:563]', 'all_cases[:564]'),
        ('{UNKNOWN, TYPO}][:563]', '{UNKNOWN, TYPO}][:564]'),
        ('!= 563', '!= 564'),
        ('489, 490, 491, 492, 493', '490, 491, 492, 493, 494'),
    ],
)

build(
    'generate-validate-five-hundred-seventy-eight.py',
    'generate-validate-five-hundred-seventy-nine.py',
    [
        ('five-hundred-seventy-eight', 'five-hundred-seventy-nine'),
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('all_cases[:563]', 'all_cases[:564]'),
        ('{UNKNOWN, TYPO}][:563]', '{UNKNOWN, TYPO}][:564]'),
        ('!= 563', '!= 564'),
        ('486, 487, 488, 489, 490', '487, 488, 489, 490, 491'),
    ],
)

build(
    'validate-five-hundred-seventy-eight-valid-list-cases.py',
    'validate-five-hundred-seventy-nine-valid-list-cases.py',
    [
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
        ('all_cases[:563]', 'all_cases[:564]'),
        ('len(valid_cases) != 563', 'len(valid_cases) != 564'),
    ],
)

build(
    'validate-five-hundred-seventy-eight-valid-mixed.py',
    'validate-five-hundred-seventy-nine-valid-mixed.py',
    [
        ('vijfhonderdachtenzeventig', 'vijfhonderdnegenenzeventig'),
        ('548, 549, 550, 551, 552', '549, 550, 551, 552, 553'),
        ('][:563]', '][:564]'),
        ('len(valid_cases) != 563', 'len(valid_cases) != 564'),
        ('plain stderr noemt niet alle vijfhonderddrieënzestig geldige first-seen cases', 'plain stderr noemt niet alle vijfhonderdvierenzestig geldige first-seen cases'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-seventy-eight.py').read_text()
verify_text = verify_src.replace('five-hundred-seventy-eight', 'five-hundred-seventy-nine')
(ROOT / 'verify-five-hundred-seventy-nine.py').write_text(verify_text)
print('verify-five-hundred-seventy-nine.py')
