#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SITES = ROOT / 'scripts' / 'web-automation-sites.py'
ARTIFACTS = ROOT / 'scripts' / 'web-automation-artifacts.py'
DESKTOP = ROOT / 'scripts' / 'desktop-fallback-status.py'


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
        raise SystemExit(f'Invalid JSON from command: {exc}\n{proc.stdout[:500]}')


def fmt_age(seconds):
    if seconds is None:
        return 'unknown'
    seconds = int(seconds)
    if seconds < 60:
        return f'{seconds}s'
    if seconds < 3600:
        return f'{seconds // 60}m'
    return f'{seconds // 3600}h{(seconds % 3600) // 60:02d}m'


def add_common_filters(command, args, *, include_slug=False, allow_configured=False):
    if allow_configured and args.configured_only:
        command.append('--configured-only')
    if include_slug:
        for value in args.slug or []:
            command.extend(['--slug', value])
    for value in args.adapter or []:
        command.extend(['--adapter', value])
    command.extend(['--stale-after', str(args.stale_after)])
    return command


def site_sort_key(site):
    return (
        not site.get('attention_needed', site.get('stale')),
        not bool(site.get('configured')),
        site.get('adapter') or '',
        site.get('age_seconds') is None,
        -(site.get('age_seconds') or 0),
        site.get('slug') or '',
    )


def build_summary(args):
    sites = run_json(add_common_filters(['python3', str(SITES), '--json'], args, include_slug=True, allow_configured=True))
    artifacts = run_json(add_common_filters(['python3', str(ARTIFACTS), '--json'], args, include_slug=False, allow_configured=False))
    desktop = run_json(add_common_filters(['python3', str(DESKTOP), '--json'], args, include_slug=True, allow_configured=True))

    artifacts_by_site = defaultdict(list)
    for item in artifacts.get('items') or []:
        if not isinstance(item, dict):
            continue
        key = (item.get('site_slug') or item.get('slug') or '').strip().lower()
        if key:
            artifacts_by_site[key].append(item)

    desktop_by_slug = {}
    for item in desktop.get('outdirs') or []:
        if not isinstance(item, dict):
            continue
        key = (item.get('configured_slug') or item.get('slug') or '').strip().lower()
        if key:
            desktop_by_slug[key] = item

    stacks = []
    for site in sorted(sites.get('sites') or [], key=site_sort_key):
        slug = str(site.get('slug') or '').strip().lower()
        related_artifacts = sorted(
            artifacts_by_site.get(slug, []),
            key=lambda item: (
                item.get('age_seconds') is None,
                item.get('age_seconds') or 0,
                item.get('artifact') or '',
            ),
        )
        desktop_item = desktop_by_slug.get(slug)
        dom_stale = bool(site.get('dom_stale', site.get('stale')))
        desktop_stale = bool(site.get('desktop_stale')) if site.get('desktop_configured') else None
        workflow_terminal = bool(site.get('workflow_terminal'))
        attention_needed = bool(site.get('attention_needed', site.get('stale')))
        if args.attention_only and not attention_needed:
            continue

        recommendation = site.get('recommended_command')
        if workflow_terminal and site.get('handoff_command'):
            recommendation = site.get('handoff_command')
        elif site.get('stack_command') and site.get('desktop_configured') and (dom_stale or bool(site.get('desktop_stale'))):
            recommendation = site.get('stack_command')
        elif site.get('desktop_command') and not dom_stale and bool(site.get('desktop_stale')):
            recommendation = site.get('desktop_command')

        status_bits = []
        if workflow_terminal:
            status_bits.append('manual-boundary')
            if recommendation:
                status_bits.append('handoff-ready')
        elif attention_needed:
            status_bits.append('attention')
        else:
            status_bits.append('healthy')
        if not workflow_terminal:
            if dom_stale:
                status_bits.append('dom-stale')
            if desktop_stale is True:
                status_bits.append('desktop-stale')
            if site.get('missing_artifact'):
                status_bits.append('dom-missing')
            if site.get('desktop_configured') and not desktop_item:
                status_bits.append('desktop-missing')

        artifact_preview = []
        for item in related_artifacts[: max(0, args.artifact_preview)]:
            artifact_preview.append({
                'artifact': item.get('artifact'),
                'age_human': item.get('age_human') or fmt_age(item.get('age_seconds')),
                'title': item.get('title'),
                'stale': bool(item.get('stale')),
                'raw_stale': bool(item.get('raw_stale')),
                'workflow_state': item.get('workflow_state'),
            })

        stacks.append({
            'slug': slug,
            'label': site.get('label'),
            'adapter': site.get('adapter'),
            'configured': bool(site.get('configured')),
            'status': ', '.join(status_bits),
            'healthy': bool(site.get('operationally_healthy')),
            'attention_needed': attention_needed,
            'recommended_command': recommendation,
            'notes': site.get('notes') or '',
            'url': site.get('url'),
            'final_url': site.get('final_url'),
            'title': site.get('title'),
            'dom': {
                'checked_at': site.get('checked_at'),
                'age_seconds': site.get('age_seconds'),
                'age_human': site.get('age_human') or fmt_age(site.get('age_seconds')),
                'stale': dom_stale,
                'healthy': bool(site.get('dom_healthy', not dom_stale)),
                'interactive_count': site.get('interactive_count'),
                'form_count': site.get('form_count'),
                'missing_artifact': bool(site.get('missing_artifact')),
                'recommended_command': site.get('recommended_command'),
                'refresh_command': site.get('refresh_command'),
            },
            'desktop': {
                'configured': bool(site.get('desktop_configured')),
                'path': site.get('desktop_path') or (desktop_item or {}).get('path'),
                'age_seconds': site.get('desktop_age_seconds') if site.get('desktop_configured') else None,
                'age_human': site.get('desktop_age_human') if site.get('desktop_configured') else None,
                'stale': desktop_stale,
                'healthy': bool(site.get('desktop_healthy')) if site.get('desktop_configured') else None,
                'screenshot_count': site.get('desktop_screenshot_count') if site.get('desktop_configured') else None,
                'metadata_success': site.get('desktop_metadata_success') if site.get('desktop_configured') else None,
                'command': site.get('desktop_command'),
                'stack_command': site.get('stack_command'),
                'keep_screenshots': site.get('desktop_keep_screenshots'),
            },
            'workflow': {
                'state': site.get('workflow_state'),
                'terminal': workflow_terminal,
                'attention': site.get('workflow_attention'),
                'note': site.get('workflow_note'),
                'checked_at': site.get('workflow_checked_at'),
                'age_seconds': site.get('workflow_age_seconds'),
                'age_human': fmt_age(site.get('workflow_age_seconds')) if site.get('workflow_age_seconds') is not None else None,
                'stale': site.get('workflow_stale'),
                'command': site.get('handoff_command') or site.get('workflow_command'),
            },
            'artifacts': {
                'count': len(related_artifacts),
                'latest_age_seconds': related_artifacts[0].get('age_seconds') if related_artifacts else None,
                'latest_age_human': related_artifacts[0].get('age_human') if related_artifacts else None,
                'preview': artifact_preview,
            },
        })

    attention_count = sum(1 for item in stacks if item.get('attention_needed'))
    manual_count = sum(1 for item in stacks if item.get('workflow', {}).get('terminal'))
    return {
        'stale_after_seconds': args.stale_after,
        'configured_only': args.configured_only,
        'requested_slugs': args.slug or [],
        'requested_adapters': args.adapter or [],
        'attention_only': args.attention_only,
        'stack_count': len(stacks),
        'attention_count': attention_count,
        'manual_boundary_count': manual_count,
        'healthy_count': sum(1 for item in stacks if item.get('healthy')),
        'stacks': stacks,
    }


def render_text(summary):
    stacks = summary.get('stacks') or []
    if not stacks:
        return 'Web automation stack: geen targets gevonden'
    lines = [
        f"Web automation stack: {summary.get('stack_count', 0)} target(s), attention {summary.get('attention_count', 0)}, manual-boundary {summary.get('manual_boundary_count', 0)}"
    ]
    for item in stacks:
        dom = item.get('dom') or {}
        desktop = item.get('desktop') or {}
        workflow = item.get('workflow') or {}
        artifact_preview = item.get('artifacts', {}).get('preview') or []
        head = f"- {item.get('slug')}: {item.get('status')} [{item.get('adapter') or '-'}]"
        if item.get('title'):
            head += f" | {item.get('title')[:90]}"
        lines.append(head)
        if workflow.get('terminal'):
            lines.append(
                f"  observability dom={dom.get('age_human')} forms={dom.get('form_count')} interactive={dom.get('interactive_count')}"
            )
            if desktop.get('configured'):
                lines.append(
                    f"  observability desktop={desktop.get('age_human') or 'unknown'} screenshots={desktop.get('screenshot_count')} ok={desktop.get('metadata_success')}"
                )
            else:
                lines.append('  observability desktop=uit')
        else:
            lines.append(
                f"  dom={dom.get('age_human')} stale={dom.get('stale')} forms={dom.get('form_count')} interactive={dom.get('interactive_count')}"
            )
            if desktop.get('configured'):
                lines.append(
                    f"  desktop={desktop.get('age_human') or 'unknown'} stale={desktop.get('stale')} screenshots={desktop.get('screenshot_count')} ok={desktop.get('metadata_success')}"
                )
            else:
                lines.append('  desktop=uit')
        if workflow.get('state'):
            note = workflow.get('note') or ''
            note = note[:140] + '…' if len(note) > 140 else note
            lines.append(
                f"  workflow={workflow.get('state')} attention={workflow.get('attention') or '-'} stale={workflow.get('stale')}"
                + (f" | {note}" if note else '')
            )
        if artifact_preview:
            preview = ', '.join(
                f"{entry.get('artifact')} ({entry.get('age_human')})"
                for entry in artifact_preview
            )
            lines.append(f"  artifacts={item.get('artifacts', {}).get('count', 0)} | {preview}")
        if item.get('recommended_command'):
            lines.append(f"  next={item.get('recommended_command')}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Toon per managed site een stack-overzicht over DOM, desktop fallback en workflow state')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--configured-only', action='store_true', help='toon alleen beheerde registry-targets')
    parser.add_argument('--slug', action='append', help='focus op specifieke slug(s), herhaalbaar')
    parser.add_argument('--adapter', action='append', help='focus op specifieke adapter(s), herhaalbaar')
    parser.add_argument('--attention-only', action='store_true', help='toon alleen targets die nu aandacht vragen')
    parser.add_argument('--stale-after', type=int, default=900, help='globale stale-drempel in seconden')
    parser.add_argument('--artifact-preview', type=int, default=3, help='hoeveel recente artifacts per target tonen')
    args = parser.parse_args()

    summary = build_summary(args)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
