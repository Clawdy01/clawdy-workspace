#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
DISPATCH = ROOT / 'scripts' / 'web-automation-dispatch.py'
PROTON_NEXT = ROOT / 'scripts' / 'proton-next-step.py'
DESKTOP_STATUS = ROOT / 'scripts' / 'desktop-fallback-status.py'
PRUNE_UNMANAGED = ROOT / 'scripts' / 'web-automation-prune.py'
SAFE_PROTON_ROUTES = {
    'proton-refresh',
    'proton-password-step',
    'investigate-password-regression',
    'proton-submit-ready',
    'proton-verify-refresh',
    'proton-request-code',
    'proton-use-code',
    'continue-password-setup',
}
MULTI_STEP_ROUTES = {
    'refresh-sites',
    'refresh-desktop',
    'refresh-stack',
    'desktop-probe',
    'prune-unmanaged',
}
PLAN_ONLY_APPEND_ROUTES = {
    'refresh-sites',
    'refresh-desktop',
    'refresh-stack',
}


def normalized_adapters(adapter_filter=None):
    return sorted({str(item).strip().lower() for item in (adapter_filter or []) if str(item).strip()})


def extend_adapter_args(command, adapter_filter=None):
    for adapter in normalized_adapters(adapter_filter):
        command.extend(['--adapter', adapter])
    return command


def summarize_targets(items, *, slug_key='slug', label_key='label', limit=3):
    summary_items = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        slug = str(item.get(slug_key) or '').strip().lower()
        label = str(item.get(label_key) or item.get(slug_key) or '').strip()
        if not slug and not label:
            continue
        summary_items.append({
            'slug': slug or None,
            'label': label or slug,
        })
    return {
        'count': len(summary_items),
        'items': summary_items,
        'preview': [item.get('label') or item.get('slug') for item in summary_items[:max(0, limit)]],
    }


def run_json(cmd, timeout=240, default=None):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def run_capture(cmd, timeout=300):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = exc
        timed_out = True
    if timed_out:
        return {
            'command': cmd,
            'ok': False,
            'returncode': 124,
            'stdout': (proc.stdout or '').strip() if getattr(proc, 'stdout', None) else '',
            'stderr': ((proc.stderr or '').strip() + ('\n' if getattr(proc, 'stderr', None) else '') + f'timeout after {timeout}s').strip(),
            'result': None,
        }
    parsed = None
    if (proc.stdout or '').strip():
        try:
            parsed = json.loads(proc.stdout)
        except Exception:
            parsed = None
    return {
        'command': cmd,
        'ok': proc.returncode == 0,
        'returncode': proc.returncode,
        'stdout': (proc.stdout or '').strip(),
        'stderr': (proc.stderr or '').strip(),
        'result': parsed,
    }


def decide(max_site_refreshes, stale_after, site_timeout, apply_prune=False, adapter_filter=None):
    requested_adapters = normalized_adapters(adapter_filter)
    allow_proton = not requested_adapters or 'proton' in requested_adapters

    sites_command = ['python3', str(DISPATCH), 'sites', '--json', '--stale-after', str(stale_after)]
    extend_adapter_args(sites_command, requested_adapters)
    sites = run_json(sites_command, default={}) or {}

    desktop_command = ['python3', str(DESKTOP_STATUS), '--json', '--stale-after', str(stale_after)]
    extend_adapter_args(desktop_command, requested_adapters)
    desktop = run_json(desktop_command, default={}) or {}

    prune_command = ['python3', str(PRUNE_UNMANAGED), '--json', '--stale-after', str(stale_after)]
    extend_adapter_args(prune_command, requested_adapters)
    prune = run_json(prune_command, default={}) or {}

    proton_next = run_json(['python3', str(PROTON_NEXT), '--json'], default={}) or {} if allow_proton else {}

    site_items = sites.get('sites') or []
    site_by_slug = {
        str(site.get('slug') or '').strip().lower(): site
        for site in site_items
        if str(site.get('slug') or '').strip()
    }
    stale_sites = [site for site in site_items if site.get('attention_needed', site.get('stale'))]
    terminal_sites = [site for site in site_items if site.get('workflow_terminal')]
    stale_generic_sites = [site for site in stale_sites if site.get('adapter') != 'proton' and site.get('configured')]
    stale_stack_sites = [site for site in stale_generic_sites if site.get('dom_stale') and site.get('desktop_stale') and site.get('stack_command')]
    blocking_desktop_actions = []
    for action in (desktop.get('configured_recommended_actions') or []):
        slug = str(action.get('slug') or '').strip().lower()
        site = site_by_slug.get(slug)
        if not site:
            blocking_desktop_actions.append(action)
            continue
        if site.get('workflow_terminal'):
            continue
        if not site.get('dom_healthy'):
            blocking_desktop_actions.append(action)
    non_blocking_desktop_actions = [
        action for action in (desktop.get('configured_recommended_actions') or [])
        if action not in blocking_desktop_actions
    ]
    if stale_stack_sites:
        selected_sites = stale_stack_sites[:max(1, max_site_refreshes)]
        command = [
            'python3', str(DISPATCH), 'refresh-stack', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-sites', str(max(1, max_site_refreshes)), '--max-targets', str(max(1, max_site_refreshes)),
        ]
        extend_adapter_args(command, requested_adapters)
        for site in selected_sites:
            if site.get('slug'):
                command += ['--slug', site['slug']]
        return {
            'route': 'refresh-stack',
            'reason': f"{len(stale_stack_sites)} beheerde niet-Proton observability stack(s) hebben tegelijk stale DOM en desktop fallback",
            'command': command,
            'command_timeout': max(60, site_timeout) + 15,
            'target_summary': summarize_targets(selected_sites),
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    if stale_generic_sites:
        selected_sites = stale_generic_sites[:max(1, max_site_refreshes)]
        command = ['python3', str(DISPATCH), 'refresh-sites', '--json', '--configured-only', '--stale-after', str(stale_after), '--max-sites', str(max(1, max_site_refreshes))]
        extend_adapter_args(command, requested_adapters)
        for site in selected_sites:
            if site.get('slug'):
                command += ['--slug', site['slug']]
        return {
            'route': 'refresh-sites',
            'reason': f"{len(stale_generic_sites)} beheerde niet-Proton site-probes zijn stale of missen verse artifacts",
            'command': command,
            'command_timeout': site_timeout,
            'target_summary': summarize_targets(selected_sites),
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    if blocking_desktop_actions:
        first = blocking_desktop_actions[0]
        command = [
            'python3', str(DISPATCH), 'refresh-desktop', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-targets', '1', '--timeout', str(max(60, site_timeout)),
        ]
        extend_adapter_args(command, requested_adapters)
        if first.get('slug'):
            command += ['--slug', str(first['slug'])]
        return {
            'route': 'refresh-desktop',
            'reason': f"{len(blocking_desktop_actions)} beheerde desktop fallback target(s) missen nog een bruikbare verse fallback naast een niet-gezonde DOM probe",
            'command': command,
            'command_timeout': max(60, site_timeout) + 15,
            'target_summary': summarize_targets([first]),
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    if non_blocking_desktop_actions and sites.get('operationally_healthy'):
        first = non_blocking_desktop_actions[0]
        command = [
            'python3', str(DISPATCH), 'refresh-desktop', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-targets', '1', '--timeout', str(max(60, site_timeout)),
        ]
        extend_adapter_args(command, requested_adapters)
        if first.get('slug'):
            command += ['--slug', str(first['slug'])]
        return {
            'route': 'refresh-desktop',
            'reason': f"{len(non_blocking_desktop_actions)} beheerde desktop fallback target(s) missen nog een verse fallback terwijl hun DOM probe al gezond is",
            'command': command,
            'command_timeout': max(60, site_timeout) + 15,
            'target_summary': summarize_targets([first]),
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    if not desktop.get('healthy') and desktop.get('recommended_command'):
        latest_age_human = (
            desktop.get('display_latest_age_human')
            or desktop.get('freshest_age_human')
            or desktop.get('default_latest_age_human')
            or 'unknown'
        )
        return {
            'route': 'desktop-probe',
            'reason': f"desktop fallback artifacts zijn stale (latest {latest_age_human})",
            'command': ['python3', str(DISPATCH), 'desktop-probe'],
            'command_timeout': max(60, site_timeout),
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    if sites.get('operationally_healthy') and not blocking_desktop_actions and prune.get('candidate_count'):
        command = ['python3', str(PRUNE_UNMANAGED), '--json', '--stale-after', str(stale_after)]
        extend_adapter_args(command, requested_adapters)
        route = 'prune-unmanaged-review'
        reason = f"beheerde web automation is gezond, maar {prune.get('candidate_count')} onbeheerde stale artifact(s)/outdir(s) kunnen naar Trash"
        if apply_prune:
            command.append('--apply')
            route = 'prune-unmanaged'
            reason = f"beheerde web automation is gezond, dus {prune.get('candidate_count')} onbeheerde stale artifact(s)/outdir(s) gaan veilig naar Trash"
        return {
            'route': route,
            'reason': reason,
            'command': command,
            'command_timeout': 30,
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    proton_route = proton_next.get('recommended_route')
    if proton_route in SAFE_PROTON_ROUTES:
        return {
            'route': 'proton-autopilot-safe',
            'reason': proton_next.get('reason') or 'veilige Proton vervolgstap beschikbaar',
            'command': ['python3', str(DISPATCH), 'proton-autopilot-safe', '--json', '--max-steps', '2'],
            'command_timeout': max(120, site_timeout),
            'requested_adapters': requested_adapters,
            'sites': sites,
            'terminal_sites': terminal_sites,
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        }

    return {
        'route': 'noop',
        'reason': 'geen veilige of nuttige web automation vervolgstap beschikbaar',
        'command': None,
        'requested_adapters': requested_adapters,
        'sites': sites,
        'terminal_sites': terminal_sites,
        'proton_next': proton_next,
        'desktop': desktop,
        'prune': prune,
    }


def action_made_progress(route, action):
    if not action.get('ok'):
        return False
    result = action.get('result') or {}
    if route in {'refresh-sites', 'refresh-desktop'}:
        return (result.get('success_count') or 0) > 0
    if route == 'refresh-stack':
        return ((result.get('site_success_count') or 0) + (result.get('desktop_success_count') or 0)) > 0
    if route == 'prune-unmanaged':
        return any(item.get('ok') for item in (result.get('results') or []))
    if route == 'desktop-probe':
        if isinstance(result, dict) and 'success' in result:
            return bool(result.get('success'))
        return True
    if route == 'proton-autopilot-safe':
        return bool(result.get('advanced')) or result.get('before_route') != result.get('after_route')
    return bool(action.get('ok'))


def extract_handled_slugs(command):
    handled = []
    parts = list(command or [])
    for index, part in enumerate(parts):
        if part == '--slug' and index + 1 < len(parts):
            slug = str(parts[index + 1]).strip().lower()
            if slug:
                handled.append(slug)
    return handled


def build_remaining_refresh_decision(route, remaining_stale_generic_sites, requested_adapters, stale_after, site_timeout, max_site_refreshes):
    remaining_stack_sites = [site for site in remaining_stale_generic_sites if site.get('dom_stale') and site.get('desktop_stale') and site.get('stack_command')]
    if route == 'refresh-stack' and remaining_stack_sites:
        selected_sites = remaining_stack_sites[:max(1, max_site_refreshes)]
        command = [
            'python3', str(DISPATCH), 'refresh-stack', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-sites', str(max(1, max_site_refreshes)), '--max-targets', str(max(1, max_site_refreshes)), '--plan-only',
        ]
        extend_adapter_args(command, requested_adapters)
        for site in selected_sites:
            if site.get('slug'):
                command += ['--slug', site['slug']]
        return {
            'decision': 'refresh-stack',
            'reason': f"na een succesvolle stack-refresh blijven waarschijnlijk nog {len(remaining_stack_sites)} beheerde observability stack(s) over met tegelijk stale DOM en desktop fallback",
            'action': run_capture(command, timeout=20),
            'target_summary': summarize_targets(selected_sites),
            'predicted': True,
        }

    if remaining_stale_generic_sites:
        selected_sites = remaining_stale_generic_sites[:max(1, max_site_refreshes)]
        command = [
            'python3', str(DISPATCH), 'refresh-sites', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-sites', str(max(1, max_site_refreshes)), '--plan-only',
        ]
        extend_adapter_args(command, requested_adapters)
        for site in selected_sites:
            if site.get('slug'):
                command += ['--slug', site['slug']]
        return {
            'decision': 'refresh-sites',
            'reason': f"na deze stap blijven waarschijnlijk nog {len(remaining_stale_generic_sites)} beheerde niet-Proton site-probe(s) stale of zonder verse artifacts",
            'action': run_capture(command, timeout=20),
            'target_summary': summarize_targets(selected_sites),
            'predicted': True,
        }

    return None


def run_action_sequence(initial_decision, max_actions, max_site_refreshes, stale_after, site_timeout, apply_prune=False):
    steps = []
    decision = initial_decision

    for _ in range(max(1, max_actions)):
        command = decision.get('command')
        if not command:
            break

        action = run_capture(command, timeout=decision.get('command_timeout', 300))
        step = {
            'decision': decision.get('route'),
            'reason': decision.get('reason'),
            'action': action,
            'sites': decision.get('sites') or {},
            'terminal_sites': decision.get('terminal_sites') or [],
            'proton_next': decision.get('proton_next') or {},
            'desktop': decision.get('desktop') or {},
            'prune': decision.get('prune') or {},
        }
        steps.append(step)

        if decision.get('route') not in MULTI_STEP_ROUTES:
            break
        if not action_made_progress(decision.get('route'), action):
            break

        next_decision = decide(max_site_refreshes, stale_after, site_timeout, apply_prune=apply_prune, adapter_filter=initial_decision.get('requested_adapters'))
        if not next_decision.get('command'):
            steps.append({
                'decision': next_decision.get('route'),
                'reason': next_decision.get('reason'),
                'action': None,
                'sites': next_decision.get('sites') or {},
                'terminal_sites': next_decision.get('terminal_sites') or [],
                'proton_next': next_decision.get('proton_next') or {},
                'desktop': next_decision.get('desktop') or {},
                'prune': next_decision.get('prune') or {},
            })
            break
        decision = next_decision

    return steps


def predict_plan_follow_up(initial_decision, stale_after, site_timeout, apply_prune=False, max_site_refreshes=2):
    route = initial_decision.get('route')
    requested_adapters = initial_decision.get('requested_adapters') or []
    desktop = initial_decision.get('desktop') or {}
    sites = initial_decision.get('sites') or {}
    prune = initial_decision.get('prune') or {}
    proton_next = initial_decision.get('proton_next') or {}
    site_by_slug = {
        str(site.get('slug') or '').strip().lower(): site
        for site in (sites.get('sites') or [])
        if str(site.get('slug') or '').strip()
    }
    blocking_desktop_actions = []
    for action in (desktop.get('configured_recommended_actions') or []):
        slug = str(action.get('slug') or '').strip().lower()
        site = site_by_slug.get(slug)
        if not site:
            blocking_desktop_actions.append(action)
            continue
        if site.get('workflow_terminal'):
            continue
        if not site.get('dom_healthy'):
            blocking_desktop_actions.append(action)

    handled_slugs = set(extract_handled_slugs(initial_decision.get('command') or []))
    stale_generic_sites = [
        site for site in (sites.get('sites') or [])
        if site.get('configured') and site.get('adapter') != 'proton' and site.get('attention_needed', site.get('stale'))
    ]
    remaining_stale_generic_sites = [
        site for site in stale_generic_sites
        if str(site.get('slug') or '').strip().lower() not in handled_slugs
    ]
    remaining_blocking_desktop_actions = [
        action for action in blocking_desktop_actions
        if str(action.get('slug') or '').strip().lower() not in handled_slugs
    ]

    remaining_refresh = build_remaining_refresh_decision(
        route,
        remaining_stale_generic_sites,
        requested_adapters,
        stale_after,
        site_timeout,
        max_site_refreshes,
    )
    if remaining_refresh:
        remaining_refresh.update({
            'sites': sites,
            'terminal_sites': initial_decision.get('terminal_sites') or [],
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
        })
        return remaining_refresh

    if route == 'refresh-sites' and blocking_desktop_actions:
        first = blocking_desktop_actions[0]
        command = [
            'python3', str(DISPATCH), 'refresh-desktop', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-targets', '1', '--timeout', str(max(60, site_timeout)), '--plan-only',
        ]
        extend_adapter_args(command, requested_adapters)
        if first.get('slug'):
            command += ['--slug', str(first['slug'])]
        return {
            'decision': 'refresh-desktop',
            'reason': f"na een succesvolle site-refresh blijft er waarschijnlijk nog {len(blocking_desktop_actions)} desktop fallback target(s) over die nog geen bruikbare verse fallback naast een niet-gezonde DOM probe hebben",
            'action': run_capture(command, timeout=20),
            'target_summary': summarize_targets([first]),
            'sites': sites,
            'terminal_sites': initial_decision.get('terminal_sites') or [],
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
            'predicted': True,
        }

    if route == 'refresh-stack' and remaining_blocking_desktop_actions:
        first = remaining_blocking_desktop_actions[0]
        command = [
            'python3', str(DISPATCH), 'refresh-desktop', '--json', '--configured-only',
            '--stale-after', str(stale_after), '--max-targets', '1', '--timeout', str(max(60, site_timeout)), '--plan-only',
        ]
        extend_adapter_args(command, requested_adapters)
        if first.get('slug'):
            command += ['--slug', str(first['slug'])]
        return {
            'decision': 'refresh-desktop',
            'reason': f"na een succesvolle stack-refresh blijven waarschijnlijk nog {len(remaining_blocking_desktop_actions)} andere desktop fallback target(s) over die nog geen bruikbare verse fallback naast een niet-gezonde DOM probe hebben",
            'action': run_capture(command, timeout=20),
            'target_summary': summarize_targets([first]),
            'sites': sites,
            'terminal_sites': initial_decision.get('terminal_sites') or [],
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
            'predicted': True,
        }

    if route in {'refresh-stack', 'refresh-sites', 'refresh-desktop', 'desktop-probe'} and prune.get('candidate_count') and sites.get('operationally_healthy') and not blocking_desktop_actions:
        command = ['python3', str(PRUNE_UNMANAGED), '--json', '--stale-after', str(stale_after)]
        extend_adapter_args(command, requested_adapters)
        predicted_route = 'prune-unmanaged-review'
        reason = f"als beheerde observability daarna gezond is, blijven nog {prune.get('candidate_count')} onbeheerde stale artifact(s)/outdir(s) over"
        if apply_prune:
            command.append('--apply')
            predicted_route = 'prune-unmanaged'
            reason = f"als beheerde observability daarna gezond is, kunnen nog {prune.get('candidate_count')} onbeheerde stale artifact(s)/outdir(s) veilig naar Trash"
        return {
            'decision': predicted_route,
            'reason': reason,
            'action': run_capture(command, timeout=20),
            'sites': sites,
            'terminal_sites': initial_decision.get('terminal_sites') or [],
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
            'predicted': True,
        }

    proton_route = proton_next.get('recommended_route')
    if route in {'refresh-stack', 'refresh-sites', 'refresh-desktop', 'desktop-probe'} and proton_route in SAFE_PROTON_ROUTES:
        command = ['python3', str(DISPATCH), 'proton-autopilot-safe', '--json', '--max-steps', '2']
        return {
            'decision': 'proton-autopilot-safe',
            'reason': f"als de onderhoudsstap slaagt, is daarna waarschijnlijk weer een veilige Proton vervolgstap beschikbaar: {proton_next.get('reason') or proton_route}",
            'action': {'command': command, 'ok': True, 'returncode': 0, 'stdout': '', 'stderr': '', 'result': None, 'planned_only': True},
            'sites': sites,
            'terminal_sites': initial_decision.get('terminal_sites') or [],
            'proton_next': proton_next,
            'desktop': desktop,
            'prune': prune,
            'predicted': True,
        }

    return None


def render_text(summary):
    lines = ['Web automation autopilot']
    if summary.get('requested_adapters'):
        lines.append(f"- adapters={', '.join(summary.get('requested_adapters') or [])}")
    lines.append(f"- decision={summary.get('decision')}, reason={summary.get('reason')}")
    target_summary = summary.get('target_summary') or {}
    if target_summary.get('preview'):
        lines.append(f"- targets={', '.join(target_summary.get('preview') or [])}")
    action = summary.get('action') or {}
    if action.get('command'):
        lines.append(f"- command={' '.join(action.get('command') or [])}")
    if action.get('planned_only') and action.get('plan_command'):
        lines.append(f"- plan_command={' '.join(action.get('plan_command') or [])}")
    result = action.get('result') or {}
    if summary.get('decision') == 'refresh-stack':
        lines.append(
            f"- stack sites={result.get('site_candidate_count', 0)} (ok={result.get('site_success_count', 0)}, refreshed={result.get('site_refreshed_count', 0)}), desktop={result.get('desktop_candidate_count', 0)} (ok={result.get('desktop_success_count', 0)}, refreshed={result.get('desktop_refreshed_count', 0)})"
        )
    elif summary.get('decision') == 'refresh-sites':
        lines.append(
            f"- refreshed={result.get('refreshed_count', 0)}, ok={result.get('success_count', 0)}, failed={result.get('failure_count', 0)}"
        )
    elif summary.get('decision') == 'refresh-desktop':
        lines.append(
            f"- desktop refreshed={result.get('refreshed_count', 0)}, ok={result.get('success_count', 0)}, failed={result.get('failure_count', 0)}"
        )
    elif summary.get('decision') == 'desktop-probe':
        lines.append(f"- desktop refresh ok={action.get('ok')} rc={action.get('returncode')}")
    elif summary.get('decision') == 'proton-autopilot-safe':
        lines.append(
            f"- before={result.get('before_route')}, after={result.get('after_route')}, advanced={result.get('advanced')}"
        )
    elif summary.get('decision') == 'prune-unmanaged-review':
        lines.append(
            f"- prune-candidates={result.get('candidate_count', 0)}, site-artifacts={result.get('site_count', 0)}, desktop-outdirs={result.get('desktop_outdir_count', 0)}"
        )
    elif summary.get('decision') == 'prune-unmanaged':
        trashed = sum(1 for item in (result.get('results') or []) if item.get('ok'))
        lines.append(
            f"- trashed={trashed}/{len(result.get('results') or [])}, remaining-candidates={result.get('candidate_count', 0)}"
        )
    terminal_sites = summary.get('terminal_sites') or []
    if terminal_sites:
        lines.append(f"- manual_boundary={len(terminal_sites)}")
    extra_steps = summary.get('steps') or []
    if extra_steps:
        lines.append(f"- extra_steps={len(extra_steps)}")
        for index, step in enumerate(extra_steps, start=2):
            step_action = step.get('action') or {}
            step_result = step_action.get('result') or {}
            lines.append(f"- step{index}={step.get('decision')}, reason={step.get('reason')}")
            if step_action.get('command'):
                lines.append(f"- step{index}_command={' '.join(step_action.get('command') or [])}")
            if step.get('decision') == 'refresh-stack':
                lines.append(
                    f"- step{index}_stack_sites={step_result.get('site_candidate_count', 0)} (ok={step_result.get('site_success_count', 0)}, refreshed={step_result.get('site_refreshed_count', 0)}), desktop={step_result.get('desktop_candidate_count', 0)} (ok={step_result.get('desktop_success_count', 0)}, refreshed={step_result.get('desktop_refreshed_count', 0)})"
                )
            elif step.get('decision') == 'refresh-sites':
                lines.append(
                    f"- step{index}_refreshed={step_result.get('refreshed_count', 0)}, ok={step_result.get('success_count', 0)}, failed={step_result.get('failure_count', 0)}"
                )
            elif step.get('decision') == 'refresh-desktop':
                lines.append(
                    f"- step{index}_desktop_refreshed={step_result.get('refreshed_count', 0)}, ok={step_result.get('success_count', 0)}, failed={step_result.get('failure_count', 0)}"
                )
            elif step.get('decision') == 'prune-unmanaged':
                trashed = sum(1 for item in (step_result.get('results') or []) if item.get('ok'))
                lines.append(
                    f"- step{index}_trashed={trashed}/{len(step_result.get('results') or [])}, remaining-candidates={step_result.get('candidate_count', 0)}"
                )
            elif step.get('decision') == 'prune-unmanaged-review':
                lines.append(
                    f"- step{index}_prune-candidates={step_result.get('candidate_count', 0)}, site-artifacts={step_result.get('site_count', 0)}, desktop-outdirs={step_result.get('desktop_outdir_count', 0)}"
                )
            elif step_action.get('stderr'):
                lines.append(f"- step{index}_stderr={step_action.get('stderr')[:220]}")
    follow_up = summary.get('follow_up') or {}
    if follow_up:
        predicted = ' (verwacht)' if follow_up.get('predicted') else ''
        lines.append(f"- follow_up={follow_up.get('decision')}{predicted}, reason={follow_up.get('reason')}")
        follow_up_targets = follow_up.get('target_summary') or {}
        if follow_up_targets.get('preview'):
            lines.append(f"- follow_up_targets={', '.join(follow_up_targets.get('preview') or [])}")
        follow_up_action = follow_up.get('action') or {}
        follow_up_result = follow_up_action.get('result') or {}
        if follow_up_action.get('command'):
            lines.append(f"- follow_up_command={' '.join(follow_up_action.get('command') or [])}")
        if follow_up.get('decision') == 'refresh-stack':
            lines.append(
                f"- stack sites={follow_up_result.get('site_candidate_count', 0)} (ok={follow_up_result.get('site_success_count', 0)}, refreshed={follow_up_result.get('site_refreshed_count', 0)}), desktop={follow_up_result.get('desktop_candidate_count', 0)} (ok={follow_up_result.get('desktop_success_count', 0)}, refreshed={follow_up_result.get('desktop_refreshed_count', 0)})"
            )
        elif follow_up.get('decision') == 'refresh-desktop':
            lines.append(
                f"- desktop refreshed={follow_up_result.get('refreshed_count', 0)}, ok={follow_up_result.get('success_count', 0)}, failed={follow_up_result.get('failure_count', 0)}"
            )
        elif follow_up.get('decision') == 'desktop-probe':
            lines.append(
                f"- desktop refresh ok={follow_up_action.get('ok')} rc={follow_up_action.get('returncode')}"
            )
        elif follow_up.get('decision') == 'proton-autopilot-safe':
            lines.append(
                f"- proton before={follow_up_result.get('before_route')}, after={follow_up_result.get('after_route')}, advanced={follow_up_result.get('advanced')}"
            )
        elif follow_up.get('decision') == 'prune-unmanaged-review':
            lines.append(
                f"- prune-candidates={follow_up_result.get('candidate_count', 0)}, site-artifacts={follow_up_result.get('site_count', 0)}, desktop-outdirs={follow_up_result.get('desktop_outdir_count', 0)}"
            )
        elif follow_up.get('decision') == 'prune-unmanaged':
            trashed = sum(1 for item in (follow_up_result.get('results') or []) if item.get('ok'))
            lines.append(
                f"- trashed={trashed}/{len(follow_up_result.get('results') or [])}, remaining-candidates={follow_up_result.get('candidate_count', 0)}"
            )
        if follow_up_action.get('stderr'):
            lines.append(f"- follow_up_stderr={follow_up_action.get('stderr')[:220]}")
    if action.get('stderr'):
        lines.append(f"- stderr={action.get('stderr')[:220]}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Veilige autopilot voor web automation onderhoud en volgende stappen')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--max-site-refreshes', type=int, default=2)
    parser.add_argument('--max-actions', type=int, default=2, help='voer maximaal dit aantal opeenvolgende onderhoudsacties uit als elke stap echt voortgang maakt')
    parser.add_argument('--stale-after', type=int, default=900)
    parser.add_argument('--site-timeout', type=int, default=90)
    parser.add_argument('--apply-prune', action='store_true', help='trash stale onbeheerde artifacts/outdirs automatisch zodra beheerde targets operationeel gezond zijn')
    parser.add_argument('--plan-only', action='store_true', help='bepaal alleen de volgende stap, zonder iets uit te voeren')
    parser.add_argument('--adapter', action='append', help='beperk autopilot tot één adapter (herhaalbaar)')
    args = parser.parse_args()

    decision = decide(args.max_site_refreshes, args.stale_after, args.site_timeout, apply_prune=args.apply_prune, adapter_filter=args.adapter)
    action = {'command': decision.get('command'), 'ok': True, 'returncode': 0, 'stdout': '', 'stderr': '', 'result': None}
    if args.plan_only:
        plan_command = list(decision.get('command') or [])
        route = decision.get('route')
        should_run_plan_command = bool(plan_command)
        if route in PLAN_ONLY_APPEND_ROUTES:
            if '--plan-only' not in plan_command:
                plan_command.append('--plan-only')
        elif route == 'prune-unmanaged':
            plan_command = [part for part in plan_command if part != '--apply']
        elif route in {'desktop-probe', 'proton-autopilot-safe'}:
            should_run_plan_command = False

        if should_run_plan_command and plan_command:
            action = run_capture(plan_command, timeout=min(decision.get('command_timeout', 300), 30))
            action['command'] = decision.get('command')
            action['plan_command'] = plan_command
            action['planned_only'] = True
        else:
            action = {'command': decision.get('command'), 'ok': True, 'returncode': 0, 'stdout': '', 'stderr': '', 'result': None, 'planned_only': True}
            if plan_command and plan_command != decision.get('command'):
                action['plan_command'] = plan_command
    elif decision.get('command'):
        action = run_capture(decision['command'], timeout=decision.get('command_timeout', 300))

    steps = []
    follow_up = None
    if args.plan_only:
        follow_up = predict_plan_follow_up(decision, args.stale_after, args.site_timeout, apply_prune=args.apply_prune, max_site_refreshes=args.max_site_refreshes)
        ok = action.get('ok', True)
        if follow_up and follow_up.get('action'):
            ok = ok and follow_up['action'].get('ok', True)
    else:
        sequence = run_action_sequence(decision, args.max_actions, args.max_site_refreshes, args.stale_after, args.site_timeout, apply_prune=args.apply_prune)
        if sequence:
            first = sequence[0]
            action = first.get('action') or action
            steps = sequence[1:]
        ok = all((step.get('action') or {'ok': True}).get('ok', True) for step in sequence if step.get('action') is not None)
        if not sequence:
            ok = action.get('ok', True)

    final_state = None
    if steps:
        final_state = steps[-1]
    elif follow_up:
        final_state = follow_up

    summary = {
        'decision': decision.get('route'),
        'reason': decision.get('reason'),
        'target_summary': decision.get('target_summary') or {},
        'action': action,
        'steps': steps,
        'follow_up': follow_up,
        'sites': (final_state or {}).get('sites') or decision.get('sites') or {},
        'terminal_sites': (final_state or {}).get('terminal_sites') or decision.get('terminal_sites') or [],
        'proton_next': (final_state or {}).get('proton_next') or decision.get('proton_next') or {},
        'desktop': (final_state or {}).get('desktop') or decision.get('desktop') or {},
        'prune': (final_state or {}).get('prune') or decision.get('prune') or {},
        'requested_adapters': decision.get('requested_adapters') or [],
        'planned_only': args.plan_only,
        'ok': ok,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))

    raise SystemExit(0 if summary.get('ok') else 1)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        if '--json' in sys.argv[1:]:
            print(json.dumps({
                'decision': 'error',
                'reason': str(exc) or exc.__class__.__name__,
                'ok': False,
                'error_type': exc.__class__.__name__,
                'traceback': traceback.format_exc(),
            }, ensure_ascii=False, indent=2))
            raise SystemExit(1)
        raise
