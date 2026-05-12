#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-five-hundred-three-from-502.py'
dst = root / 'create-five-hundred-four-from-503.py'
text = src.read_text()
repls = [
    ('five-hundred-two', '__OLD__'),
    ('five-hundred-three', '__NEW__'),
    ('vijfhonderdtwee', '__OLD_NL__'),
    ('vijfhonderddrie', '__NEW_NL__'),
]
for old, new in repls:
    text = text.replace(old, new)
text = text.replace('__OLD__', 'five-hundred-three')
text = text.replace('__NEW__', 'five-hundred-four')
text = text.replace('__OLD_NL__', 'vijfhonderddrie')
text = text.replace('__NEW_NL__', 'vijfhonderdvier')


def bump_nums_in_quoted(match):
    s = match.group(0)

    def bump_num(m):
        return str(int(m.group(0)) + 1)

    return re.sub(r'\d+', bump_num, s)


text = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", bump_nums_in_quoted, text)
dst.write_text(text)
print(dst)
