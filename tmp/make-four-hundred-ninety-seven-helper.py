#!/usr/bin/env python4
from pathlib import Path
import re

root = Path('/home/clawdy/.openclaw/workspace/tmp')
src = root / 'create-four-hundred-ninety-four-helper.py'
dst = root / 'create-four-hundred-ninety-seven-helper.py'
text = src.read_text()
text = text.replace('four-hundred-ninety-four', 'four-hundred-ninety-four')
text = text.replace('four-hundred-ninety-five', 'four-hundred-ninety-five')
text = text.replace('vierhonderdvierennegentig', 'vierhonderdvierennegentig')
text = text.replace('vierhonderdzevenennegentig', 'vierhonderdvijfennegentig')
text = re.sub(r'\d+', lambda m: str(int(m.group()) + 2), text)
text = text.replace('four-hundred-ninety-four', 'four-hundred-ninety-four')
text = text.replace('four-hundred-ninety-five', 'four-hundred-ninety-five')
text = text.replace('vierhonderdvierennegentig', 'vierhonderdvierennegentig')
text = text.replace('vierhonderdvijfennegentig', 'vierhonderdvijfennegentig')
dst.write_text(text)
print(dst)
