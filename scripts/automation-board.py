#!/usr/bin/env python3
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
AUTOMATION = ROOT / 'scripts' / 'web-automation-dispatch.py'
PROTON = ROOT / 'scripts' / 'proton-status-summary.py'
PROTON_VERIFY = ROOT / 'scripts' / 'proton-verification-status.py'
PROTON_NEXT = ROOT / 'scripts' / 'proton-next-step.py'
PROTON_FINISH = ROOT / 'scripts' / 'proton-manual-finish-summary.py'
ARTIFACTS = ROOT / 'scripts' / 'web-automation-artifacts.py'
SITES = ROOT / 'scripts' / 'web-automation-sites.py'
DESKTOP = ROOT / 'scripts' / 'desktop-fallback-status.py'
PRUNE = ROOT / 'scripts' / 'web-automation-prune.py'
AUTOPILOT = ROOT / 'scripts' / 'web-automation-autopilot.py'
STACK_STATUS = ROOT / 'scripts' / 'web-automation-stack-status.py'


def extend_common_filters(command, args, *, allow_configured=False, allow_attention=False):
    command = list(command)
    command.extend(['--stale-after', str(args.stale_after)])
    for value in args.adapter or []:
        command.extend(['--adapter', value])
    for value in args.slug or []:
        command.extend(['--slug', value])
    if allow_configured and args.configured_only:
        command.append('--configured-only')
    if allow_attention and args.attention_only:
        command.append('--attention-only')
    return command


def include_proton(args):
    adapters = [str(value).strip().lower() for value in (args.adapter or []) if str(value).strip()]
    return 'proton' in adapters


def run_json(cmd, default=None, timeout=25):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired:
        return default, f'timed out: {cmd}'
    if proc.returncode != 0:
        return default, (proc.stderr.strip() or proc.stdout.strip() or f'command failed: {cmd}')
    try:
        return json.loads(proc.stdout), None
    except Exception as exc:
        return default, f'invalid json for {cmd}: {exc}'


def format_target_preview(targets, limit=2):
    labels = [(item.get('label') or item.get('slug') or '?') for item in (targets or []) if (item.get('label') or item.get('slug') or '?')]
    if not labels:
        return ''
    preview = ', '.join(labels[:limit])
    remaining = len(labels) - limit
    if remaining > 0:
        preview += f' +{remaining} meer'
    return preview


def human_bytes(size_bytes):
    if size_bytes is None:
        return '?'
    value = float(size_bytes)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == 'B':
                return f'{int(value)} {unit}'
            return f'{value:.1f} {unit}'
        value /= 1024
    return f'{int(size_bytes)} B'


def select_stack_focus(args, sites):
    site_items = sites.get('sites') or []
    requested = [str(value).strip().lower() for value in (args.slug or []) if str(value).strip()]
    if requested:
        return requested[0]
    for item in site_items:
        if item.get('configured') and item.get('attention_needed', item.get('stale')):
            slug = str(item.get('slug') or '').strip().lower()
            if slug:
                return slug
    for item in site_items:
        if item.get('configured'):
            slug = str(item.get('slug') or '').strip().lower()
            if slug:
                return slug
    return None


def format_stack_queue_items(stacks, limit=3):
    formatted = []
    for item in stacks or []:
        if not isinstance(item, dict):
            continue
        label = item.get('slug') or item.get('label') or '?'
        workflow = item.get('workflow') or {}
        if workflow.get('terminal'):
            state = workflow.get('state') or 'manual-boundary'
            formatted.append(f"{label} [{state}]")
            continue
        dom = item.get('dom') or {}
        desktop = item.get('desktop') or {}
        status_bits = []
        if item.get('attention_needed'):
            status_bits.append('attention')
        elif item.get('healthy'):
            status_bits.append('healthy')
        if dom.get('age_human'):
            status_bits.append(f"dom {dom.get('age_human')}")
        if desktop.get('configured'):
            desktop_age = desktop.get('age_human') or 'unknown'
            status_bits.append(f"desktop {desktop_age}")
        formatted.append(f"{label} [{', '.join(status_bits)}]")
    preview = ', '.join(formatted[:limit])
    remaining = len(formatted) - limit
    if remaining > 0:
        preview += f" +{remaining} meer"
    return preview


def build_board(args):
    jobs = {
        'catalog': (['python3', str(AUTOMATION), 'catalog', '--json'], {'layers': [], 'routes': [], 'aliases': {}}, 25),
        'artifacts': (extend_common_filters(['python3', str(ARTIFACTS), '--json'], args), {}, 25),
        'sites': (extend_common_filters(['python3', str(SITES), '--json'], args, allow_configured=True, allow_attention=True), {}, 25),
        'desktop': (extend_common_filters(['python3', str(DESKTOP), '--json'], args, allow_configured=True), {}, 25),
        'prune': (extend_common_filters(['python3', str(PRUNE), '--json'], args), {}, 25),
        'autopilot': (extend_common_filters(['python3', str(AUTOPILOT), '--json', '--plan-only'], args), {}, 25),
    }

    if include_proton(args):
        jobs.update({
            'proton': (['python3', str(PROTON), '--json'], {}, 25),
            'proton_verify': (['python3', str(PROTON_VERIFY), '--json'], {}, 25),
            'proton_next': (['python3', str(PROTON_NEXT), '--json'], {}, 25),
            'proton_finish': (['python3', str(PROTON_FINISH), '--json'], {}, 25),
        })
    else:
        jobs.update({
            'proton': ({'skipped': True, 'reason': 'adapter filter excludes proton'}, None, None),
            'proton_verify': ({'skipped': True, 'reason': 'adapter filter excludes proton'}, None, None),
            'proton_next': ({'skipped': True, 'reason': 'adapter filter excludes proton'}, None, None),
            'proton_finish': ({'skipped': True, 'reason': 'adapter filter excludes proton'}, None, None),
        })

    runnable_jobs = {
        name: meta for name, meta in jobs.items()
        if isinstance(meta[0], list)
    }

    results = {}
    with ThreadPoolExecutor(max_workers=max(1, len(runnable_jobs))) as pool:
        futures = {
            name: pool.submit(run_json, command, default=default, timeout=timeout)
            for name, (command, default, timeout) in runnable_jobs.items()
        }
        results.update({name: future.result() for name, future in futures.items()})

    for name, (command, default, timeout) in jobs.items():
        if isinstance(command, dict):
            results[name] = (command, None)

    catalog, catalog_error = results['catalog']
    proton, proton_error = results['proton']
    proton_verify, proton_verify_error = results['proton_verify']
    proton_next, proton_next_error = results['proton_next']
    proton_finish, proton_finish_error = results['proton_finish']
    artifacts, artifacts_error = results['artifacts']
    sites, sites_error = results['sites']
    desktop, desktop_error = results['desktop']
    prune, prune_error = results['prune']
    autopilot, autopilot_error = results['autopilot']

    stack_overview_command = extend_common_filters(
        ['python3', str(STACK_STATUS), '--json', '--configured-only', '--artifact-preview', '1'],
        args,
        allow_configured=True,
        allow_attention=True,
    )
    stack_overview, stack_overview_error = run_json(stack_overview_command, default={}, timeout=25)
    stack_overview = stack_overview or {}

    stack_focus_slug = select_stack_focus(args, sites or {})
    stack_focus = {}
    stack_focus_error = None
    if stack_focus_slug:
        focus_candidates = [
            item for item in (stack_overview.get('stacks') or [])
            if str(item.get('slug') or '').strip().lower() == stack_focus_slug
        ]
        if focus_candidates:
            stack_focus = {
                'selected_slug': stack_focus_slug,
                'stacks': focus_candidates,
            }
        else:
            stack_focus_command = extend_common_filters(
                ['python3', str(STACK_STATUS), '--json', '--configured-only', '--slug', stack_focus_slug, '--artifact-preview', '2'],
                args,
            )
            stack_focus, stack_focus_error = run_json(stack_focus_command, default={}, timeout=25)
            stack_focus = stack_focus or {}
            stack_focus['selected_slug'] = stack_focus_slug

    return {
        'layers': (catalog or {}).get('layers', []),
        'route_count': len((catalog or {}).get('routes', [])),
        'routes': (catalog or {}).get('routes', []),
        'aliases': (catalog or {}).get('aliases', {}),
        'filters': {
            'stale_after': args.stale_after,
            'configured_only': bool(args.configured_only),
            'attention_only': bool(args.attention_only),
            'adapters': args.adapter or [],
            'slugs': args.slug or [],
        },
        'proton': proton or {},
        'proton_verify': proton_verify or {},
        'proton_next': proton_next or {},
        'proton_finish': proton_finish or {},
        'artifacts': artifacts or {},
        'sites': sites or {},
        'desktop': desktop or {},
        'prune': prune or {},
        'autopilot': autopilot or {},
        'stack_overview': stack_overview,
        'stack_focus': stack_focus,
        'errors': {k: v for k, v in {
            'catalog': catalog_error,
            'proton': proton_error,
            'proton_verify': proton_verify_error,
            'proton_next': proton_next_error,
            'proton_finish': proton_finish_error,
            'artifacts': artifacts_error,
            'sites': sites_error,
            'desktop': desktop_error,
            'prune': prune_error,
            'autopilot': autopilot_error,
            'stack_overview': stack_overview_error,
            'stack_focus': stack_focus_error,
        }.items() if v},
    }


def render_text(board):
    lines = ['Automation board']
    filters = board.get('filters') or {}
    filter_bits = []
    if filters.get('adapters'):
        filter_bits.append(f"adapter={', '.join(filters.get('adapters') or [])}")
    if filters.get('slugs'):
        filter_bits.append(f"slug={', '.join(filters.get('slugs') or [])}")
    if filters.get('configured_only'):
        filter_bits.append('configured-only')
    if filters.get('attention_only'):
        filter_bits.append('attention-only')
    if filter_bits:
        lines.append(f"- filters: {'; '.join(filter_bits)}")
    sites = board.get('sites') or {}
    desktop = board.get('desktop') or {}
    site_by_slug = {
        str(item.get('slug') or '').strip().lower(): item
        for item in (sites.get('sites') or [])
        if str(item.get('slug') or '').strip()
    }
    desktop_blocking_actions = []
    for action in (desktop.get('configured_recommended_actions') or []):
        slug = str(action.get('slug') or '').strip().lower()
        site = site_by_slug.get(slug)
        if not site:
            desktop_blocking_actions.append(action)
            continue
        if site.get('workflow_terminal'):
            continue
        if not site.get('dom_healthy'):
            desktop_blocking_actions.append(action)
    effective_desktop_operational = not desktop_blocking_actions
    lines.append(f"- lagen: {', '.join(board['layers'])}")
    lines.append(f"- routes: {board['route_count']}")
    artifacts = board.get('artifacts') or {}
    lines.append(
        f"- artifacts: adapters={artifacts.get('adapter_count')}, total={artifacts.get('artifact_count')}, stale={artifacts.get('stale_artifact_count')} (configured {artifacts.get('configured_stale_artifact_count')}, unmanaged {artifacts.get('unmanaged_stale_artifact_count')}), healthy={artifacts.get('healthy')}, operational={artifacts.get('operationally_healthy', artifacts.get('configured_healthy'))}, freshest={artifacts.get('freshest_age_human')}, stalest={artifacts.get('stalest_age_human')}"
    )
    artifact_adapters = artifacts.get('adapters') or []
    artifact_preview_items = [
        f"{item.get('adapter')}:{item.get('artifact_count')}" for item in artifact_adapters[:4]
    ]
    if len(artifact_adapters) > 4:
        artifact_preview_items.append(f"+{len(artifact_adapters) - 4} meer")
    top_adapters = ', '.join(artifact_preview_items)
    if top_adapters:
        lines.append(f"- artifact adapters: {top_adapters}")
    actions = artifacts.get('configured_recommended_actions') or []
    if actions:
        first = actions[0]
        lines.append(f"- artifact refresh: {first.get('adapter')} -> {first.get('command')}")
    prune = board.get('prune') or {}
    prune_count = prune.get('candidate_count', 0)
    prune_targets = prune.get('target_count', 0)
    prune_target_preview = format_target_preview(prune.get('targets'))
    if artifacts.get('unmanaged_stale_artifact_count') and not artifacts.get('configured_stale_artifact_count'):
        lines.append('- artifact nuance: alleen onbeheerde/demo artifacts zijn stale, beheerde automation-artifacts zijn operationeel gezond')
        prune_line = '- artifact prune: python3 scripts/web-automation-dispatch.py prune-unmanaged'
        if prune_count:
            prune_line += f' ({prune_count} path(s)'
            if prune_targets:
                prune_line += f', {prune_targets} target(s)'
            if prune.get('total_size_bytes') is not None:
                prune_line += f', {human_bytes(prune.get("total_size_bytes"))}'
            prune_line += ')'
        if prune_target_preview:
            prune_line += f' -> {prune_target_preview}'
        lines.append(prune_line)
    lines.append(
        f"- generic sites: count={sites.get('site_count')}, stale={sites.get('stale_site_count')} (configured {sites.get('configured_stale_site_count')}, unmanaged {sites.get('unmanaged_stale_site_count')}), healthy={sites.get('healthy')}, operational={sites.get('operationally_healthy', sites.get('configured_healthy'))}, freshest={sites.get('freshest_age_human')}, stalest={sites.get('stalest_age_human')}"
    )
    site_items = sites.get('sites') or []
    site_preview_items = [f"{item.get('slug')}:{item.get('adapter')}" for item in site_items[:4]]
    if len(site_items) > 4:
        site_preview_items.append(f"+{len(site_items) - 4} meer")
    site_preview = ', '.join(site_preview_items)
    if site_preview:
        lines.append(f"- site adapters: {site_preview}")
    adapter_summaries = sites.get('adapter_summaries') or []
    adapter_preview_items = [
        f"{item.get('adapter')}:{item.get('site_count')}"
        + (f" latest={item.get('latest_age_human')}" if item.get('latest_age_human') else '')
        + (f" stale={item.get('stale_site_count')}" if item.get('stale_site_count') else '')
        + (f" cfg={item.get('configured_stale_site_count')}" if item.get('configured_stale_site_count') else '')
        + (f" -> {item.get('next_attention_slug')}" if item.get('next_attention_slug') else '')
        for item in adapter_summaries[:4]
    ]
    if len(adapter_summaries) > 4:
        adapter_preview_items.append(f"+{len(adapter_summaries) - 4} meer")
    adapter_health = ', '.join(adapter_preview_items)
    if adapter_health:
        lines.append(f"- site adapter health: {adapter_health}")
    first_adapter_attention = next((item for item in (sites.get('adapter_summaries') or []) if item.get('next_attention_command')), None)
    stale_site = next(
        (
            item for item in (sites.get('sites') or [])
            if item.get('attention_needed', item.get('stale')) and item.get('configured') and item.get('recommended_command')
        ),
        None,
    )
    if first_adapter_attention and (
        not stale_site or first_adapter_attention.get('next_attention_command') != stale_site.get('recommended_command')
    ):
        lines.append(f"- site adapter refresh: {first_adapter_attention.get('adapter')} -> {first_adapter_attention.get('next_attention_command')}")
    if stale_site:
        stack_command = stale_site.get('stack_command') if stale_site.get('desktop_stale') else None
        if stack_command:
            lines.append(f"- stack refresh: {stale_site.get('slug')} -> {stack_command}")
        lines.append(f"- site refresh: {stale_site.get('slug')} -> {stale_site.get('recommended_command')}")
        lines.append("- maintenance: python3 scripts/web-automation-dispatch.py autopilot")
    autopilot = board.get('autopilot') or {}
    if autopilot.get('decision'):
        lines.append(f"- autopilot next: {autopilot.get('decision')} ({autopilot.get('reason')})")
        target_preview = ', '.join((autopilot.get('target_summary') or {}).get('preview') or [])
        if target_preview:
            lines.append(f"- autopilot targets: {target_preview}")
        planned = (autopilot.get('action') or {}).get('command')
        if planned:
            lines.append(f"- autopilot plan: {' '.join(planned)}")
        follow_up_preview = ', '.join((((autopilot.get('follow_up') or {}).get('target_summary') or {}).get('preview') or []))
        if follow_up_preview:
            lines.append(f"- autopilot daarna: {follow_up_preview}")
    stack_overview = board.get('stack_overview') or {}
    queue_candidates = [
        item for item in (stack_overview.get('stacks') or [])
        if (item.get('workflow') or {}).get('terminal') or item.get('attention_needed')
    ]
    if not queue_candidates:
        queue_candidates = (stack_overview.get('stacks') or [])
    stack_queue_preview = format_stack_queue_items(queue_candidates)
    if stack_queue_preview:
        lines.append(f"- stack queue: {stack_queue_preview}")
    stack_focus = board.get('stack_focus') or {}
    focus_items = stack_focus.get('stacks') or []
    if focus_items:
        focus = focus_items[0]
        dom = focus.get('dom') or {}
        desktop_focus = focus.get('desktop') or {}
        workflow = focus.get('workflow') or {}
        if workflow.get('terminal'):
            lines.append(
                f"- stack focus: {focus.get('slug')} [{focus.get('status')}] workflow={workflow.get('state') or '-'}"
            )
            lines.append(
                f"- stack observability: dom={dom.get('age_human')} desktop="
                + (desktop_focus.get('age_human') or ('uit' if not desktop_focus.get('configured') else 'unknown'))
            )
        else:
            lines.append(
                f"- stack focus: {focus.get('slug')} [{focus.get('status')}] dom={dom.get('age_human')} desktop="
                + (desktop_focus.get('age_human') or ('uit' if not desktop_focus.get('configured') else 'unknown'))
                + (f" workflow={workflow.get('state')}" if workflow.get('state') else '')
            )
        preview = focus.get('artifacts', {}).get('preview') or []
        if preview:
            preview_text = ', '.join(
                f"{entry.get('artifact')} ({entry.get('age_human')})"
                for entry in preview
            )
            lines.append(f"- stack artifacts: {preview_text}")
        if focus.get('recommended_command'):
            lines.append(f"- stack next: {focus.get('recommended_command')}")
        if focus.get('slug') and focus.get('status') in {'attention', 'stale', 'missing'}:
            lines.append(f"- stack selectors: python3 scripts/web-automation-dispatch.py selectors --slug {focus.get('slug')}")
    lines.append(
        f"- desktop fallback: stale={desktop.get('stale_outdir_count')} (configured {desktop.get('configured_attention_target_count', desktop.get('configured_stale_outdir_count'))}, missing {desktop.get('missing_configured_target_count', 0)}, blocking {len(desktop_blocking_actions)}, unmanaged {desktop.get('unmanaged_stale_outdir_count')}), healthy={desktop.get('healthy')}, operational={effective_desktop_operational}, latest={desktop.get('display_latest_age_human', desktop.get('default_latest_age_human'))}, screenshots={desktop.get('display_screenshot_count', desktop.get('screenshot_count'))}, windows={desktop.get('display_has_windows_capture', desktop.get('default_has_windows_capture'))}"
    )
    if desktop.get('display_scope') == 'configured' and desktop.get('display_path'):
        lines.append(f"- desktop display: beheerde target {desktop.get('display_slug') or desktop.get('display_path')} als referentie")
    if desktop.get('unmanaged_stale_outdir_count') and not desktop.get('configured_attention_target_count', desktop.get('configured_stale_outdir_count')):
        lines.append('- desktop nuance: alleen onbeheerde/demo desktop-artifacts zijn stale, beheerde desktop fallbacks zijn operationeel gezond')
        prune_line = '- desktop prune: python3 scripts/web-automation-dispatch.py prune-unmanaged'
        if prune_count:
            prune_line += f' ({prune_count} path(s)'
            if prune_targets:
                prune_line += f', {prune_targets} target(s)'
            if prune.get('total_size_bytes') is not None:
                prune_line += f', {human_bytes(prune.get("total_size_bytes"))}'
            prune_line += ')'
        if prune_target_preview:
            prune_line += f' -> {prune_target_preview}'
        lines.append(prune_line)
    if desktop_blocking_actions:
        if desktop_blocking_actions[0].get('stack_command'):
            lines.append(f"- desktop stack refresh: {desktop_blocking_actions[0].get('stack_command')}")
        lines.append(f"- desktop refresh: {desktop_blocking_actions[0].get('recommended_command')}")
    elif desktop.get('configured_attention_target_count', desktop.get('configured_stale_outdir_count')):
        lines.append('- desktop nuance: sommige beheerde desktop fallbacks zijn stale, maar hun DOM probe is al gezond')
    elif desktop.get('recommended_command'):
        lines.append(f"- desktop refresh: {desktop.get('recommended_command')}")
    proton = board['proton']
    if not proton.get('skipped'):
        start = proton.get('start', {})
        route = proton.get('route', {})
        proton_verify = board.get('proton_verify') or {}
        manual_boundary = bool(proton.get('manual_boundary')) or bool(proton_verify.get('account_created')) or bool(proton_verify.get('recovery_kit_ready'))
        phase = 'account_created' if manual_boundary else ('password_step' if route.get('reached_password_step') else ('start_page' if start.get('signup_visible') else 'unknown'))
        submit_ready = False if manual_boundary else bool(route.get('reached_password_step') and route.get('password_visible') and route.get('password_confirm_visible') and route.get('get_started_visible'))
        lines.append(
            f"- proton: fase={phase}, submit-ready={submit_ready}, blocked={start.get('blocked', False)}, regressie={proton.get('regression_suspected')}"
        )
        lines.append(
            f"- verify: screen={proton_verify.get('verification_screen')}, stale={proton_verify.get('stale')}, mail_matches={proton_verify.get('verification_mail_matches')}, used_code={proton_verify.get('latest_used_code')}, pw_ready={proton_verify.get('password_setup_ready')}, account_created={proton_verify.get('account_created')}, recovery_kit={proton_verify.get('recovery_kit_ready')}, next={proton_verify.get('recommended_action')}"
        )
        proton_next = board.get('proton_next') or {}
        lines.append(
            f"- proton-next: route={proton_next.get('recommended_route')}, stale={proton_next.get('stale')}, why={proton_next.get('reason')}"
        )
        proton_command = proton_next.get('recommended_command') or proton_next.get('command')
        if proton_command:
            lines.append(f"- proton command: {proton_command}")
        proton_finish = board.get('proton_finish') or {}
        if proton_finish.get('manual_boundary'):
            lines.append(
                f"- proton handoff: recovery_kit={proton_finish.get('recovery_kit_ready')}, account_created={proton_finish.get('account_created')}, route={proton_finish.get('recommended_route')}, source={proton_finish.get('verification_source')}, age={proton_finish.get('verification_age_seconds')}s"
            )
            if proton_finish.get('recommended_command'):
                lines.append(f"- proton handoff command: {proton_finish.get('recommended_command')}")
            checklist = proton_finish.get('checklist') or []
            if checklist:
                lines.append(f"- proton checklist: {checklist[0]}")
    if board['routes']:
        preview = ', '.join(route['name'] for route in board['routes'][:4])
        extra = len(board['routes']) - 4
        lines.append(f"- eerste routes: {preview}" + (f" (+{extra})" if extra > 0 else ''))
    if board['aliases']:
        aliases = ', '.join(f"{k}->{v}" for k, v in list(sorted(board['aliases'].items()))[:4])
        extra = len(board['aliases']) - 4
        lines.append(f"- aliases: {aliases}" + (f" (+{extra})" if extra > 0 else ''))
    errors = board.get('errors') or {}
    if errors:
        lines.append(f"- gedegradeerd: {', '.join(sorted(errors))}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compact overzicht van web automation routes en status')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--configured-only', action='store_true', help='focus op beheerde registry-targets waar mogelijk')
    parser.add_argument('--attention-only', action='store_true', help='focus sites-view op targets die nu aandacht nodig hebben')
    parser.add_argument('--adapter', action='append', help='focus op specifieke adapter(s), herhaalbaar')
    parser.add_argument('--slug', action='append', help='focus op specifieke slug(s), herhaalbaar')
    parser.add_argument('--stale-after', type=int, default=900, help='globale stale-drempel in seconden')
    args = parser.parse_args()

    board = build_board(args)
    if args.json:
        print(json.dumps(board, ensure_ascii=False, indent=2))
    else:
        print(render_text(board))


if __name__ == '__main__':
    main()
