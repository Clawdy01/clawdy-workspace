#!/usr/bin/env python3
import py_compile
import subprocess
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
files = [
    root / 'tmp' / 'make-four-hundred-seventy.py',
    root / 'tmp' / 'create-four-hundred-seventy-files.py',
    root / 'tmp' / 'create-four-hundred-seventy.py',
    root / 'tmp' / 'generate-validate-four-hundred-seventy.py',
    root / 'tmp' / 'validate-four-hundred-seventy-valid-list-cases.py',
    root / 'tmp' / 'validate-four-hundred-seventy-valid-mixed.py',
]
for path in files:
    py_compile.compile(str(path), doraise=True)
for script in [
    'tmp/validate-four-hundred-seventy-valid-list-cases.py',
    'tmp/validate-four-hundred-seventy-valid-mixed.py',
]:
    proc = subprocess.run(['python3', script], cwd=root, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stdout + proc.stderr)
print('OK')
