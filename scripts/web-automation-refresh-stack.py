#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
DISPATCH = ROOT / 'scripts' / 'web-automation-dispatch.py'


def run_json(command):
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = (proc.stdout or '').strip()
    stderr = (proc.stderr or '').strip()
    payload = None
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = None
    return {
        'command': command,
        'returncode': proc.returncode,
        'ok': proc.returncode == 0,
        'stdout': stdout,
        'stderr': stderr,
        'result': payload,
    }


def add_shared_filters(command, args, *, include_timeout=False):
    if args.all:
        command.append('--all')
    if args.configured_only:
        command.append('--configured-only')
    for slug in args.slug:
        command.extend(['--slug', slug])
    for adapter in args.adapter:
        command.extend(['--adapter', adapter])
    if args.stale_after is not None:
        command.extend(['--stale-after', str(args.stale_after)])
    if include_timeout:
        timeout_value = args.timeout if args.timeout is not None else args.site_timeout
        if timeout_value is not None:
            command.extend(['--timeout', str(timeout_value)])
    if args.plan_only:
        command.append('--plan-only')
    return command


def build_sites_command(args):
    command = ['python3', str(DISPATCH), 'refresh-sites', '--json']
    add_shared_filters(command, args, include_timeout=True)
    if args.max_sites is not None:
        command.extend(['--max-sites', str(args.max_sites)])
    if args.max_targets is not None:
        command.extend(['--max-targets', str(args.max_targets)])
    if args.include_terminal:
        command.append('--include-terminal')
    return command


def build_desktop_command(args):
    command = ['python3', str(DISPATCH), 'refresh-desktop', '--json']
    add_shared_filters(command, args, include_timeout=False)
    timeout_value = args.timeout if args.timeout is not None else args.desktop_timeout
    if timeout_value is not None:
        command.extend(['--timeout', str(timeout_value)])
    if args.max_targets is not None:
        command.extend(['--max-targets', str(args.max_targets)])
    if args.force_desktop:
        command.append('--force')
    if args.keep_screenshots is not None:
        command.extend(['--keep-screenshots', str(args.keep_screenshots)])
    return command


def summarize_step(step):
    payload = step.get('result') or {}
    if 'planned' in payload:
        item_count = len(payload.get('planned') or [])
        success_count = payload.get('success_count', 0)
        refreshed_count = payload.get('refreshed_count', 0)
        failure_count = payload.get('failure_count', 0)
        timed_out_count = payload.get('timed_out_count', 0)
        skipped_terminal_count = payload.get('skipped_terminal_count', 0)
    else:
        item_count = payload.get('candidate_count', 0)
        success_count = 0
        refreshed_count = 0
        failure_count = 0
        timed_out_count = 0
        skipped_terminal_count = 0
    return {
        'candidate_count': payload.get('candidate_count', item_count),
        'success_count': success_count,
        'refreshed_count': refreshed_count,
        'failure_count': failure_count,
        'timed_out_count': timed_out_count,
        'skipped_terminal_count': skipped_terminal_count,
        'planned_only': bool(payload.get('planned_only')),
    }


def build_summary(sites_step, desktop_step):
    site_summary = summarize_step(sites_step)
    desktop_summary = summarize_step(desktop_step)
    planned_only = site_summary['planned_only'] or desktop_summary['planned_only']
    return {
        'planned_only': planned_only,
        'ok': sites_step.get('ok', False) and desktop_step.get('ok', False),
        'site_candidate_count': site_summary['candidate_count'],
        'desktop_candidate_count': desktop_summary['candidate_count'],
        'site_refreshed_count': site_summary['refreshed_count'],
        'desktop_refreshed_count': desktop_summary['refreshed_count'],
        'site_success_count': site_summary['success_count'],
        'desktop_success_count': desktop_summary['success_count'],
        'site_failure_count': site_summary['failure_count'],
        'desktop_failure_count': desktop_summary['failure_count'],
        'site_timed_out_count': site_summary['timed_out_count'],
        'desktop_timed_out_count': desktop_summary['timed_out_count'],
        'site_skipped_terminal_count': site_summary['skipped_terminal_count'],
        'desktop_skipped_terminal_count': desktop_summary['skipped_terminal_count'],
    }


def render_text(payload):
    summary = payload['summary']
    lines = ['Web automation refresh stack']
    mode = 'plan' if summary['planned_only'] else 'run'
    lines.append(
        f"- mode: {mode}, ok={summary['ok']}, sites={summary['site_candidate_count']} (success {summary['site_success_count']}, refreshed {summary['site_refreshed_count']}), desktop={summary['desktop_candidate_count']} (success {summary['desktop_success_count']}, refreshed {summary['desktop_refreshed_count']})"
    )
    if summary.get('site_skipped_terminal_count'):
        lines.append(f"- sites manual-boundary skipped: {summary['site_skipped_terminal_count']}")
    if summary.get('desktop_skipped_terminal_count'):
        lines.append(f"- desktop manual-boundary skipped: {summary['desktop_skipped_terminal_count']}")

    sites_result = (payload['sites'] or {}).get('result') or {}
    desktop_result = (payload['desktop'] or {}).get('result') or {}
    site_items = sites_result.get('planned') or sites_result.get('refreshed') or []
    desktop_items = desktop_result.get('planned') or desktop_result.get('refreshed') or []

    if site_items:
        first = site_items[0]
        site_label = first.get('slug') or first.get('label') or first.get('url') or 'site'
        site_command = first.get('command') or ''
        lines.append(f"- site: {site_label} -> {site_command}")
    if desktop_items:
        first = desktop_items[0]
        desktop_label = first.get('slug') or first.get('path') or 'desktop'
        desktop_command = first.get('command') or ''
        lines.append(f"- desktop: {desktop_label} -> {desktop_command}")

    if payload['sites'].get('stderr'):
        lines.append(f"- site stderr: {payload['sites']['stderr']}")
    if payload['desktop'].get('stderr'):
        lines.append(f"- desktop stderr: {payload['desktop']['stderr']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Refresh één web automation target over DOM-site probes en desktop fallback heen')
    parser.add_argument('--all', action='store_true', help='neem niet alleen stale targets maar alle overeenkomende targets mee')
    parser.add_argument('--configured-only', action='store_true', help='beperk tot beheerde registry/desktoptargets')
    parser.add_argument('--slug', action='append', default=[], help='focus op één slug, herhaalbaar')
    parser.add_argument('--adapter', action='append', default=[], help='focus op één adapter, herhaalbaar')
    parser.add_argument('--stale-after', type=int, help='override freshness threshold in seconden')
    parser.add_argument('--timeout', type=int, help='gebruik dezelfde timeout voor site- en desktop-refresh')
    parser.add_argument('--site-timeout', type=int, help='timeout voor DOM/site refreshes')
    parser.add_argument('--desktop-timeout', type=int, help='timeout voor desktop refreshes')
    parser.add_argument('--max-sites', type=int, help='max aantal site-refreshes')
    parser.add_argument('--max-targets', type=int, help='max aantal desktop targets')
    parser.add_argument('--force-desktop', action='store_true', help='force desktop refresh ook als target niet stale lijkt')
    parser.add_argument('--keep-screenshots', type=int, help='bewaar na desktop refresh hooguit dit aantal genummerde screenshots per target')
    parser.add_argument('--include-terminal', action='store_true', help='neem ook manual-boundary/terminal site workflows mee in site-refreshes')
    parser.add_argument('--plan-only', action='store_true', help='toon alleen wat er zou gebeuren')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    sites_step = run_json(build_sites_command(args))
    desktop_step = run_json(build_desktop_command(args))
    payload = {
        'summary': build_summary(sites_step, desktop_step),
        'sites': sites_step,
        'desktop': desktop_step,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload))

    if not payload['summary']['ok']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
