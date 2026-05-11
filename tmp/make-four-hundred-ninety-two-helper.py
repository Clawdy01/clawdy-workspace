#!/usr/bin/env python3
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-ninety-one-helper.py'
dst = root / 'create-four-hundred-ninety-two-helper.py'
text = src.read_text()
text = text.replace('four-hundred-ninety', '__SRC_SLUG__')
text = text.replace('four-hundred-ninety-one', '__DST_SLUG__')
text = text.replace('vierhonderdnegentig', '__SRC_DUTCH__')
text = text.replace('vierhonderdeenennegentig', '__DST_DUTCH__')
text = re.sub(r'\d+', lambda m: str(int(m.group()) + 1), text)
text = text.replace('__SRC_SLUG__', 'four-hundred-ninety-one')
text = text.replace('__DST_SLUG__', 'four-hundred-ninety-two')
text = text.replace('__SRC_DUTCH__', 'vierhonderdeenennegentig')
text = text.replace('__DST_DUTCH__', 'vierhonderdtweeënnegentig')
dst.write_text(text)
print(dst)
