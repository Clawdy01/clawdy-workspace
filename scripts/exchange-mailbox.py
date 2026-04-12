#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
TOOL = ROOT / 'scripts' / 'exchange-ews-tool.py'


def run_json(args):
    cmd = ['python3', str(TOOL), '--inbox', '--json'] + args
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=90)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or 'exchange-ews-tool failed')
    return json.loads(proc.stdout)


def render(items):
    lines = []
    for item in items:
        sender = item.get('from_name') or item.get('from_email') or 'onbekend'
        unread = 'unread' if not item.get('is_read') else 'read'
        preview = (item.get('preview') or '').strip()
        if len(preview) > 120:
            preview = preview[:117] + '...'
        line = f"- {sender} — {item.get('subject') or '(geen onderwerp)'} [{unread}]"
        if item.get('received'):
            line += f" {item['received']}"
        if preview:
            line += f"\n  {preview}"
        lines.append(line)
    return '\n'.join(lines) if lines else 'Geen resultaten.'


def main():
    parser = argparse.ArgumentParser(description='Praktische Exchange mailbox helper')
    parser.add_argument('--latest', action='store_true')
    parser.add_argument('--unread', action='store_true')
    parser.add_argument('--search')
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    tool_args = ['--limit', str(max(1, min(args.limit, 50)))]
    if args.unread:
        tool_args.append('--unread-only')
    if args.search:
        tool_args += ['--search', args.search]
    payload = run_json(tool_args)
    items = payload.get('inbox') or []

    if args.latest and len(items) > 1:
        items = items[:1]

    if args.json:
        print(json.dumps({'inbox': items}, ensure_ascii=False, indent=2))
    else:
        print(render(items))


if __name__ == '__main__':
    main()
