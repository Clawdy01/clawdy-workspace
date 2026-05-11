#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-ninety-two-helper.py'
dst = root / 'create-four-hundred-ninety-three-helper.py'
text = src.read_text()
text = text.replace('four-hundred-ninety-two', '__SRC_SLUG__')
text = text.replace('four-hundred-ninety-three', '__DST_SLUG__')
text = text.replace('vierhonderdtweeënnegentig', '__SRC_DUTCH__')
text = text.replace('vierhonderddrieënnegentig', '__DST_DUTCH__')
text = re.sub(r'\d+', lambda m: str(int(m.group()) + 1), text)
text = text.replace('__SRC_SLUG__', 'four-hundred-ninety-two')
text = text.replace('__DST_SLUG__', 'four-hundred-ninety-three')
text = text.replace('__SRC_DUTCH__', 'vierhonderdtweeënnegentig')
text = text.replace('__DST_DUTCH__', 'vierhonderddrieënnegentig')
dst.write_text(text)
print(dst)
