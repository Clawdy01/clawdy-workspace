#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-five-hundred-six-from-505.py'
dst = root / 'create-five-hundred-seven-from-506.py'
text = src.read_text()
repls = [
    ('five-hundred-five', '__OLD__'),
    ('five-hundred-six', '__NEW__'),
    ('vijfhonderdvijf', '__OLD_NL__'),
    ('vijfhonderdzes', '__NEW_NL__'),
]
for old, new in repls:
    text = text.replace(old, new)
text = text.replace('__OLD__', 'five-hundred-six')
text = text.replace('__NEW__', 'five-hundred-seven')
text = text.replace('__OLD_NL__', 'vijfhonderdzes')
text = text.replace('__NEW_NL__', 'vijfhonderdzeven')


def bump_nums_in_quoted(match):
    s = match.group(0)

    def bump_num(m):
        return str(int(m.group(0)) + 1)

    return re.sub(r'\d+', bump_num, s)


text = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", bump_nums_in_quoted, text)
dst.write_text(text)
print(dst)
