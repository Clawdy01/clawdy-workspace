#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')


def run(*args):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'failed: {args}')
    return proc.stdout.strip()


def readiness_summary():
    output = run('python3', 'scripts/git-publish-readiness.py', '--json')
    return json.loads(output)


def main():
    parser = argparse.ArgumentParser(description='Concreet plan voor eerste private GitHub push')
    parser.add_argument('--repo', help='github repo slug, bv. clawdy/clawdy-private')
    parser.add_argument('--branch', default='main', help='gewenste standaardbranch voor eerste push')
    parser.add_argument('--protocol', choices=['ssh', 'https'], default='ssh', help='remote protocol voor origin (default: ssh)')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    current_branch = run('git', 'rev-parse', '--abbrev-ref', 'HEAD')
    remotes = run('git', 'remote', '-v').splitlines()
    repo_slug = args.repo or '<owner>/<repo>'
    branch = args.branch
    readiness = readiness_summary()
    remote_url = (
        f'git@github.com:{repo_slug}.git'
        if args.protocol == 'ssh'
        else f'https://github.com/{repo_slug}.git'
    )

    commands = [
        'python3 scripts/git-publish-readiness.py',
    ]
    if readiness.get('untrack_command'):
        commands.append(readiness['untrack_command'])
    if current_branch != branch:
        commands.append(f'git branch -M {branch}')
    if not readiness.get('has_origin'):
        commands.append(f'git remote add origin {remote_url}')
    commands.extend([
        'git status --short --branch',
        f'git push -u origin {branch}',
    ])

    summary = {
        'current_branch': current_branch,
        'target_branch': branch,
        'has_remote': bool(remotes),
        'has_origin': readiness.get('has_origin', False),
        'repo_slug': repo_slug,
        'protocol': args.protocol,
        'remote_url': remote_url,
        'publish_blockers': readiness.get('publish_blockers', []),
        'active_risky_count': readiness.get('active_risky_count', 0),
        'resolved_sensitive_count': readiness.get('resolved_sensitive_count', 0),
        'publish_candidate_count': readiness.get('publish_candidate_count', 0),
        'tracked_risky_paths': readiness.get('tracked_risky_paths', []),
        'untrack_command': readiness.get('untrack_command'),
        'commands': commands,
        'next_hint': readiness.get('next_hint') or 'bereid eerst de private push veilig voor',
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print('Git first push plan')
        print(f"- huidige branch: {current_branch}")
        print(f"- doelbranch: {branch}")
        print(f"- remote aanwezig: {'ja' if summary['has_remote'] else 'nee'}")
        print(f"- origin aanwezig: {'ja' if summary['has_origin'] else 'nee'}")
        if summary['publish_blockers']:
            print(f"- blockers: {', '.join(summary['publish_blockers'])}")
        print(f"- actieve risicopaden: {summary['active_risky_count']}")
        print(f"- publish-kandidaten: {summary['publish_candidate_count']}")
        if summary['resolved_sensitive_count']:
            print(f"- al veilig uitgefaseerd uit tracking: {summary['resolved_sensitive_count']}")
        if summary['tracked_risky_paths']:
            print(f"- tracked risky: {', '.join(summary['tracked_risky_paths'])}")
        if summary['untrack_command']:
            print(f"- untrack: {summary['untrack_command']}")
        print(f"- repo: {repo_slug}")
        print(f"- protocol: {summary['protocol']}")
        print(f"- remote url: {summary['remote_url']}")
        print('- commando’s:')
        for cmd in commands:
            print(f'  - {cmd}')
        print(f"- next: {summary['next_hint']}")


if __name__ == '__main__':
    main()
