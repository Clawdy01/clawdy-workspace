#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
proc = subprocess.run(
    ['python3', 'scripts/ai-briefing-status.py', '--json'],
    cwd=root,
    capture_output=True,
    text=True,
    check=False,
    timeout=120,
)
if proc.returncode != 0:
    raise SystemExit(proc.stderr or proc.stdout or f'failed: {proc.returncode}')
obj = json.loads(proc.stdout)
assert obj['ok'] is True
assert obj['payload_audit']['ok'] is True
print(obj['payload_audit']['message_sha256_short'])
print(obj['payload_audit']['text'])
print(obj['text'])
