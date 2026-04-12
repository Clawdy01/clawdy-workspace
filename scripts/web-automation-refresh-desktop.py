#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
DESKTOP_STATUS = ROOT / 'scripts' / 'desktop-fallback-status.py'


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


def build_command(item, keep_screenshots=None):
    command = str(item.get('command') or '').strip()
    if not command:
        return None
    parts = shlex.split(command)
    effective_keep = keep_screenshots if keep_screenshots is not None else item.get('keep_screenshots')
    if effective_keep is not None:
        parts.extend(['--keep-screenshots', str(effective_keep)])
    return parts


def refresh_target(item, timeout_seconds=None, keep_screenshots=None):
    command = build_command(item, keep_screenshots=keep_screenshots)
    if not command:
        return {
            'ok': False,
            'command': None,
            'returncode': 1,
            'stdout': '',
            'stderr': 'geen desktop refresh-commando beschikbaar',
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
    stdout = (getattr(proc, 'stdout', '') or '').strip()
    stderr = (getattr(proc, 'stderr', '') or '').strip()
    payload = None
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


def build_refresh_plan(stale_after, include_all=False, slug_filter=None, adapter_filter=None, max_targets=None, configured_only=False, force=False):
    command = ['python3', str(DESKTOP_STATUS), '--json', '--stale-after', str(stale_after)]
    for adapter in sorted(adapter_filter or []):
        command.extend(['--adapter', adapter])
    summary = run_json(command)
    if configured_only:
        candidates = list(summary.get('configured_recommended_actions') or [])
    else:
        candidates = []
        seen = set()
        for item in summary.get('configured_recommended_actions') or []:
            key = (item.get('slug'), item.get('path'))
            if key not in seen:
                candidates.append(item)
                seen.add(key)
        if include_all and summary.get('recommended_command'):
            fallback = {
                'path': summary.get('default_outdir'),
                'slug': summary.get('default_configured_slug'),
                'command': summary.get('recommended_command'),
            }
            key = (fallback.get('slug'), fallback.get('path'))
            if key not in seen:
                candidates.append(fallback)
                seen.add(key)

    wanted = None
    if slug_filter:
        wanted = {item.strip().lower() for item in slug_filter if item and item.strip()}
        candidates = [item for item in candidates if str(item.get('slug') or '').strip().lower() in wanted]

    if force:
        if configured_only:
            forced = []
            seen = set()
            for item in summary.get('outdirs') or []:
                if not item.get('configured'):
                    continue
                slug = item.get('configured_slug') or item.get('slug')
                candidate = {
                    'path': item.get('path'),
                    'slug': slug,
                    'command': f"python3 scripts/web-automation-dispatch.py desktop-probe --slug {slug}" if slug else None,
                    'internal_command': f"python3 scripts/web-automation-dispatch.py desktop-probe --slug {slug}" if slug else None,
                    'recommended_command': f"python3 scripts/web-automation-dispatch.py refresh-desktop --configured-only --slug {slug}" if slug else None,
                    'keep_screenshots': item.get('configured_desktop_keep_screenshots'),
                }
                key = (candidate.get('slug'), candidate.get('path'))
                if key not in seen and candidate.get('command'):
                    forced.append(candidate)
                    seen.add(key)
            candidates = forced
        elif include_all and summary.get('recommended_command') and not candidates:
            candidates = [{
                'path': summary.get('default_outdir'),
                'slug': summary.get('default_configured_slug'),
                'command': summary.get('recommended_command'),
            }]

    if wanted is not None:
        candidates = [item for item in candidates if str(item.get('slug') or '').strip().lower() in wanted]

    if max_targets is not None:
        candidates = candidates[:max(0, max_targets)]
    return summary, candidates


def render_text(result):
    refreshed = result.get('refreshed') or []
    planned_only = bool(result.get('planned_only'))
    candidate_count = result.get('candidate_count', 0)
    if not refreshed and candidate_count == 0:
        return 'Web automation refresh-desktop: niets te verversen'

    if planned_only:
        lines = [
            f"Web automation refresh-desktop plan: {candidate_count} kandidaat/kandidaten"
        ]
        for item in result.get('planned') or []:
            keep_hint = f", keep={item.get('keep_screenshots')}" if item.get('keep_screenshots') else ''
            lines.append(
                f"- {item.get('slug') or item.get('path')}: was {item.get('age_human_before')}, screenshots={item.get('screenshot_count_before')}{keep_hint}, cmd={item.get('command') or '-'}"
            )
        return '\n'.join(lines)

    lines = [
        f"Web automation refresh-desktop: {result.get('refreshed_count', 0)} gedaan, {result.get('success_count', 0)} ok, {result.get('failure_count', 0)} mislukt"
    ]
    for item in refreshed:
        status = 'timeout' if item.get('timed_out') else ('ok' if item.get('ok') else 'fail')
        keep_hint = f", keep={item.get('keep_screenshots')}" if item.get('keep_screenshots') else ''
        lines.append(
            f"- {item.get('slug') or item.get('path')}: {status}, was {item.get('age_human_before')}, screenshots={item.get('screenshot_count_before')}{keep_hint}"
        )
        if item.get('stderr'):
            lines.append(f"  - stderr: {item['stderr'][:160]}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Refresh desktop fallback targets op basis van desktop status observability')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--all', action='store_true', help='neem ook de algemene recommended_command mee als die niet bij configured actions zit')
    parser.add_argument('--configured-only', action='store_true', help='refresh alleen expliciet beheerde desktop targets')
    parser.add_argument('--slug', action='append', help='refresh alleen specifieke slug(s), herhaalbaar')
    parser.add_argument('--adapter', action='append', help='refresh alleen specifieke adapter(s), herhaalbaar')
    parser.add_argument('--max-targets', type=int, default=None, help='maximaal aantal desktop targets om te refreshen')
    parser.add_argument('--force', action='store_true', help='forceer refresh ook als targets volgens hun eigen stale-regels nog niet stale zijn')
    parser.add_argument('--keep-screenshots', type=int, default=None, help='bewaar na elke refresh hooguit dit aantal genummerde screenshots per target')
    parser.add_argument('--stale-after', type=int, default=900, help='stale-drempel in seconden')
    parser.add_argument('--timeout', type=int, default=90, help='timeout per refresh-commando in seconden')
    parser.add_argument('--plan-only', action='store_true', help='toon alleen welke desktop-refreshes nu gepland zouden worden, zonder ze uit te voeren')
    args = parser.parse_args()

    summary, candidates = build_refresh_plan(
        stale_after=args.stale_after,
        include_all=args.all,
        slug_filter=args.slug,
        adapter_filter={str(item).strip().lower() for item in (args.adapter or []) if str(item).strip()},
        max_targets=args.max_targets,
        configured_only=args.configured_only,
        force=args.force,
    )

    before_by_slug = {
        str(item.get('configured_slug') or item.get('slug') or '').strip().lower(): item
        for item in summary.get('outdirs') or []
    }

    planned = []
    for target in candidates:
        slug = str(target.get('slug') or '').strip().lower()
        before = before_by_slug.get(slug) or {}
        planned.append({
            'slug': slug or None,
            'path': target.get('path'),
            'age_seconds_before': before.get('metadata_age_seconds') if before.get('metadata_age_seconds') is not None else before.get('latest_age_seconds'),
            'age_human_before': before.get('metadata_age_human') if before.get('metadata_age_human') not in (None, 'unknown') else before.get('latest_age_human'),
            'screenshot_count_before': before.get('screenshot_count'),
            'keep_screenshots': args.keep_screenshots if args.keep_screenshots is not None else target.get('keep_screenshots'),
            'command': ' '.join(build_command(target, keep_screenshots=args.keep_screenshots) or []),
        })

    refreshed = []
    if not args.plan_only:
        for target in candidates:
            slug = str(target.get('slug') or '').strip().lower()
            before = before_by_slug.get(slug) or {}
            probe = refresh_target(target, timeout_seconds=args.timeout, keep_screenshots=args.keep_screenshots)
            refreshed.append({
                'slug': slug or None,
                'path': target.get('path'),
                'age_seconds_before': before.get('metadata_age_seconds') if before.get('metadata_age_seconds') is not None else before.get('latest_age_seconds'),
                'age_human_before': before.get('metadata_age_human') if before.get('metadata_age_human') not in (None, 'unknown') else before.get('latest_age_human'),
                'screenshot_count_before': before.get('screenshot_count'),
                'keep_screenshots': args.keep_screenshots if args.keep_screenshots is not None else target.get('keep_screenshots'),
                **probe,
            })

    result = {
        'stale_after_seconds': args.stale_after,
        'requested_all': args.all,
        'configured_only': args.configured_only,
        'requested_slugs': args.slug or [],
        'requested_adapters': args.adapter or [],
        'forced': args.force,
        'keep_screenshots': args.keep_screenshots,
        'planned_only': args.plan_only,
        'outdir_count_seen': summary.get('outdir_count', 0),
        'candidate_count': len(candidates),
        'planned': planned,
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
