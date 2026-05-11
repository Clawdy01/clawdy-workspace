#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-ninety-three-helper.py'
dst = root / 'create-four-hundred-ninety-four-helper.py'
text = src.read_text()
text = text.replace('four-hundred-ninety-three', '__SRC_SLUG__')
text = text.replace('four-hundred-ninety-four', '__DST_SLUG__')
text = text.replace('vierhonderddrieënnegentig', '__SRC_DUTCH__')
text = text.replace('vierhonderdvierennegentig', '__DST_DUTCH__')
text = re.sub(r'\d+', lambda m: str(int(m.group()) + 1), text)
text = text.replace('__SRC_SLUG__', 'four-hundred-ninety-three')
text = text.replace('__DST_SLUG__', 'four-hundred-ninety-four')
text = text.replace('__SRC_DUTCH__', 'vierhonderddrieënnegentig')
text = text.replace('__DST_DUTCH__', 'vierhonderdvierennegentig')
dst.write_text(text)
print(dst)
