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
    'create-five-hundred-thirty-two-assets.py',
    'create-five-hundred-thirty-three-assets.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('[:517]', '[:518]'),
        ('!= 517', '!= 518'),
        ('kreeg 517', 'kreeg 518'),
        ('498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508', '498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509'),
    ],
)

build(
    'create-five-hundred-thirty-two-bootstrap.py',
    'create-five-hundred-thirty-three-bootstrap.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('all_cases[:517]', 'all_cases[:518]'),
        ('{UNKNOWN, TYPO}][:517]', '{UNKNOWN, TYPO}][:518]'),
        ('!= 517', '!= 518'),
        ('kreeg 517', 'kreeg 518'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505'),
    ],
)

build(
    'create-five-hundred-thirty-two-minimal.py',
    'create-five-hundred-thirty-three-minimal.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('!= 517', '!= 518'),
        ('kreeg 517', 'kreeg 518'),
        (' 458)', ' 459)'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505'),
    ],
)

build(
    'make-five-hundred-thirty-two.py',
    'make-five-hundred-thirty-three.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('all_cases[:517]', 'all_cases[:518]'),
        ('{UNKNOWN, TYPO}][:517]', '{UNKNOWN, TYPO}][:518]'),
        ('!= 517', '!= 518'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445'),
    ],
)

build(
    'create-five-hundred-thirty-two-files.py',
    'create-five-hundred-thirty-three-files.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('all_cases[:517]', 'all_cases[:518]'),
        ('{UNKNOWN, TYPO}][:517]', '{UNKNOWN, TYPO}][:518]'),
        ('!= 517', '!= 518'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445'),
    ],
)

build(
    'create-five-hundred-thirty-two.py',
    'create-five-hundred-thirty-three.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('all_cases[:517]', 'all_cases[:518]'),
        ('{UNKNOWN, TYPO}][:517]', '{UNKNOWN, TYPO}][:518]'),
        ('!= 517', '!= 518'),
        ('437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447', '437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-two.py',
    'generate-validate-five-hundred-thirty-three.py',
    [
        ('five-hundred-thirty-two', 'five-hundred-thirty-three'),
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('all_cases[:517]', 'all_cases[:518]'),
        ('{UNKNOWN, TYPO}][:517]', '{UNKNOWN, TYPO}][:518]'),
        ('!= 517', '!= 518'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445'),
    ],
)

build(
    'validate-five-hundred-thirty-two-valid-list-cases.py',
    'validate-five-hundred-thirty-three-valid-list-cases.py',
    [
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507'),
        ('all_cases[:517]', 'all_cases[:518]'),
        ('len(valid_cases) != 517', 'len(valid_cases) != 518'),
    ],
)

build(
    'validate-five-hundred-thirty-two-valid-mixed.py',
    'validate-five-hundred-thirty-three-valid-mixed.py',
    [
        ('vijfhonderdtweeëndertig', 'vijfhonderddrieëndertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507'),
        ('][:517]', '][:518]'),
        ('len(valid_cases) != 517', 'len(valid_cases) != 518'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-two.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-two', 'five-hundred-thirty-three')
(ROOT / 'verify-five-hundred-thirty-three.py').write_text(verify_text)
print('verify-five-hundred-thirty-three.py')
