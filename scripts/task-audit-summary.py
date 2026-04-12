#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')


def run_status():
    proc = subprocess.run(
        ['openclaw', 'status', '--json'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'openclaw status failed: {proc.returncode}')
    return json.loads(proc.stdout)


def summarize(data):
    tasks = data.get('tasks') or {}
    audit = data.get('taskAudit') or {}
    by_status = tasks.get('byStatus') or {}
    by_code = audit.get('byCode') or {}
    return {
        'active': tasks.get('active', 0),
        'failures': tasks.get('failures', 0),
        'lost': by_status.get('lost', 0),
        'warnings': audit.get('warnings', 0),
        'errors': audit.get('errors', 0),
        'timestamp_warns': by_code.get('inconsistent_timestamps', 0),
        'lost_audit': by_code.get('lost', 0),
    }


def render(summary):
    lines = ['Task audit']
    lines.append(f"- actief: {summary['active']}")
    lines.append(f"- failures: {summary['failures']}")
    lines.append(f"- lost: {summary['lost']}")
    lines.append(f"- audit: {summary['errors']} errors, {summary['warnings']} warns")
    lines.append(f"- timestamp warns: {summary['timestamp_warns']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte task/audit samenvatting')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    summary = summarize(run_status())
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render(summary))


if __name__ == '__main__':
    main()
