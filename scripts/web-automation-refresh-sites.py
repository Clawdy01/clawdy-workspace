#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SITES = ROOT / 'scripts' / 'web-automation-sites.py'
DISPATCH = ROOT / 'scripts' / 'web-automation-dispatch.py'


def run_json(command):
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'command failed: {command}')
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'Invalid JSON from command: {exc}\n{proc.stdout}')


def build_command(site):
    refresh_command = (site.get('refresh_command') or '').strip()
    if refresh_command:
        return shlex.split(refresh_command)

    refresh_command = (site.get('recommended_command') or '').strip()
    if refresh_command:
        return shlex.split(refresh_command)

    route = (site.get('route') or '').strip()
    route_args = site.get('route_args') or []
    if route:
        return ['python3', str(DISPATCH), route, *[str(arg) for arg in route_args]]

    url = (site.get('url') or '').strip()
    slug = (site.get('slug') or '').strip()
    if not url:
        return None

    command = ['python3', str(DISPATCH), 'probe-page', url]
    probe_args = site.get('probe_args') or []
    if probe_args:
        command += [str(arg) for arg in probe_args]
    if slug:
        command += ['--slug', slug]
    return command


def refresh_probe(site, timeout_seconds=None):
    command = build_command(site)
    if not command:
        return {
            'ok': False,
            'command': None,
            'returncode': 1,
            'stdout': '',
            'stderr': 'geen refresh-commando of URL beschikbaar',
            'result': None,
            'timed_out': False,
        }
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = exc
        timed_out = True
    payload = None
    stdout = (getattr(proc, 'stdout', '') or '').strip()
    stderr = (getattr(proc, 'stderr', '') or '').strip()
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = {'raw_stdout': stdout}
    if timed_out:
        timeout_hint = f'timeout after {timeout_seconds}s' if timeout_seconds else 'timeout'
        stderr = f"{stderr}\n{timeout_hint}".strip()
    return {
        'ok': (not timed_out) and proc.returncode == 0,
        'command': ' '.join(command),
        'returncode': 124 if timed_out else proc.returncode,
        'stdout': stdout,
        'stderr': stderr,
        'result': payload,
        'timed_out': timed_out,
    }


def resolve_site_limit(max_sites=None, max_targets=None):
    limits = [value for value in (max_sites, max_targets) if value is not None]
    if not limits:
        return None
    return max(0, min(limits))


def build_refresh_plan(stale_after, include_all=False, slug_filter=None, adapter_filter=None, max_sites=None, max_targets=None, configured_only=False, include_terminal=False):
    command = ['python3', str(SITES), '--json', '--stale-after', str(stale_after)]
    for adapter in sorted(adapter_filter or []):
        command += ['--adapter', adapter]
    summary = run_json(command)
    candidates = summary.get('sites') or []
    skipped_terminal = []
    if configured_only:
        candidates = [site for site in candidates if site.get('configured')]
    if not include_all:
        candidates = [site for site in candidates if site.get('attention_needed', site.get('stale'))]
    if slug_filter:
        wanted = {item.strip() for item in slug_filter if item.strip()}
        candidates = [site for site in candidates if site.get('slug') in wanted]
    if not include_terminal:
        kept = []
        for site in candidates:
            if site.get('workflow_terminal'):
                skipped_terminal.append({
                    'slug': site.get('slug'),
                    'label': site.get('label'),
                    'url': site.get('url'),
                    'handoff_command': site.get('handoff_command') or site.get('recommended_command'),
                    'workflow_state': site.get('workflow_state'),
                    'workflow_note': site.get('workflow_note'),
                })
                continue
            kept.append(site)
        candidates = kept
    candidates.sort(key=lambda site: (not site.get('attention_needed', site.get('stale')), site.get('age_seconds') is None, -(site.get('age_seconds') or 0), site.get('slug') or ''))
    limit = resolve_site_limit(max_sites=max_sites, max_targets=max_targets)
    if limit is not None:
        candidates = candidates[:limit]
    return summary, candidates, skipped_terminal


def render_text(result):
    refreshed = result.get('refreshed') or []
    skipped_terminal = result.get('skipped_terminal') or []
    planned_only = bool(result.get('planned_only'))
    candidate_count = result.get('candidate_count', 0)
    if not refreshed and not skipped_terminal and candidate_count == 0:
        return 'Web automation refresh-sites: niets te verversen'

    if planned_only:
        lines = [
            f"Web automation refresh-sites plan: {candidate_count} kandidaat/kandidaten"
        ]
    else:
        lines = [
            f"Web automation refresh-sites: {result.get('refreshed_count', 0)} gedaan, {result.get('success_count', 0)} ok, {result.get('failure_count', 0)} mislukt"
        ]
    if skipped_terminal:
        lines.append(f"- manual-boundary overgeslagen: {len(skipped_terminal)}")
        for item in skipped_terminal[:5]:
            lines.append(f"  - {item.get('slug')}: {item.get('workflow_state') or 'terminal'}")
    entries = refreshed if not planned_only else (result.get('planned') or [])
    for item in entries:
        if planned_only:
            lines.append(
                f"- {item.get('slug')}: {item.get('age_human_before')}, url={item.get('url')}, cmd={item.get('command') or '-'}"
            )
            continue
        status = 'timeout' if item.get('timed_out') else ('ok' if item.get('ok') else 'fail')
        title = ((item.get('result') or {}).get('title') or item.get('title') or '-').strip()
        lines.append(
            f"- {item.get('slug')}: {status}, was {item.get('age_human_before')}, url={item.get('url')}, title={title}"
        )
        if item.get('stderr'):
            lines.append(f"  - stderr: {item['stderr'][:160]}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Refresh generieke web probe sites op basis van bestaande artifacts')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--all', action='store_true', help='refresh ook niet-stale sites')
    parser.add_argument('--configured-only', action='store_true', help='refresh alleen expliciet beheerde registry-sites')
    parser.add_argument('--slug', action='append', help='refresh alleen specifieke slug(s), herhaalbaar')
    parser.add_argument('--adapter', action='append', help='refresh alleen specifieke adapter(s), herhaalbaar')
    parser.add_argument('--max-sites', type=int, default=None, help='maximaal aantal sites om te refreshen')
    parser.add_argument('--max-targets', type=int, default=None, help='alias voor --max-sites, handig voor stack/autopilot flows')
    parser.add_argument('--stale-after', type=int, default=900, help='stale-drempel in seconden')
    parser.add_argument('--timeout', type=int, default=90, help='timeout per refresh-commando in seconden')
    parser.add_argument('--include-terminal', action='store_true', help='neem ook manual-boundary/terminal workflows mee in refreshes')
    parser.add_argument('--plan-only', action='store_true', help='toon alleen welke site-refreshes nu gepland zouden worden, zonder ze uit te voeren')
    args = parser.parse_args()

    summary, candidates, skipped_terminal = build_refresh_plan(
        stale_after=args.stale_after,
        include_all=args.all,
        slug_filter=args.slug,
        adapter_filter={str(item).strip().lower() for item in (args.adapter or []) if str(item).strip()},
        max_sites=args.max_sites,
        max_targets=args.max_targets,
        configured_only=args.configured_only,
        include_terminal=args.include_terminal,
    )

    planned = [
        {
            'slug': site.get('slug'),
            'url': site.get('url'),
            'label': site.get('label'),
            'adapter': site.get('adapter'),
            'stale_after_seconds': site.get('stale_after_seconds'),
            'age_seconds_before': site.get('age_seconds'),
            'age_human_before': site.get('age_human'),
            'title': site.get('title'),
            'command': ' '.join(build_command(site) or []),
        }
        for site in candidates
    ]

    refreshed = []
    if not args.plan_only:
        for site in candidates:
            probe = refresh_probe(site, timeout_seconds=args.timeout)
            refreshed.append({
                'slug': site.get('slug'),
                'url': site.get('url'),
                'label': site.get('label'),
                'adapter': site.get('adapter'),
                'stale_after_seconds': site.get('stale_after_seconds'),
                'age_seconds_before': site.get('age_seconds'),
                'age_human_before': site.get('age_human'),
                'title': site.get('title'),
                **probe,
            })

    result = {
        'stale_after_seconds': args.stale_after,
        'requested_all': args.all,
        'configured_only': args.configured_only,
        'include_terminal': args.include_terminal,
        'requested_slugs': args.slug or [],
        'requested_adapters': args.adapter or [],
        'requested_max_sites': args.max_sites,
        'requested_max_targets': args.max_targets,
        'planned_only': args.plan_only,
        'site_count_seen': summary.get('site_count', 0),
        'candidate_count': len(candidates),
        'planned': planned,
        'skipped_terminal_count': len(skipped_terminal),
        'skipped_terminal': skipped_terminal,
        'refreshed_count': len(refreshed),
        'success_count': sum(1 for item in refreshed if item.get('ok')),
        'failure_count': sum(1 for item in refreshed if not item.get('ok')),
        'timeout_seconds': args.timeout,
        'timed_out_count': sum(1 for item in refreshed if item.get('timed_out')),
        'refreshed': refreshed,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))


if __name__ == '__main__':
    main()
