#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('gen-five-hundred-five-from-504-bootstrap.py', 'gen-five-hundred-six-from-505-bootstrap.py'),
    ('create-five-hundred-five-from-504.py', 'create-five-hundred-six-from-505.py'),
]
for src_name, dst_name in repls:
    text = (root / src_name).read_text()
    text = text.replace('five-hundred-five', 'TMP_FIVE_HUNDRED_FIVE')
    text = text.replace('five-hundred-six', 'TMP_FIVE_HUNDRED_SIX')
    text = text.replace('five-hundred-four', 'five-hundred-five')
    text = text.replace('five-hundred-five', 'five-hundred-six')
    text = text.replace('TMP_FIVE_HUNDRED_FIVE', 'five-hundred-five')
    text = text.replace('TMP_FIVE_HUNDRED_SIX', 'five-hundred-six')
    text = text.replace('vijfhonderdvijf', 'TMP_VIJFHONDERDVIJF')
    text = text.replace('vijfhonderdzes', 'TMP_VIJFHONDERDZES')
    text = text.replace('vijfhonderdvier', 'vijfhonderdvijf')
    text = text.replace('vijfhonderdvijf', 'vijfhonderdzes')
    text = text.replace('TMP_VIJFHONDERDVIJF', 'vijfhonderdvijf')
    text = text.replace('TMP_VIJFHONDERDZES', 'vijfhonderdzes')
    text = text.replace('from-504', 'from-505')
    text = text.replace('from-503', 'from-504')
    (root / dst_name).write_text(text)
    print(dst_name)
