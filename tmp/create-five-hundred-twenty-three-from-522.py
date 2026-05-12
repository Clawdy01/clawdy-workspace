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
    'create-five-hundred-twenty-two-assets.py',
    'create-five-hundred-twenty-three-assets.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('[:507]', '[:508]'),
        ('!= 507', '!= 508'),
        ('kreeg 507', 'kreeg 508'),
        ('497, 498]', '497, 498, 499]'),
    ],
)

build(
    'create-five-hundred-twenty-two-bootstrap.py',
    'create-five-hundred-twenty-three-bootstrap.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('all_cases[:507]', 'all_cases[:508]'),
        ('{UNKNOWN, TYPO}][:507]', '{UNKNOWN, TYPO}][:508]'),
        ('!= 507', '!= 508'),
        ('kreeg 507', 'kreeg 508'),
        ('493, 494]', '493, 494, 495]'),
    ],
)

build(
    'create-five-hundred-twenty-two-minimal.py',
    'create-five-hundred-twenty-three-minimal.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('!= 507', '!= 508'),
        ('kreeg 507', 'kreeg 508'),
        (' 448)', ' 449)'),
        ('493, 494]', '493, 494, 495]'),
    ],
)

build(
    'make-five-hundred-twenty-two.py',
    'make-five-hundred-twenty-three.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('all_cases[:507]', 'all_cases[:508]'),
        ('{UNKNOWN, TYPO}][:507]', '{UNKNOWN, TYPO}][:508]'),
        ('!= 507', '!= 508'),
        ('433, 434]', '433, 434, 435]'),
    ],
)

build(
    'create-five-hundred-twenty-two-files.py',
    'create-five-hundred-twenty-three-files.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('all_cases[:507]', 'all_cases[:508]'),
        ('{UNKNOWN, TYPO}][:507]', '{UNKNOWN, TYPO}][:508]'),
        ('!= 507', '!= 508'),
        ('433, 434]', '433, 434, 435]'),
    ],
)

build(
    'create-five-hundred-twenty-two.py',
    'create-five-hundred-twenty-three.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('all_cases[:507]', 'all_cases[:508]'),
        ('{UNKNOWN, TYPO}][:507]', '{UNKNOWN, TYPO}][:508]'),
        ('!= 507', '!= 508'),
        ('436, 437]', '436, 437, 438]'),
    ],
)

build(
    'generate-validate-five-hundred-twenty-two.py',
    'generate-validate-five-hundred-twenty-three.py',
    [
        ('five-hundred-twenty-two', 'five-hundred-twenty-three'),
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('all_cases[:507]', 'all_cases[:508]'),
        ('{UNKNOWN, TYPO}][:507]', '{UNKNOWN, TYPO}][:508]'),
        ('!= 507', '!= 508'),
        ('433, 434]', '433, 434, 435]'),
    ],
)

build(
    'validate-five-hundred-twenty-two-valid-list-cases.py',
    'validate-five-hundred-twenty-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('495, 496]', '495, 496, 497]'),
        ('all_cases[:507]', 'all_cases[:508]'),
        ('len(valid_cases) != 507', 'len(valid_cases) != 508'),
    ],
)

build(
    'validate-five-hundred-twenty-two-valid-mixed.py',
    'validate-five-hundred-twenty-three-valid-mixed.py',
    [
        ('vijfhonderdtweeëntwintig', 'vijfhonderddrieëntwintig'),
        ('495, 496]', '495, 496, 497]'),
        ('][:507]', '][:508]'),
        ('len(valid_cases) != 507', 'len(valid_cases) != 508'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-twenty-two.py').read_text()
verify_text = verify_src.replace('five-hundred-twenty-two', 'five-hundred-twenty-three')
(ROOT / 'verify-five-hundred-twenty-three.py').write_text(verify_text)
print('verify-five-hundred-twenty-three.py')
