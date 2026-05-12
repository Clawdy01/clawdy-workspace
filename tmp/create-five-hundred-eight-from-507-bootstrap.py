#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('gen-five-hundred-seven-from-506-bootstrap.py', 'gen-five-hundred-eight-from-507-bootstrap.py'),
    ('create-five-hundred-seven-from-506-bootstrap.py', 'create-five-hundred-eight-from-507-bootstrap.py'),
]
for src_name, dst_name in repls:
    text = (root / src_name).read_text()
    text = text.replace('gen-five-hundred-seven-from-506-bootstrap.py', 'TMP_GEN_SRC')
    text = text.replace('create-five-hundred-seven-from-506-bootstrap.py', 'TMP_CREATE_SRC')
    text = text.replace('gen-five-hundred-eight-from-507-bootstrap.py', 'TMP_GEN_DST')
    text = text.replace('create-five-hundred-eight-from-507-bootstrap.py', 'TMP_CREATE_DST')
    text = text.replace('five-hundred-five', 'TMP_OLD')
    text = text.replace('five-hundred-seven', 'TMP_NEW')
    text = text.replace('vijfhonderdvijf', 'TMP_OLD_NL')
    text = text.replace('vijfhonderdzeven', 'TMP_NEW_NL')
    text = text.replace('TMP_OLD', 'five-hundred-seven')
    text = text.replace('TMP_NEW', 'five-hundred-eight')
    text = text.replace('TMP_OLD_NL', 'vijfhonderdzeven')
    text = text.replace('TMP_NEW_NL', 'vijfhonderdacht')
    text = text.replace('from-506', 'from-507')
    text = text.replace('from-505', 'from-506')
    text = text.replace('TMP_GEN_SRC', 'gen-five-hundred-seven-from-506-bootstrap.py')
    text = text.replace('TMP_CREATE_SRC', 'create-five-hundred-seven-from-506-bootstrap.py')
    text = text.replace('TMP_GEN_DST', 'gen-five-hundred-eight-from-507-bootstrap.py')
    text = text.replace('TMP_CREATE_DST', 'create-five-hundred-eight-from-507-bootstrap.py')
    (root / dst_name).write_text(text)
    print(dst_name)
