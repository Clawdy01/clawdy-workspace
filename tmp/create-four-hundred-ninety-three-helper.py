#!/usr/bin/env python3
from pathlib import Path
import re

src = Path('/home/clawdy/.openclaw/workspace/tmp/create-four-hundred-ninety-two-helper.py').read_text()
first_line, body = src.splitlines(True)[0], ''.join(src.splitlines(True)[1:])
body = body.replace('four-hundred-ninety-one', '__SRC_SLUG__')
body = body.replace('four-hundred-ninety-two', '__DST_SLUG__')
body = body.replace('vierhonderdeenennegentig', '__SRC_DUTCH__')
body = body.replace('vierhonderdtweeënnegentig', '__DST_DUTCH__')
body = re.sub(r'\d+', lambda m: str(int(m.group()) + 1), body)
body = body.replace('__SRC_SLUG__', 'four-hundred-ninety-two')
body = body.replace('__DST_SLUG__', 'four-hundred-ninety-three')
body = body.replace('__SRC_DUTCH__', 'vierhonderdtweeënnegentig')
body = body.replace('__DST_DUTCH__', 'vierhonderddrieënnegentig')
exec(compile(first_line + body, '<generated-create-four-hundred-ninety-three-helper>', 'exec'))
