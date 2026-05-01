#!/usr/bin/env python3
import py_compile
from pathlib import Path

path = Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-regression-check.py')
py_compile.compile(str(path), doraise=True)
print('ok')
