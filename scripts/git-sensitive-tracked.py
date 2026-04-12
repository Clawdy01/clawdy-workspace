#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
CANDIDATES = [
    'HEARTBEAT.md',
    'MEMORY.md',
    'TOOLS.md',
    'USER.md',
    'memory/',
]


def run(*args):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return ''
    return proc.stdout.strip()


def tracked_matches():
    tracked = set(run('git', 'ls-files').splitlines())
    matches = []
    for path in sorted(tracked):
        for candidate in CANDIDATES:
            if candidate.endswith('/'):
                if path.startswith(candidate):
                    matches.append(path)
                    break
            elif path == candidate:
                matches.append(path)
                break
    return matches


def build_summary():
    paths = tracked_matches()
    return {
        'tracked_sensitive_count': len(paths),
        'tracked_sensitive_paths': paths,
        'untrack_command': 'git rm --cached -- HEARTBEAT.md MEMORY.md TOOLS.md USER.md memory/2026-04-06.md',
        'next_hint': 'haal deze paden eerst uit git-tracking of maak een schone publish-branch voordat je de private remote toevoegt',
    }


def render_text(summary):
    lines = ['Git sensitive tracked']
    lines.append(f"- tracked sensitive: {summary['tracked_sensitive_count']}")
    if summary['tracked_sensitive_paths']:
        preview = ', '.join(summary['tracked_sensitive_paths'])
        lines.append(f"- paths: {preview}")
    lines.append(f"- untrack: {summary['untrack_command']}")
    lines.append(f"- next: {summary['next_hint']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Toon gevoelige paden die nog tracked zijn voor eerste private push')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    summary = build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
