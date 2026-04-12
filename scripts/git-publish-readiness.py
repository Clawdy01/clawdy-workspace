#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
RISKY_PREFIXES = [
    '.openclaw/',
    'memory/',
    '.venv-',
    '.venv/',
    'state/',
    'MEMORY.md',
    'HEARTBEAT.md',
    'USER.md',
    'TOOLS.md',
]


def run(*args):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'failed: {args}')
    return proc.stdout


def git_lines(*args):
    return [line for line in run('git', *args).splitlines() if line.strip()]


def git_status_entries():
    out = subprocess.run(
        ['git', 'status', '--porcelain=v1', '-z'],
        cwd=ROOT,
        capture_output=True,
        text=False,
        check=False,
    )
    if out.returncode != 0:
        raise SystemExit((out.stderr or out.stdout or b'').decode(errors='replace').strip() or 'git status failed')
    raw = out.stdout.decode(errors='replace').split('\x00')
    entries = []
    i = 0
    while i < len(raw):
        item = raw[i]
        i += 1
        if not item:
            continue
        code = item[:2]
        path = item[3:]
        original_path = None
        if code and code[0] in {'R', 'C'} and i < len(raw):
            original_path = path
            path = raw[i]
            i += 1
        entries.append({'code': code, 'path': path, 'original_path': original_path})
    return entries


def classify_path(path):
    for prefix in RISKY_PREFIXES:
        if prefix.endswith('/'):
            base = prefix.rstrip('/')
            if path == base or path.startswith(prefix):
                return base
        elif path == prefix or path.startswith(prefix + '/'):
            return prefix
    return None


def load_gitignore_patterns():
    gitignore = ROOT / '.gitignore'
    if not gitignore.exists():
        return []
    patterns = []
    for line in gitignore.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        patterns.append(line)
    return patterns


def path_matches_pattern(path, pattern):
    path_clean = path.rstrip('/')
    pattern_clean = pattern.rstrip('/')
    if '*' in pattern:
        if Path(path_clean).match(pattern_clean):
            return True
        if pattern.endswith('/'):
            prefix = pattern_clean.split('*', 1)[0]
            return path_clean.startswith(prefix)
        return False
    if pattern.endswith('/'):
        return path_clean == pattern_clean or path.startswith(pattern)
    return path_clean == pattern_clean or path_clean.startswith(pattern_clean + '/')


def build_summary():
    branch = run('git', 'rev-parse', '--abbrev-ref', 'HEAD').strip()
    remotes = git_lines('remote', '-v')
    remote_names = git_lines('remote')
    entries = git_status_entries()
    gitignore_patterns = load_gitignore_patterns()

    tracked_changed = []
    untracked = []
    risks = []
    tracked_risks = []
    uncovered_risks = []

    for entry in entries:
        code = entry['code']
        path = entry['path']
        if code == '??':
            untracked.append(path)
            risk = classify_path(path)
            if risk:
                item = {'kind': 'untracked', 'path': path, 'risk': risk}
                risks.append(item)
                uncovered = not any(path_matches_pattern(path, pattern) for pattern in gitignore_patterns)
                if uncovered:
                    uncovered_risks.append(item)
            continue

        tracked_changed.append({'code': code, 'path': path})
        risk = classify_path(path)
        if risk:
            item = {'kind': 'tracked', 'path': path, 'risk': risk}
            risks.append(item)
            tracked_risks.append(path)

    publish_blockers = []
    if tracked_risks:
        publish_blockers.append('tracked_sensitive_paths')
    if uncovered_risks:
        publish_blockers.append('uncovered_untracked_sensitive_paths')
    if not gitignore_patterns:
        publish_blockers.append('missing_gitignore')
    if not remotes:
        publish_blockers.append('missing_remote')
    if 'origin' not in remote_names:
        publish_blockers.append('missing_origin')

    next_hint = 'repo oogt klaar voor private remote + eerste push'
    if tracked_risks:
        next_hint = 'haal tracked gevoelige paden eerst uit git-tracking en commit daarna pas richting private remote'
    elif uncovered_risks or not gitignore_patterns:
        next_hint = 'werk eerst een publish-veilige .gitignore af voordat je private repo + eerste push doet'
    elif not remotes:
        next_hint = 'publish-selectie oogt beter; volgende stap is private remote toevoegen en eerste push voorbereiden'

    return {
        'branch': branch,
        'remote_count': len(remotes),
        'has_remote': bool(remotes),
        'has_origin': 'origin' in remote_names,
        'gitignore_present': bool(gitignore_patterns),
        'gitignore_pattern_count': len(gitignore_patterns),
        'publish_blockers': publish_blockers,
        'tracked_changed_count': len(tracked_changed),
        'untracked_count': len(untracked),
        'risky_count': len(risks),
        'tracked_risky_count': len(tracked_risks),
        'uncovered_risky_untracked_count': len(uncovered_risks),
        'tracked_changed': tracked_changed[:20],
        'untracked': untracked[:20],
        'risks': risks[:30],
        'tracked_risky_paths': tracked_risks[:20],
        'uncovered_risky_untracked': uncovered_risks[:20],
        'untrack_command': f"git rm --cached -- {' '.join(tracked_risks)}" if tracked_risks else None,
        'next_hint': next_hint,
    }


def render_text(summary):
    lines = ['Git publish readiness']
    lines.append(f"- branch: {summary['branch']}")
    lines.append(f"- remote: {'ja' if summary['has_remote'] else 'nee'} ({summary['remote_count']})")
    lines.append(f"- origin: {'ja' if summary['has_origin'] else 'nee'}")
    lines.append(f"- .gitignore: {'ja' if summary['gitignore_present'] else 'nee'} ({summary['gitignore_pattern_count']} patronen)")
    if summary.get('publish_blockers'):
        lines.append(f"- blockers: {', '.join(summary['publish_blockers'])}")
    lines.append(f"- tracked gewijzigd: {summary['tracked_changed_count']}, untracked: {summary['untracked_count']}")
    lines.append(f"- risicopaden: {summary['risky_count']}")
    lines.append(f"- tracked gevoelig: {summary['tracked_risky_count']}, ongedekt untracked gevoelig: {summary['uncovered_risky_untracked_count']}")
    if summary['risks']:
        preview = ', '.join(item['path'] for item in summary['risks'][:6])
        if len(summary['risks']) > 6:
            preview += f" (+{len(summary['risks']) - 6})"
        lines.append(f"- risico-preview: {preview}")
    if summary['untrack_command']:
        lines.append(f"- untrack: {summary['untrack_command']}")
    lines.append(f"- next: {summary['next_hint']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Snelle readiness-check voor eerste private GitHub push')
    parser.add_argument('--json', action='store_true', help='toon machineleesbare JSON-output')
    args = parser.parse_args()

    summary = build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
