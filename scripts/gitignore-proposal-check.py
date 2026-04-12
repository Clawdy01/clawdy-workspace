#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
PROPOSAL = ROOT / 'research' / 'github-private-gitignore-proposal.txt'


def load_patterns():
    patterns = []
    for line in PROPOSAL.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        patterns.append(line)
    return patterns


def all_paths(limit=400):
    paths = []
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT).as_posix()
        if rel == '.git' or rel.startswith('.git/'):
            continue
        paths.append(rel + ('/' if path.is_dir() else ''))
        if len(paths) >= limit:
            break
    return sorted(paths)


def matches(pattern, rel):
    rel_clean = rel.rstrip('/')
    if '*' in pattern:
        pattern_clean = pattern.rstrip('/')
        if Path(rel_clean).match(pattern_clean):
            return True
        if pattern.endswith('/'):
            prefix = pattern_clean.split('*', 1)[0]
            return rel_clean.startswith(prefix)
        return False
    if pattern.endswith('/'):
        base = pattern.rstrip('/')
        return rel == base or rel.startswith(pattern)
    return rel == pattern or rel.startswith(pattern + '/')


def main():
    patterns = load_patterns()
    paths = all_paths()
    matched = []
    unmatched = []
    for rel in paths:
        hit = next((p for p in patterns if matches(p, rel)), None)
        if hit:
            matched.append({'path': rel, 'pattern': hit})
        else:
            unmatched.append(rel)

    summary = {
        'pattern_count': len(patterns),
        'scanned_count': len(paths),
        'matched_count': len(matched),
        'unmatched_count': len(unmatched),
        'matched_preview': matched[:40],
        'unmatched_preview': unmatched[:40],
        'next_hint': 'pas hierna pas een echte .gitignore toe, nadat je de unmatched inhoud nog even beoordeelt',
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
