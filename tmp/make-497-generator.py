#!/usr/bin/env python3
from pathlib import Path
import re

src = Path('/home/clawdy/.openclaw/workspace/tmp/create-four-hundred-ninety-six-from-495.py')
dst = Path('/home/clawdy/.openclaw/workspace/tmp/create-four-hundred-ninety-seven-from-496.py')
text = src.read_text()
subs = [
    ('four-hundred-ninety-five', '__PREV__'),
    ('four-hundred-ninety-six', '__CURR__'),
    ('vierhonderdvijfennegentig', '__PREV_NL__'),
    ('vierhonderdzesennegentig', '__CURR_NL__'),
]
for old, new in subs:
    text = text.replace(old, new)
text = text.replace('__PREV__', 'four-hundred-ninety-six')
text = text.replace('__CURR__', 'four-hundred-ninety-seven')
text = text.replace('__PREV_NL__', 'vierhonderdzesennegentig')
text = text.replace('__CURR_NL__', 'vierhonderdzevenennegentig')
text = re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'", lambda m: "'" + re.sub(r'\d+', lambda n: str(int(n.group()) + 1), m.group(1)) + "'", text)
dst.write_text(text)
print(dst)
