#!/usr/bin/env python3
import py_compile
import subprocess
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
files = [
    root / 'tmp' / 'make-five-hundred-fifteen.py',
    root / 'tmp' / 'create-five-hundred-fifteen-files.py',
    root / 'tmp' / 'create-five-hundred-fifteen.py',
    root / 'tmp' / 'generate-validate-five-hundred-fifteen.py',
    root / 'tmp' / 'validate-five-hundred-fifteen-valid-list-cases.py',
    root / 'tmp' / 'validate-five-hundred-fifteen-valid-mixed.py',
]
for path in files:
    py_compile.compile(str(path), doraise=True)
for script in [
    'tmp/validate-five-hundred-fifteen-valid-list-cases.py',
    'tmp/validate-five-hundred-fifteen-valid-mixed.py',
]:
    proc = subprocess.run(['python3', script], cwd=root, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stdout + proc.stderr)
print('OK')
