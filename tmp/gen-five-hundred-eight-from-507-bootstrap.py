#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-five-hundred-seven-from-506.py'
dst = root / 'create-five-hundred-eight-from-507.py'
text = src.read_text()
repls = [
    ('five-hundred-five', 'five-hundred-seven'),
    ('five-hundred-seven', 'five-hundred-eight'),
    ('vijfhonderdvijf', 'vijfhonderdzeven'),
    ('vijfhonderdzeven', 'vijfhonderdacht'),
]
for old, new in repls:
    text = text.replace(old, new)
text = text.replace('five-hundred-seven', 'five-hundred-seven')
text = text.replace('five-hundred-eight', 'five-hundred-eight')
text = text.replace('vijfhonderdzeven', 'vijfhonderdzeven')
text = text.replace('vijfhonderdacht', 'vijfhonderdacht')


def bump_nums_in_quoted(match):
    s = match.group(0)

    def bump_num(m):
        return str(int(m.group(0)) + 1)

    return re.sub(r'\d+', bump_num, s)


text = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", bump_nums_in_quoted, text)
dst.write_text(text)
print(dst)
