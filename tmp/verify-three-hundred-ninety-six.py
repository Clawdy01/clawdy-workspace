#!/usr/bin/env python3
import py_compile
import subprocess
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
files = [
    root / 'tmp' / 'make-three-hundred-ninety-six.py',
    root / 'tmp' / 'create-three-hundred-ninety-six-files.py',
    root / 'tmp' / 'create-three-hundred-ninety-six.py',
    root / 'tmp' / 'generate-validate-three-hundred-ninety-six.py',
    root / 'tmp' / 'validate-three-hundred-ninety-six-valid-list-cases.py',
    root / 'tmp' / 'validate-three-hundred-ninety-six-valid-mixed.py',
]
for path in files:
    py_compile.compile(str(path), doraise=True)
for script in [
    'tmp/validate-three-hundred-ninety-six-valid-list-cases.py',
    'tmp/validate-three-hundred-ninety-six-valid-mixed.py',
]:
    proc = subprocess.run(['python3', script], cwd=root, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stdout + proc.stderr)
print('OK')
