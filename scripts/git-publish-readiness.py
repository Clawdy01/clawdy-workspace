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


def upstream_status(branch):
    proc = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return {
            'has_upstream': False,
            'upstream': None,
            'ahead': None,
            'behind': None,
        }
    upstream = proc.stdout.strip()
    counts = run('git', 'rev-list', '--left-right', '--count', f'{branch}...{upstream}').strip().split()
    ahead = int(counts[0]) if len(counts) > 0 else 0
    behind = int(counts[1]) if len(counts) > 1 else 0
    return {
        'has_upstream': True,
        'upstream': upstream,
        'ahead': ahead,
        'behind': behind,
    }


def build_summary():
    branch = run('git', 'rev-parse', '--abbrev-ref', 'HEAD').strip()
    remotes = git_lines('remote', '-v')
    remote_names = git_lines('remote')
    entries = git_status_entries()
    gitignore_patterns = load_gitignore_patterns()
    upstream = upstream_status(branch)

    tracked_changed = []
    untracked = []
    risks = []
    tracked_risks = []
    uncovered_risks = []
    resolved_sensitive = []
    publish_candidates = []

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
            else:
                publish_candidates.append({'code': code, 'path': path})
            continue

        tracked_changed.append({'code': code, 'path': path})
        risk = classify_path(path)
        if not risk:
            publish_candidates.append({'code': code, 'path': path})
            continue

        is_staged_removal = code[0] == 'D'
        now_ignored = any(path_matches_pattern(path, pattern) for pattern in gitignore_patterns)
        item = {
            'kind': 'tracked',
            'path': path,
            'risk': risk,
            'staged_removal': is_staged_removal,
            'now_ignored': now_ignored,
        }
        risks.append(item)
        if is_staged_removal and now_ignored:
            resolved_sensitive.append(path)
        else:
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
    if not upstream['has_upstream']:
        publish_blockers.append('missing_upstream')

    next_hint = 'repo oogt klaar voor private remote + eerste push'
    if tracked_risks:
        next_hint = 'haal tracked gevoelige paden eerst uit git-tracking en commit daarna pas richting private remote'
    elif uncovered_risks or not gitignore_patterns:
        next_hint = 'werk eerst een publish-veilige .gitignore af voordat je private repo + eerste push doet'
    elif not remotes:
        next_hint = 'publish-selectie oogt beter; volgende stap is private remote toevoegen en eerste push voorbereiden'
    elif not upstream['has_upstream']:
        next_hint = 'origin bestaat al; volgende stap is branch koppelen met upstream via de eerste push'
    elif upstream['ahead']:
        next_hint = 'upstream bestaat; volgende stap is lokale commits pushen'

    active_risks = tracked_risks + [item['path'] for item in uncovered_risks]

    return {
        'branch': branch,
        'remote_count': len(remotes),
        'has_remote': bool(remotes),
        'has_origin': 'origin' in remote_names,
        'gitignore_present': bool(gitignore_patterns),
        'gitignore_pattern_count': len(gitignore_patterns),
        'publish_blockers': publish_blockers,
        'has_upstream': upstream['has_upstream'],
        'upstream': upstream['upstream'],
        'ahead_count': upstream['ahead'],
        'behind_count': upstream['behind'],
        'tracked_changed_count': len(tracked_changed),
        'untracked_count': len(untracked),
        'risky_count': len(risks),
        'active_risky_count': len(active_risks),
        'resolved_sensitive_count': len(resolved_sensitive),
        'publish_candidate_count': len(publish_candidates),
        'tracked_risky_count': len(tracked_risks),
        'uncovered_risky_untracked_count': len(uncovered_risks),
        'tracked_changed': tracked_changed[:20],
        'untracked': untracked[:20],
        'risks': risks[:30],
        'active_risky_paths': active_risks[:20],
        'resolved_sensitive_paths': resolved_sensitive[:20],
        'publish_candidates': publish_candidates[:20],
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
    lines.append(f"- upstream: {'ja' if summary['has_upstream'] else 'nee'}")
    if summary['upstream']:
        lines.append(f"- upstream ref: {summary['upstream']} (ahead {summary['ahead_count']}, behind {summary['behind_count']})")
    if summary.get('publish_blockers'):
        lines.append(f"- blockers: {', '.join(summary['publish_blockers'])}")
    lines.append(f"- tracked gewijzigd: {summary['tracked_changed_count']}, untracked: {summary['untracked_count']}")
    lines.append(f"- actieve risicopaden: {summary['active_risky_count']}")
    lines.append(f"- tracked gevoelig: {summary['tracked_risky_count']}, ongedekt untracked gevoelig: {summary['uncovered_risky_untracked_count']}")
    if summary['active_risky_paths']:
        preview = ', '.join(summary['active_risky_paths'][:6])
        if summary['active_risky_count'] > 6:
            preview += f" (+{summary['active_risky_count'] - 6})"
        lines.append(f"- actief risico-preview: {preview}")
    if summary['resolved_sensitive_count']:
        preview = ', '.join(summary['resolved_sensitive_paths'][:4])
        if summary['resolved_sensitive_count'] > 4:
            preview += f" (+{summary['resolved_sensitive_count'] - 4})"
        lines.append(f"- al veilig uitgefaseerd uit tracking: {preview}")
    lines.append(f"- publish-kandidaten: {summary['publish_candidate_count']}")
    if summary['publish_candidates']:
        preview = ', '.join(item['path'] for item in summary['publish_candidates'][:6])
        if summary['publish_candidate_count'] > 6:
            preview += f" (+{summary['publish_candidate_count'] - 6})"
        lines.append(f"- kandidaat-preview: {preview}")
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
