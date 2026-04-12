#!/usr/bin/env python3
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mail_heuristics import (
    format_attachment_hint,
    format_cluster_hint,
    format_next_step_alternative_commands,
    format_next_step_candidate_hint,
    format_security_alert_hint,
    format_stale_attention_hint,
)

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUSBOARD = ROOT / 'scripts' / 'statusboard.py'
TOOLSBOARD = ROOT / 'scripts' / 'toolsboard.py'
AUTOMATIONBOARD = ROOT / 'scripts' / 'automation-board.py'


def run_json(command, default=None, timeout=25):
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return default, f'command timed out: {command}'
    if proc.returncode != 0:
        return default, (proc.stderr.strip() or proc.stdout.strip() or f'command failed: {command}')
    try:
        return json.loads(proc.stdout), None
    except Exception as exc:
        return default, f'invalid json for {command}: {exc}'


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


def mail_board_from_status(status_summary):
    mail = (status_summary or {}).get('mail') or {}
    recent_mail = (status_summary or {}).get('recent_mail') or []
    recent_mail_current = (status_summary or {}).get('recent_mail_current') or []
    recent_threads = (status_summary or {}).get('recent_threads') or []
    recent_threads_current = (status_summary or {}).get('recent_threads_current') or []
    mail_triage = (status_summary or {}).get('mail_triage') or {}
    mail_focus = (status_summary or {}).get('mail_focus') or {}
    mail_high_recent = (status_summary or {}).get('mail_high_recent') or {}
    mail_next_step = (status_summary or {}).get('mail_next_step') or {}

    recent_high_count = mail_high_recent.get('total_count', mail_high_recent.get('count', 0)) if mail_high_recent.get('items') else 0
    recent_attention_now_count = mail_high_recent.get('total_attention_now_count', mail_high_recent.get('attention_now_count', 0)) if mail_high_recent.get('items') else 0
    recent_stale_high_count = mail_high_recent.get('total_stale_attention_count', mail_high_recent.get('stale_attention_count', 0)) if mail_high_recent.get('items') else 0

    return {
        'new_count': 0,
        'unread_count': 0,
        'draft_count': 0,
        'latest_thread_count': len(recent_threads),
        'recent_high_count': recent_high_count,
        'recent_attention_now_count': recent_attention_now_count,
        'recent_stale_high_count': recent_stale_high_count,
        'triage_high_group_count': mail_high_recent.get('total_related_group_count', mail_high_recent.get('related_group_count', 0)),
        'triage_high_groups': mail_high_recent.get('top_related_groups', []),
        'triage_high_scope': mail_high_recent.get('scope', 'latest+high'),
        'latest_meaningful': recent_mail,
        'latest_current': recent_mail_current,
        'latest_threads': recent_threads,
        'latest_threads_current': recent_threads_current,
        'unread': [],
        'focus_scope': mail_focus.get('scope', 'unread'),
        'focus': mail_focus.get('focus'),
        'focus_burst_count': mail_focus.get('focus_burst_count', 0),
        'focus_related_burst_count': mail_focus.get('focus_related_burst_count', 0),
        'focus_draft': mail_focus.get('draft'),
        'focus_fallback_thread': mail_focus.get('fallback_thread'),
        'focus_skipped_ephemeral_count': mail_focus.get('skipped_ephemeral_count', 0),
        'next_step': mail_next_step,
        'account': mail.get('account', 'onbekend'),
        'host': mail.get('host', 'onbekend'),
        'last_uid': mail.get('last_uid', 0),
        'tracked_notifications': mail.get('tracked_notifications', 0),
        'triage': mail_triage.get('items', []),
        'errors': {},
    }


def build_board(limit=5, tool_section=None):
    tools_cmd = ['python3', str(TOOLSBOARD), '--json']
    if tool_section:
        tools_cmd += ['--section', tool_section]

    jobs = {
        'status': (['python3', str(STATUSBOARD), '--json'], {}, 40),
        'automation': (['python3', str(AUTOMATIONBOARD), '--json'], {}, 30),
        'tools': (tools_cmd, {}, 10),
    }

    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        futures = {
            name: pool.submit(run_json, command, default=default, timeout=timeout)
            for name, (command, default, timeout) in jobs.items()
        }
        results = {name: future.result() for name, future in futures.items()}

    status, status_error = results['status']
    automation, automation_error = results['automation']
    tools, tools_error = results['tools']

    security = (status or {}).get('security') or {}
    tasks = (status or {}).get('task_audit') or {}

    return {
        'status': status or {},
        'mail': mail_board_from_status(status),
        'security': security,
        'tasks': tasks,
        'tools': tools or {},
        'automation': automation or {},
        'errors': {k: v for k, v in {
            'status': status_error,
            'automation': automation_error,
            'tools': tools_error,
        }.items() if v},
    }


def render_text(board):
    status_summary = board.get('status') or {}
    status = status_summary.get('status') or {
        'version': 'onbekend',
        'gateway': {'text': 'onbekend'},
        'tasks': {'active': 0, 'lost': 0},
    }
    mail = board.get('mail') or {}
    security = board.get('security') or {}
    tasks = board.get('tasks') or {}
    tool_sections = list((board.get('tools') or {}).keys())
    automation = board.get('automation', {})

    lines = ['Command board']
    lines.append(
        f"- status: OpenClaw {status.get('version', 'onbekend')}, gateway {(status.get('gateway') or {}).get('text', 'onbekend')}, taken {(status.get('tasks') or {}).get('active', 0)} actief/{(status.get('tasks') or {}).get('lost', 0)} vermist"
    )
    recent_high = mail.get('recent_high_count', 0)
    recent_high_groups = mail.get('triage_high_group_count', 0)
    recent_attention_now = mail.get('recent_attention_now_count', 0)
    recent_stale_high = mail.get('recent_stale_high_count', 0)
    recent_high_suffix = ''
    if recent_high and recent_high_groups:
        recent_high_suffix = f" in {recent_high_groups} cluster(s)"
    if recent_high and mail.get('triage_high_scope') != 'unread+high':
        recent_high_detail = f', actueel {recent_attention_now}, niet actueel {recent_stale_high}'
        if recent_attention_now == 0:
            recent_high_detail += ', alles niet actueel'
        mail_summary = (
            f"- mail: nieuw {mail.get('new_count', 0)}, unread {mail.get('unread_count', 0)}, drafts {mail.get('draft_count', 0)}, "
            f"threads {mail.get('latest_thread_count', 0)}, hoog recent {recent_high}{recent_high_suffix}{recent_high_detail}"
        )
    else:
        mail_summary = (
            f"- mail: nieuw {mail.get('new_count', 0)}, unread {mail.get('unread_count', 0)}, drafts {mail.get('draft_count', 0)}, "
            f"threads {mail.get('latest_thread_count', 0)}"
        )
    lines.append(mail_summary)
    triage_high_groups = mail.get('triage_high_groups') or []
    if triage_high_groups:
        group_bits = [format_cluster_hint(group, include_age=True) for group in triage_high_groups[:2]]
        remaining = max(0, len(triage_high_groups) - len(group_bits))
        suffix = f" +{remaining} cluster(s)" if remaining else ''
        lines.append(f"- hoge mailclusters: {'; '.join(group_bits)}{suffix}")
    if mail.get('unread'):
        first = mail['unread'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        lines.append(f"- bovenste unread: {first['from']} — {first['subject']}{format_attachment_hint(first)}{age}")
    elif mail.get('latest_current'):
        first = mail['latest_current'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        lines.append(f"- actuele betekenisvolle mail: {first['from']} — {first['subject']}{format_attachment_hint(first)}{format_security_alert_hint(first)}{age}{format_stale_attention_hint(first)}")
    elif mail.get('latest_meaningful'):
        first = mail['latest_meaningful'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        lines.append(f"- laatste betekenisvolle mail: {first['from']} — {first['subject']}{format_attachment_hint(first)}{format_security_alert_hint(first)}{age}{format_stale_attention_hint(first)}")
    elif mail.get('latest'):
        first = mail['latest'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        lines.append(f"- laatste mail: {first['from']} — {first['subject']}{format_attachment_hint(first)}{age}{format_stale_attention_hint(first)}")
    mail_threads = mail.get('latest_threads_current') or mail.get('latest_threads') or []
    if mail_threads:
        thread = mail_threads[0]
        stale = ' [niet actueel]' if thread.get('stale_attention') else ''
        thread_label = 'mail thread' if not thread.get('stale_attention') else 'laatste mailthread'
        variant_suffix = f", +{thread.get('subject_variant_count', 0) - 1} variant(en)" if (thread.get('subject_variant_count', 0) or 0) > 1 else ''
        time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
        time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
        lines.append(
            f"- {thread_label}: {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{variant_suffix}, laatste {thread.get('latest_from', 'onbekend')}{time_suffix}){format_attachment_hint(thread)}{format_security_alert_hint(thread)}{stale}"
        )
    focus = mail.get('focus') or {}
    if focus:
        suffix = ' ↩' if focus.get('reply_needed') else ''
        deadline = f" ⏰{focus.get('deadline_hint')}" if focus.get('deadline_hint') else ''
        draft_flag = ' + concept' if mail.get('focus_draft') else ''
        age = f" ({focus.get('age_hint')})" if focus.get('age_hint') else ''
        related_burst = mail.get('focus_related_burst_count', 0)
        exact_burst = mail.get('focus_burst_count', 0)
        burst = max(related_burst, exact_burst)
        burst_label = 'verwant' if related_burst > exact_burst else 'soortgelijk'
        burst_suffix = f" ({burst}x {burst_label})" if burst > 1 else ''
        focus_line = (
            f"- mail focus: {focus.get('from', 'onbekend')} — {focus.get('subject', '(geen onderwerp)')}{format_attachment_hint(focus)}{format_security_alert_hint(focus)} [{focus.get('action_hint', 'ter info')}{suffix}]{deadline} ({mail.get('focus_scope', 'mail')}){draft_flag}{burst_suffix}{age}"
        )
        if focus.get('stale_attention'):
            focus_line = (
                f"- geen actuele focus, laatste kandidaat was: {focus.get('from', 'onbekend')} — {focus.get('subject', '(geen onderwerp)')}{format_attachment_hint(focus)}{format_security_alert_hint(focus)} [{focus.get('action_hint', 'ter info')}{suffix}]{deadline}{draft_flag}{burst_suffix}{age} [niet actueel]"
            )
        lines.append(focus_line)
    elif mail.get('focus_fallback_thread'):
        thread = mail.get('focus_fallback_thread') or {}
        participants = ', '.join((thread.get('participants') or [])[:2]) or thread.get('latest_from', 'onbekend')
        extra_people = max(0, len(thread.get('participants') or []) - 2)
        if extra_people:
            participants += f' (+{extra_people})'
        skipped = mail.get('focus_skipped_ephemeral_count', 0)
        time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
        time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
        stale = ' [niet actueel]' if thread.get('stale_attention') else ''
        suffix = f", code-noise overgeslagen: {skipped}" if skipped else ''
        label = 'geen actuele focus, laatste betekenisvolle thread' if thread.get('stale_attention') else 'mail focus fallback'
        lines.append(
            f"- {label}: {participants} — {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{time_suffix}){format_attachment_hint(thread)}{suffix}{stale}"
        )
    next_step = mail.get('next_step') or {}
    selected = next_step.get('selected_group') or {}
    if next_step.get('recommended_route') and next_step.get('recommended_route') != 'noop' and selected:
        review_only = bool(next_step.get('review_only'))
        label = 'mail review' if review_only or selected.get('stale_attention') else 'mail next'
        lines.append(
            f"- {label}: {format_next_step_candidate_hint(selected, include_age=True)}"
            + (' + concept' if next_step.get('selected_draft') else '')
        )
        candidates = next_step.get('candidates') or []
        alternative_candidates = candidates[1:3] if len(candidates) > 1 else []
        if alternative_candidates:
            preview = '; '.join(format_next_step_candidate_hint(candidate, include_age=True) for candidate in alternative_candidates)
            remaining = max(0, len(candidates) - 1 - len(alternative_candidates))
            suffix = f" +{remaining} meer" if remaining else ''
            lines.append(f"- mail queue: {preview}{suffix}")
            command_preview = format_next_step_alternative_commands(alternative_candidates, limit=len(alternative_candidates))
            if command_preview:
                lines.append(f"- mail queue commands: {command_preview}")
        if next_step.get('recommended_command'):
            command_label = 'mail review command' if review_only or selected.get('stale_attention') else 'mail next command'
            lines.append(f"- {command_label}: {next_step.get('recommended_command')}")
    lines.append(
        f"- security/tasks: {security.get('text', 'onbekend')}, task-audit {tasks.get('errors', 0)} errors / {tasks.get('warnings', 0)} warns"
    )
    artifacts = automation.get('artifacts') or {}
    sites = automation.get('sites') or {}
    desktop = automation.get('desktop') or {}
    autopilot = automation.get('autopilot') or {}
    stack_focus = automation.get('stack_focus') or {}
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
    lines.append(
        f"- automation: {automation.get('route_count', len(automation.get('routes', [])))} routes, artifacts {artifacts.get('artifact_count', 0)}, sites {sites.get('site_count', 0)}"
    )
    if artifacts:
        configured_stale_artifacts = artifacts.get('configured_stale_artifact_count', 0)
        unmanaged_stale_artifacts = artifacts.get('unmanaged_stale_artifact_count', 0)
        lines.append(
            f"- artifact health: stale={artifacts.get('stale_artifact_count', 0)} (configured {configured_stale_artifacts}, unmanaged {unmanaged_stale_artifacts}), healthy={artifacts.get('healthy', False)}, operational={artifacts.get('operationally_healthy', artifacts.get('configured_healthy', False))}, adapters={artifacts.get('adapter_count', 0)}, freshest={artifacts.get('freshest_age_human', 'onbekend')}, stalest={artifacts.get('stalest_age_human', 'onbekend')}"
        )
        prune = automation.get('prune') or {}
        prune_count = prune.get('candidate_count', 0)
        prune_targets = prune.get('target_count', 0)
        prune_target_preview = format_target_preview(prune.get('targets'))
        if unmanaged_stale_artifacts and not configured_stale_artifacts:
            lines.append('- artifact nuance: alleen onbeheerde demo-artifacts zijn stale, beheerde automation-artifacts zijn operationeel gezond')
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
    if sites:
        configured_stale = sites.get('configured_stale_site_count', 0)
        unmanaged_stale = sites.get('unmanaged_stale_site_count', 0)
        lines.append(
            f"- site health: stale={sites.get('stale_site_count', 0)} (configured {configured_stale}, unmanaged {unmanaged_stale}), healthy={sites.get('healthy', False)}, operational={sites.get('operationally_healthy', sites.get('configured_healthy', False))}"
        )
        adapter_summaries = sites.get('adapter_summaries') or []
        adapter_preview_items = [
            f"{item.get('adapter')}:{item.get('site_count')}"
            + (f" stale={item.get('stale_site_count')}" if item.get('stale_site_count') else '')
            + (f" cfg={item.get('configured_stale_site_count')}" if item.get('configured_stale_site_count') else '')
            + (f" -> {item.get('next_attention_slug')}" if item.get('next_attention_slug') else '')
            for item in adapter_summaries[:4]
        ]
        if len(adapter_summaries) > 4:
            adapter_preview_items.append(f"+{len(adapter_summaries) - 4} meer")
        adapter_health = ', '.join(adapter_preview_items)
        if adapter_health:
            lines.append(f"- site adapters: {adapter_health}")
        first_adapter_attention = next((item for item in (sites.get('adapter_summaries') or []) if item.get('next_attention_command')), None)
        configured_stale_site = next(
            (
                item for item in (sites.get('sites') or [])
                if item.get('attention_needed', item.get('stale')) and item.get('configured') and item.get('recommended_command')
            ),
            None,
        )
        if first_adapter_attention and (
            not configured_stale_site or first_adapter_attention.get('next_attention_command') != configured_stale_site.get('recommended_command')
        ):
            lines.append(f"- site adapter refresh: {first_adapter_attention.get('adapter')} -> {first_adapter_attention.get('next_attention_command')}")
        if unmanaged_stale and not configured_stale:
            lines.append('- site nuance: alleen onbeheerde demo-probes zijn stale, beheerde sites zijn operationeel gezond')
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
    stack_overview = automation.get('stack_overview') or {}
    queue_candidates = [
        item for item in (stack_overview.get('stacks') or [])
        if (item.get('workflow') or {}).get('terminal') or item.get('attention_needed')
    ]
    if not queue_candidates:
        queue_candidates = stack_overview.get('stacks') or []
    stack_queue_preview = format_stack_queue_items(queue_candidates)
    if stack_queue_preview:
        lines.append(f"- stack queue: {stack_queue_preview}")
    focus_items = stack_focus.get('stacks') or []
    if focus_items:
        focus = focus_items[0]
        focus_dom = focus.get('dom') or {}
        focus_desktop = focus.get('desktop') or {}
        focus_workflow = focus.get('workflow') or {}
        if focus_workflow.get('terminal'):
            lines.append(
                f"- stack focus: {focus.get('slug')} [{focus.get('status')}] workflow={focus_workflow.get('state') or '-'}"
            )
            lines.append(
                f"- stack observability: dom={focus_dom.get('age_human')} desktop="
                + (focus_desktop.get('age_human') or ('uit' if not focus_desktop.get('configured') else 'unknown'))
            )
        else:
            lines.append(
                f"- stack focus: {focus.get('slug')} [{focus.get('status')}] dom={focus_dom.get('age_human')} desktop="
                + (focus_desktop.get('age_human') or ('uit' if not focus_desktop.get('configured') else 'unknown'))
                + (f", workflow={focus_workflow.get('state')}" if focus_workflow.get('state') else '')
            )
        if focus.get('recommended_command'):
            lines.append(f"- stack next: {focus.get('recommended_command')}")
    if desktop:
        lines.append(
            f"- desktop fallback: stale={desktop.get('stale_outdir_count', 0)} (configured {desktop.get('configured_attention_target_count', desktop.get('configured_stale_outdir_count', 0))}, missing {desktop.get('missing_configured_target_count', 0)}, blocking {len(desktop_blocking_actions)}, unmanaged {desktop.get('unmanaged_stale_outdir_count', 0)}), healthy={desktop.get('healthy')}, operational={effective_desktop_operational}, latest={desktop.get('display_latest_age_human', desktop.get('default_latest_age_human'))}, screenshots={desktop.get('display_screenshot_count', desktop.get('screenshot_count'))}, windows={desktop.get('display_has_windows_capture', desktop.get('default_has_windows_capture'))}"
        )
        if desktop.get('display_scope') == 'configured' and desktop.get('display_path'):
            lines.append(f"- desktop display: beheerde target {desktop.get('display_slug') or desktop.get('display_path')} als referentie")
        if desktop.get('unmanaged_stale_outdir_count') and not desktop.get('configured_attention_target_count', desktop.get('configured_stale_outdir_count', 0)):
            lines.append('- desktop nuance: alleen onbeheerde demo-desktop-artifacts zijn stale, beheerde desktop fallbacks zijn operationeel gezond')
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
        elif desktop.get('recommended_command'):
            lines.append(f"- desktop refresh: {desktop.get('recommended_command')}")
    lines.append(f"- tools-secties: {', '.join(tool_sections[:4]) or 'geen'}" + (f" (+{len(tool_sections) - 4})" if len(tool_sections) > 4 else ''))
    errors = board.get('errors') or {}
    if errors:
        lines.append(f"- deels gedegradeerd: {', '.join(sorted(errors))}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Gecombineerd command board voor status, mail, security, tasks, automation en tools')
    parser.add_argument('-n', '--limit', type=int, default=5)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--tool-section', help='filter toolsboard op sectie/tekst')
    args = parser.parse_args()

    board = build_board(limit=max(1, min(args.limit, 20)), tool_section=args.tool_section)
    if args.json:
        print(json.dumps(board, ensure_ascii=False, indent=2))
    else:
        print(render_text(board))


if __name__ == '__main__':
    main()
