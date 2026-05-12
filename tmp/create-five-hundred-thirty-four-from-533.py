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
    'create-five-hundred-thirty-three-assets.py',
    'create-five-hundred-thirty-four-assets.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('[:518]', '[:519]'),
        ('!= 518', '!= 519'),
        ('kreeg 518', 'kreeg 519'),
        ('498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509', '498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510'),
    ],
)

build(
    'create-five-hundred-thirty-three-bootstrap.py',
    'create-five-hundred-thirty-four-bootstrap.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('all_cases[:518]', 'all_cases[:519]'),
        ('{UNKNOWN, TYPO}][:518]', '{UNKNOWN, TYPO}][:519]'),
        ('!= 518', '!= 519'),
        ('kreeg 518', 'kreeg 519'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506'),
    ],
)

build(
    'create-five-hundred-thirty-three-minimal.py',
    'create-five-hundred-thirty-four-minimal.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('!= 518', '!= 519'),
        ('kreeg 518', 'kreeg 519'),
        (' 459)', ' 460)'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506'),
    ],
)

build(
    'make-five-hundred-thirty-three.py',
    'make-five-hundred-thirty-four.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('all_cases[:518]', 'all_cases[:519]'),
        ('{UNKNOWN, TYPO}][:518]', '{UNKNOWN, TYPO}][:519]'),
        ('!= 518', '!= 519'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446'),
    ],
)

build(
    'create-five-hundred-thirty-three-files.py',
    'create-five-hundred-thirty-four-files.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('all_cases[:518]', 'all_cases[:519]'),
        ('{UNKNOWN, TYPO}][:518]', '{UNKNOWN, TYPO}][:519]'),
        ('!= 518', '!= 519'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446'),
    ],
)

build(
    'create-five-hundred-thirty-three.py',
    'create-five-hundred-thirty-four.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('all_cases[:518]', 'all_cases[:519]'),
        ('{UNKNOWN, TYPO}][:518]', '{UNKNOWN, TYPO}][:519]'),
        ('!= 518', '!= 519'),
        ('437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448', '437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-three.py',
    'generate-validate-five-hundred-thirty-four.py',
    [
        ('five-hundred-thirty-three', 'five-hundred-thirty-four'),
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('all_cases[:518]', 'all_cases[:519]'),
        ('{UNKNOWN, TYPO}][:518]', '{UNKNOWN, TYPO}][:519]'),
        ('!= 518', '!= 519'),
        ('434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445', '434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446'),
    ],
)

build(
    'validate-five-hundred-thirty-three-valid-list-cases.py',
    'validate-five-hundred-thirty-four-valid-list-cases.py',
    [
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508'),
        ('all_cases[:518]', 'all_cases[:519]'),
        ('len(valid_cases) != 518', 'len(valid_cases) != 519'),
    ],
)

build(
    'validate-five-hundred-thirty-three-valid-mixed.py',
    'validate-five-hundred-thirty-four-valid-mixed.py',
    [
        ('vijfhonderddrieëndertig', 'vijfhonderdvierendertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508'),
        ('][:518]', '][:519]'),
        ('len(valid_cases) != 518', 'len(valid_cases) != 519'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-three.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-three', 'five-hundred-thirty-four')
(ROOT / 'verify-five-hundred-thirty-four.py').write_text(verify_text)
print('verify-five-hundred-thirty-four.py')
