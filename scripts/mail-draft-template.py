#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) < 4:
    print('Usage: mail-draft-template.py <to> <subject> <goal>')
    sys.exit(2)

to, subject, goal = sys.argv[1], sys.argv[2], sys.argv[3]
out = {
    'to': to,
    'subject': subject,
    'goal': goal,
    'draft': f"Hoi,\n\n{goal}\n\nGroet,\nClawdy"
}
print(json.dumps(out, ensure_ascii=False, indent=2))
