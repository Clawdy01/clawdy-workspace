#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
src_slug = 'two-hundred-seventy-three'
dst_slug = 'two-hundred-seventy-four'
src_nl = 'tweehonderddrieenzeventig'
dst_nl = 'tweehonderdvierenzeventig'
src_count = 269
dst_count = 270
order_tail = f'{src_count - 2}, {src_count - 1}]'
new_order_tail = f'{src_count - 2}, {src_count - 1}, {dst_count - 1}]'

for name in (
    f'generate-validate-{src_slug}.py',
    f'validate-{src_slug}-valid-list-cases.py',
    f'validate-{src_slug}-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace(src_slug, dst_slug)
    text = src.read_text()
    text = text.replace(src_slug, dst_slug)
    text = text.replace(src_nl, dst_nl)
    text = text.replace(f'[:{src_count}]', f'[:{dst_count}]')
    text = text.replace(f'!= {src_count}', f'!= {dst_count}')
    text = text.replace(order_tail, new_order_tail)
    dst.write_text(text)
