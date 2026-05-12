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
    'create-five-hundred-thirty-four-assets.py',
    'create-five-hundred-thirty-five-assets.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('[:519]', '[:520]'),
        ('!= 519', '!= 520'),
        ('kreeg 519', 'kreeg 520'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510]', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]'),
    ],
)

build(
    'create-five-hundred-thirty-four-bootstrap.py',
    'create-five-hundred-thirty-five-bootstrap.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('all_cases[:519]', 'all_cases[:520]'),
        ('{UNKNOWN, TYPO}][:519]', '{UNKNOWN, TYPO}][:520]'),
        ('!= 519', '!= 520'),
        ('kreeg 519', 'kreeg 520'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506]', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507]'),
    ],
)

build(
    'create-five-hundred-thirty-four-minimal.py',
    'create-five-hundred-thirty-five-minimal.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('!= 519', '!= 520'),
        ('kreeg 519', 'kreeg 520'),
        (' 460)', ' 461)'),
        ('494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506]', '494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507]'),
    ],
)

build(
    'make-five-hundred-thirty-four.py',
    'make-five-hundred-thirty-five.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('all_cases[:519]', 'all_cases[:520]'),
        ('{UNKNOWN, TYPO}][:519]', '{UNKNOWN, TYPO}][:520]'),
        ('!= 519', '!= 520'),
        ('442, 443, 444, 445, 446]', '442, 443, 444, 445, 446, 447]'),
    ],
)

build(
    'create-five-hundred-thirty-four-files.py',
    'create-five-hundred-thirty-five-files.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('all_cases[:519]', 'all_cases[:520]'),
        ('{UNKNOWN, TYPO}][:519]', '{UNKNOWN, TYPO}][:520]'),
        ('!= 519', '!= 520'),
        ('442, 443, 444, 445, 446]', '442, 443, 444, 445, 446, 447]'),
    ],
)

build(
    'create-five-hundred-thirty-four.py',
    'create-five-hundred-thirty-five.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('all_cases[:519]', 'all_cases[:520]'),
        ('{UNKNOWN, TYPO}][:519]', '{UNKNOWN, TYPO}][:520]'),
        ('!= 519', '!= 520'),
        ('447, 448, 449]', '447, 448, 449, 450]'),
    ],
)

build(
    'generate-validate-five-hundred-thirty-four.py',
    'generate-validate-five-hundred-thirty-five.py',
    [
        ('five-hundred-thirty-four', 'five-hundred-thirty-five'),
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('all_cases[:519]', 'all_cases[:520]'),
        ('{UNKNOWN, TYPO}][:519]', '{UNKNOWN, TYPO}][:520]'),
        ('!= 519', '!= 520'),
        ('442, 443, 444, 445, 446]', '442, 443, 444, 445, 446, 447]'),
    ],
)

build(
    'validate-five-hundred-thirty-four-valid-list-cases.py',
    'validate-five-hundred-thirty-five-valid-list-cases.py',
    [
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509'),
        ('all_cases[:519]', 'all_cases[:520]'),
        ('len(valid_cases) != 519', 'len(valid_cases) != 520'),
    ],
)

build(
    'validate-five-hundred-thirty-four-valid-mixed.py',
    'validate-five-hundred-thirty-five-valid-mixed.py',
    [
        ('vijfhonderdvierendertig', 'vijfhonderdvijfendertig'),
        ('497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508', '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509'),
        ('][:519]', '][:520]'),
        ('len(valid_cases) != 519', 'len(valid_cases) != 520'),
    ],
)

verify_src = (ROOT / 'verify-five-hundred-thirty-four.py').read_text()
verify_text = verify_src.replace('five-hundred-thirty-four', 'five-hundred-thirty-five')
(ROOT / 'verify-five-hundred-thirty-five.py').write_text(verify_text)
print('verify-five-hundred-thirty-five.py')
