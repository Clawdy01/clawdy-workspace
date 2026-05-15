#!/usr/bin/env python3
import py_compile
import subprocess
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
files = [
    root / 'tmp' / 'make-six-hundred-thirty-six.py',
    root / 'tmp' / 'create-six-hundred-thirty-six-files.py',
    root / 'tmp' / 'create-six-hundred-thirty-six.py',
    root / 'tmp' / 'generate-validate-six-hundred-thirty-six.py',
    root / 'tmp' / 'validate-six-hundred-thirty-six-valid-list-cases.py',
    root / 'tmp' / 'validate-six-hundred-thirty-six-valid-mixed.py',
]
for path in files:
    py_compile.compile(str(path), doraise=True)
for script in [
    'tmp/validate-six-hundred-thirty-six-valid-list-cases.py',
    'tmp/validate-six-hundred-thirty-six-valid-mixed.py',
]:
    proc = subprocess.run(['python3', script], cwd=root, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stdout + proc.stderr)
print('OK')
