#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
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
MAIL_SUMMARY = ROOT / 'scripts' / 'mail-summary.py'
MAIL_DRAFTS = ROOT / 'scripts' / 'mail-drafts.py'
MAIL_LATEST = ROOT / 'scripts' / 'mail-latest.py'
MAIL_TRIAGE = ROOT / 'scripts' / 'mail-triage.py'
MAIL_FOCUS = ROOT / 'scripts' / 'mail-focus.py'
MAIL_NEXT_STEP = ROOT / 'scripts' / 'mail-next-step.py'
MAIL_SECURITY_ALERTS = ROOT / 'scripts' / 'mail-security-alerts.py'


def quickstart_payload():
    return [
        {
            'command': 'python3 scripts/mail-dispatch.py board',
            'description': 'totaaloverzicht van mailstatus',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py board-now',
            'also': ['overview-now', 'overview-current', 'board-current'],
            'description': 'compact board met alleen actuele aandacht zonder losse flags',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py board-review',
            'also': ['overview-review', 'overview-review-worthy', 'board-review-worthy'],
            'description': 'compact board met alleen reviewwaardige mail zonder losse flags',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py latest --unread',
            'description': 'alleen ongelezen mail',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py check',
            'description': 'alleen echt nieuwe mail sinds laatste state-update',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py latest-now --threads --explain-empty',
            'also': ['latest-current'],
            'description': 'alleen actuele recente threads, met suppressed-uitleg als het leeg is',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py latest-review --threads --explain-empty',
            'also': ['latest-review-worthy'],
            'description': 'alleen reviewwaardige recente threads, met noop-uitleg als het leeg is',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py now --explain-empty',
            'description': 'alleen wat nu echt aandacht vraagt, met suppressed-uitleg als het leeg is',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py triage-now --explain-empty',
            'also': ['triage-current'],
            'description': 'actuele prioritering met suppressed-uitleg bij een lege actuele mailbox',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py triage-review --explain-empty',
            'also': ['triage-review-worthy'],
            'description': 'reviewwaardige prioritering met suppressed-uitleg bij noop',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py security-alerts-now',
            'also': ['security-now', 'security-current', 'alerts-now', 'alerts-current', 'security-alerts-current'],
            'description': 'alleen actuele security- of loginmeldingen, met noop-uitleg al ingebouwd',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py code-now',
            'also': ['code-current', 'verify-now', 'verify-current', 'otp-now', 'otp-current', 'auth-code-now', 'auth-code-current', 'codes-now', 'codes-current'],
            'description': 'alleen actuele verificatiecodes, met uitleg bij lege mailbox al ingebouwd',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py focus-now',
            'also': ['focus-current'],
            'description': 'beste actuele mail-focus zonder stale fallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py focus-review',
            'also': ['focus-review-worthy'],
            'description': 'beste reviewwaardige mail-focus zonder code-only of ruisfallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py next-step-now',
            'also': ['next-current', 'next-step-current'],
            'description': 'beste actuele vervolgstap zonder stale fallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py next-step-review',
            'also': ['next-review-worthy', 'next-step-review-worthy'],
            'description': 'beste reviewwaardige vervolgstap zonder ruisfallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py queue-now',
            'also': ['queue-current', 'worklist-now', 'worklist-current', 'todo-now', 'todo-current'],
            'description': 'korte actuele mailwerkrij zonder stale fallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py queue-review',
            'also': ['queue-review-worthy', 'worklist-review', 'worklist-review-worthy', 'todo-review', 'todo-review-worthy'],
            'description': 'korte reviewwaardige mailwerkrij zonder code-only of ruisfallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py thread-now --explain-empty',
            'also': ['thread-current'],
            'description': 'open direct alleen een actuele thread, met suppressed-uitleg bij noop',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py thread-review --explain-empty',
            'also': ['thread-review-worthy'],
            'description': 'open direct alleen een reviewwaardige thread, met suppressed-uitleg bij noop',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py open-now --explain-empty',
            'also': ['open-current', 'review-next-current'],
            'description': 'aanbevolen actuele thread meteen openen zonder stale fallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py open-review --explain-empty',
            'also': ['open-review-worthy', 'review-next-review-worthy'],
            'description': 'aanbevolen reviewwaardige thread meteen openen zonder ruisfallback',
        },
        {
            'command': 'python3 scripts/mail-dispatch.py open',
            'description': 'aanbevolen thread meteen openen',
        },
    ]


def run_json(command, default=None, timeout=20):
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
    except json.JSONDecodeError as exc:
        return default, f'invalid json for {command}: {exc}'


def build_board(limit=5, current_only=False, review_worthy_only=False):
    def latest_items(payload):
        if isinstance(payload, dict):
            return payload.get('items') or []
        return payload or []

    def latest_suppressed(payload):
        if isinstance(payload, dict):
            return payload.get('suppressed_groups') or []
        return []

    next_step_command = ['python3', str(MAIL_NEXT_STEP), '--json', '-n', '3']
    security_alerts_command = ['python3', str(MAIL_SECURITY_ALERTS), '--json', '-n', '5', '--explain-empty']
    latest_base_flags = ['--review-worthy'] if review_worthy_only else ['--meaningful']
    triage_review_flags = ['--review-worthy'] if review_worthy_only else []
    if current_only:
        next_step_command.append('--current-only')
        security_alerts_command.append('--current-only')
    if review_worthy_only:
        next_step_command.append('--review-worthy')

    jobs = {
        'latest': (['python3', str(MAIL_LATEST), '-n', str(limit), '--json'] + (['--review-worthy'] if review_worthy_only else []), [], 20),
        'latest_meaningful': (['python3', str(MAIL_LATEST), '-n', str(limit), '--json'] + latest_base_flags, [], 20),
        'latest_current': (['python3', str(MAIL_LATEST), '-n', str(limit), '--json'] + latest_base_flags + ['--current-only', '--explain-empty'], {}, 20),
        'latest_threads': (['python3', str(MAIL_LATEST), '-n', str(limit), '--json', '--threads'] + latest_base_flags, [], 20),
        'latest_threads_current': (['python3', str(MAIL_LATEST), '-n', str(limit), '--json', '--threads'] + latest_base_flags + ['--current-only', '--explain-empty'], {}, 20),
        'unread': (['python3', str(MAIL_LATEST), '-n', str(limit), '--json', '--unread'] + (['--review-worthy'] if review_worthy_only else []), [], 20),
        'summary': (['python3', str(MAIL_SUMMARY), '--json'], {}, 20),
        'drafts': (['python3', str(MAIL_DRAFTS), '--json', '--unread', '-n', str(limit)], {}, 20),
        'triage': (['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit)] + triage_review_flags, {}, 20),
        'triage_meaningful': (['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit), '--all', '--review-worthy', '--search-limit', '50'], {}, 25),
        'triage_current': (['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit), '--all', '--current-only', '--search-limit', '50'] + triage_review_flags, {}, 25),
        'triage_reply': (['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit), '--reply-only'] + triage_review_flags, {}, 20),
        'triage_high': (['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit), '--high-only'] + triage_review_flags, {}, 20),
        'triage_high_latest': (['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit), '--high-only', '--all', '--search-limit', '50'] + triage_review_flags, {}, 25),
        'focus': (['python3', str(MAIL_FOCUS), '--json', '-n', str(limit)], {}, 30),
        'next_step': (next_step_command, {}, 35),
        'security_alerts': (security_alerts_command, {}, 35),
    }

    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        futures = {
            name: pool.submit(run_json, command, default=default, timeout=timeout)
            for name, (command, default, timeout) in jobs.items()
        }
        results = {name: future.result() for name, future in futures.items()}

    latest, latest_error = results['latest']
    latest_meaningful, latest_meaningful_error = results['latest_meaningful']
    latest_current, latest_current_error = results['latest_current']
    latest_threads, latest_threads_error = results['latest_threads']
    latest_threads_current, latest_threads_current_error = results['latest_threads_current']
    unread, unread_error = results['unread']
    summary, summary_error = results['summary']
    drafts, drafts_error = results['drafts']
    triage, triage_error = results['triage']
    triage_meaningful, triage_meaningful_error = results['triage_meaningful']
    triage_current, triage_current_error = results['triage_current']
    triage_reply, triage_reply_error = results['triage_reply']
    triage_high, triage_high_error = results['triage_high']
    triage_high_latest, triage_high_latest_error = results['triage_high_latest']
    focus, focus_error = results['focus']
    next_step, next_step_error = results['next_step']
    security_alerts, security_alerts_error = results['security_alerts']

    latest = latest or []
    latest_meaningful = latest_meaningful or []
    latest_current_payload = latest_current or {}
    latest_threads = latest_threads or []
    latest_threads_current_payload = latest_threads_current or {}
    latest_current = latest_items(latest_current_payload)
    latest_threads_current = latest_items(latest_threads_current_payload)
    unread = unread or []
    summary = summary or {}
    drafts = drafts or {}
    triage = triage or {}
    triage_meaningful = triage_meaningful or {}
    triage_current = triage_current or {}
    triage_reply = triage_reply or {}
    triage_high = triage_high or {}
    triage_high_latest = triage_high_latest or {}
    focus = focus or {}
    next_step = next_step or {}
    security_alerts = security_alerts or {}

    effective_triage_high = triage_high
    effective_triage_high_scope = triage_high.get('scope', 'unread+high')
    if not effective_triage_high.get('items') and not unread and (triage_high_latest.get('items') or []):
        effective_triage_high = triage_high_latest
        effective_triage_high_scope = triage_high_latest.get('scope', 'latest+high')

    if review_worthy_only:
        unread = [item for item in unread if item.get('review_worthy')]
        drafts = {
            **drafts,
            'drafts': [draft for draft in (drafts.get('drafts') or []) if draft.get('review_worthy')],
            'draft_count': sum(1 for draft in (drafts.get('drafts') or []) if draft.get('review_worthy')),
        }

    if current_only:
        latest = []
        latest_meaningful = []
        latest_threads = []
        unread = [item for item in unread if item.get('attention_now') and not item.get('stale_attention')]
        unread_uids = {item.get('uid') for item in unread if item.get('uid') is not None}
        drafts = {
            **drafts,
            'drafts': [draft for draft in (drafts.get('drafts') or []) if draft.get('uid') in unread_uids],
            'draft_count': sum(1 for draft in (drafts.get('drafts') or []) if draft.get('uid') in unread_uids),
        }
        triage = {}
        if effective_triage_high.get('items'):
            current_high_items = [item for item in (effective_triage_high.get('items') or []) if item.get('attention_now') and not item.get('stale_attention')]
            effective_triage_high = dict(effective_triage_high)
            effective_triage_high['items'] = current_high_items
            effective_triage_high['count'] = len(current_high_items)
            effective_triage_high['total_count'] = len(current_high_items)
            effective_triage_high['attention_now_count'] = len(current_high_items)
            effective_triage_high['total_attention_now_count'] = len(current_high_items)
            effective_triage_high['stale_attention_count'] = 0
            effective_triage_high['total_stale_attention_count'] = 0
            effective_triage_high['related_group_count'] = len(current_high_items)
            effective_triage_high['total_related_group_count'] = len(current_high_items)
            effective_triage_high['top_related_groups'] = [
                group for group in (effective_triage_high.get('top_related_groups') or [])
                if group.get('attention_now') and not group.get('stale_attention')
            ]

    new_high_count = summary.get('high_count', 0)
    recent_high_count = triage_high_latest.get('total_count', triage_high_latest.get('count', 0)) if triage_high_latest.get('items') else 0
    recent_attention_now_count = triage_high_latest.get('total_attention_now_count', triage_high_latest.get('attention_now_count', 0)) if triage_high_latest.get('items') else 0
    recent_stale_high_count = triage_high_latest.get('total_stale_attention_count', triage_high_latest.get('stale_attention_count', 0)) if triage_high_latest.get('items') else 0
    effective_high_count = new_high_count
    if effective_triage_high_scope != 'unread+high' and recent_high_count:
        effective_high_count = max(new_high_count, recent_high_count)

    return {
        'quickstart': quickstart_payload(),
        'current_only': current_only,
        'review_worthy_only': review_worthy_only,
        'latest_count': len(latest),
        'unread_count': len(unread),
        'new_count': summary.get('new_count', 0),
        'latest_thread_count': len(latest_threads),
        'latest_current_count': len(latest_current),
        'latest_threads_current_count': len(latest_threads_current),
        'high_count': effective_high_count,
        'new_high_count': new_high_count,
        'recent_high_count': recent_high_count,
        'recent_attention_now_count': recent_attention_now_count,
        'recent_stale_high_count': recent_stale_high_count,
        'has_current_high_attention': recent_attention_now_count > 0 or new_high_count > 0,
        'draft_scope': drafts.get('scope', 'unread'),
        'draft_count': drafts.get('draft_count', 0),
        'triage_count': triage.get('count', 0),
        'triage_meaningful_count': triage_meaningful.get('count', 0),
        'triage_current_count': triage_current.get('count', 0),
        'triage_reply_needed_count': triage.get('reply_needed_count', 0),
        'triage_high_count': effective_triage_high.get('total_count', effective_triage_high.get('count', 0)),
        'triage_high_group_count': effective_triage_high.get('total_related_group_count', effective_triage_high.get('related_group_count', 0)),
        'triage_high_attention_now_count': effective_triage_high.get('total_attention_now_count', effective_triage_high.get('attention_now_count', 0)),
        'triage_high_stale_count': effective_triage_high.get('total_stale_attention_count', effective_triage_high.get('stale_attention_count', 0)),
        'triage_high_groups': effective_triage_high.get('top_related_groups', []),
        'latest': latest,
        'latest_meaningful': latest_meaningful,
        'latest_current': latest_current,
        'latest_threads': latest_threads,
        'latest_threads_current': latest_threads_current,
        'latest_current_suppressed': latest_suppressed(latest_current_payload),
        'latest_threads_current_suppressed': latest_suppressed(latest_threads_current_payload),
        'unread': unread,
        'new_messages': summary.get('messages', []),
        'drafts': drafts.get('drafts', []),
        'triage': triage.get('items', []),
        'triage_meaningful': triage_meaningful.get('items', []),
        'triage_current': triage_current.get('items', []),
        'triage_reply': triage_reply.get('items', []),
        'triage_high': effective_triage_high.get('items', []),
        'triage_high_scope': effective_triage_high_scope,
        'focus_scope': focus.get('scope', 'unread'),
        'focus': focus.get('focus'),
        'focus_burst_count': focus.get('focus_burst_count', 0),
        'focus_related_burst_count': focus.get('focus_related_burst_count', 0),
        'focus_draft': focus.get('draft'),
        'focus_fallback_thread': focus.get('fallback_thread'),
        'focus_skipped_ephemeral_count': focus.get('skipped_ephemeral_count', 0),
        'next_step': next_step,
        'security_alerts': security_alerts,
        'errors': {
            key: value for key, value in {
                'latest': latest_error,
                'latest_meaningful': latest_meaningful_error,
                'latest_current': latest_current_error,
                'latest_threads': latest_threads_error,
                'latest_threads_current': latest_threads_current_error,
                'unread': unread_error,
                'summary': summary_error,
                'drafts': drafts_error,
                'triage': triage_error,
                'triage_meaningful': triage_meaningful_error,
                'triage_current': triage_current_error,
                'triage_reply': triage_reply_error,
                'triage_high': triage_high_error,
                'triage_high_latest': triage_high_latest_error,
                'focus': focus_error,
                'next_step': next_step_error,
                'security_alerts': security_alerts_error,
            }.items() if value
        },
    }


def has_current_mail_activity(board):
    if board.get('new_count', 0) > 0:
        return True
    if board.get('unread_count', 0) > 0:
        return True
    if board.get('draft_count', 0) > 0:
        return True
    if board.get('latest_current'):
        return True
    if board.get('latest_threads_current'):
        return True
    if board.get('triage_current'):
        return True
    if board.get('has_current_high_attention'):
        return True
    if (board.get('security_alerts') or {}).get('current_count', 0) > 0:
        return True
    focus = board.get('focus') or {}
    if focus and not focus.get('stale_attention'):
        return True
    next_step = board.get('next_step') or {}
    selected = next_step.get('selected_group') or {}
    if selected and not selected.get('stale_attention') and not next_step.get('review_only'):
        return True
    return False


def summarize_suppressed_hint(group):
    group = group or {}
    label = group.get('label') or group.get('sender') or group.get('from') or group.get('sender_email') or 'onbekend'
    subject = group.get('subject') or '(geen onderwerp)'
    action = group.get('action_hint') or 'mail checken'
    reason = group.get('reason') or 'onderdrukt'
    age = group.get('age_hint') or group.get('latest_age_hint')
    age_suffix = f" ({age})" if age else ''
    count = group.get('count') or 1
    count_suffix = f" x{count}" if count and count > 1 else ''
    return f"{label} — {subject} [{action}]{count_suffix}{age_suffix} | {reason}"



def render_text(board, show_preview=False, current_only=False, review_worthy_only=False):
    lines = ['Mailboard']
    quickstart = board.get('quickstart') or []
    if quickstart:
        lines.append('- snelle start:')
        for item in quickstart:
            alias_suffix = ''
            if item.get('also'):
                alias_suffix = f" (ook: {', '.join(item['also'])})"
            lines.append(f"  - {item['command']}: {item['description']}{alias_suffix}")
    has_current_activity = has_current_mail_activity(board)
    triage_high_suffix = ''
    if board.get('triage_high_count', 0) > 1 and board.get('triage_high_group_count', 0):
        triage_high_suffix = f" in {board['triage_high_group_count']} cluster(s)"
    recent_high_count = board.get('recent_high_count', 0)
    recent_attention_now_count = board.get('recent_attention_now_count', 0)
    recent_stale_high_count = board.get('recent_stale_high_count', 0)
    recent_high_groups = board.get('triage_high_group_count', 0)
    recent_high_suffix = f" in {recent_high_groups} cluster(s)" if recent_high_count and recent_high_groups else ''
    if recent_high_count and board.get('triage_high_scope') != 'unread+high':
        freshness_bits = [f"actueel {recent_attention_now_count}", f"niet actueel {recent_stale_high_count}"]
        if recent_attention_now_count == 0:
            freshness_bits.append('alles niet actueel')
        high_summary = (
            f"hoog nieuw: {board.get('new_high_count', 0)}, hoog recent: {recent_high_count}{recent_high_suffix}"
            f" ({', '.join(freshness_bits)})"
        )
    else:
        high_summary = f"hoog: {board.get('high_count', 0)}"
    triage_high_summary = f"{board['triage_high_count']}{triage_high_suffix}"
    if board.get('triage_high_scope') != 'unread+high' and board.get('triage_high_count'):
        triage_freshness_bits = [
            f"actueel {board.get('triage_high_attention_now_count', 0)}",
            f"niet actueel {board.get('triage_high_stale_count', 0)}",
        ]
        if board.get('triage_high_attention_now_count', 0) == 0:
            triage_freshness_bits.append('alles niet actueel')
        triage_high_summary += f" ({', '.join(triage_freshness_bits)})"
    lines.append(
        f"- nieuw: {board['new_count']} ({high_summary}), unread: {board['unread_count']}, drafts: {board['draft_count']}, triage-reply: {board['triage_reply_needed_count']}, triage-high: {triage_high_summary}"
    )
    triage_high_groups = board.get('triage_high_groups') or []
    if triage_high_groups and (not current_only or board.get('has_current_high_attention')):
        group_bits = [format_cluster_hint(group, include_age=True) for group in triage_high_groups[:2]]
        remaining = max(0, len(triage_high_groups) - len(group_bits))
        suffix = f" +{remaining} cluster(s)" if remaining else ''
        lines.append(f"- hoge clusters: {'; '.join(group_bits)}{suffix}")
    security_alerts = board.get('security_alerts') or {}
    if security_alerts.get('recent_count') and (not current_only or security_alerts.get('current_count')):
        lines.append(
            f"- security alerts: actueel {security_alerts.get('current_count', 0)}, recent {security_alerts.get('recent_count', 0)}, stale {security_alerts.get('stale_count', 0)}"
        )
        selected_alert = security_alerts.get('selected_group') or {}
        if selected_alert:
            sender = selected_alert.get('sender') or selected_alert.get('sender_email') or 'onbekend'
            subject = selected_alert.get('subject') or '(geen onderwerp)'
            security = selected_alert.get('security_alert_summary')
            security_suffix = f" {{{security}}}" if security else ''
            stale_suffix = ' [niet actueel]' if selected_alert.get('stale_attention') else ''
            lines.append(
                f"- security focus: {sender} — {subject} [{selected_alert.get('action_hint') or 'security'}] ({selected_alert.get('latest_age_hint') or '?'}){security_suffix}{stale_suffix}"
            )
        if security_alerts.get('recommended_command'):
            lines.append(f"- security command: {security_alerts.get('recommended_command')}")
    if board['unread']:
        first = board['unread'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        line = f"- bovenste unread: {first['from']} — {first['subject']}{format_attachment_hint(first)}{format_security_alert_hint(first)}{age}"
        if show_preview and first.get('preview'):
            line += f" — {first['preview'][:140]}"
        lines.append(line)
    elif board['latest_current']:
        first = board['latest_current'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        line = f"- actuele betekenisvolle mail: {first['from']} — {first['subject']}{format_attachment_hint(first)}{format_security_alert_hint(first)}{age}{format_stale_attention_hint(first)}"
        if show_preview and first.get('preview'):
            line += f" — {first['preview'][:140]}"
        lines.append(line)
    elif not current_only and board['latest_meaningful']:
        first = board['latest_meaningful'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        line = f"- laatste betekenisvolle mail: {first['from']} — {first['subject']}{format_attachment_hint(first)}{format_security_alert_hint(first)}{age}{format_stale_attention_hint(first)}"
        if show_preview and first.get('preview'):
            line += f" — {first['preview'][:140]}"
        lines.append(line)
    elif not current_only and board['latest']:
        first = board['latest'][0]
        age = f" ({first.get('age_hint')})" if first.get('age_hint') else ''
        line = f"- laatste mail: {first['from']} — {first['subject']}{format_attachment_hint(first)}{format_security_alert_hint(first)}{age}{format_stale_attention_hint(first)}"
        if show_preview and first.get('preview'):
            line += f" — {first['preview'][:140]}"
        lines.append(line)
    thread = None
    if board.get('latest_threads_current'):
        thread = board['latest_threads_current'][0]
        thread_label = 'actieve thread'
    elif not current_only and board.get('latest_threads'):
        thread = board['latest_threads'][0]
        thread_label = 'actieve thread' if not thread.get('stale_attention') else 'laatste betekenisvolle thread'
    if thread:
        noise = ' [code-thread]' if thread.get('ephemeral_only') else ''
        stale = ' [niet actueel]' if thread.get('stale_attention') else ''
        variant_suffix = f", +{thread.get('subject_variant_count', 0) - 1} variant(en)" if (thread.get('subject_variant_count', 0) or 0) > 1 else ''
        time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
        time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
        lines.append(
            f"- {thread_label}: {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{variant_suffix}, laatste van {thread.get('latest_from', 'onbekend')}{time_suffix}){format_attachment_hint(thread)}{format_security_alert_hint(thread)}{noise}{stale}"
        )
    triage_items = board.get('triage_current') or ([] if current_only else (board.get('triage_meaningful') or []))
    if triage_items:
        item = triage_items[0]
        deadline = f" ⏰{item.get('deadline_hint')}" if item.get('deadline_hint') else ''
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        attach = format_attachment_hint(item)
        security = format_security_alert_hint(item)
        burst = f" ({item.get('related_group_size', 0)}x verwant)" if (item.get('related_group_size', 0) or 0) > 1 else ''
        stale = ' [niet actueel]' if item.get('stale_attention') else ''
        triage_label = 'triage nu' if board.get('triage_current') else ('triage review' if review_worthy_only else 'triage eerst')
        lines.append(
            f"- {triage_label}: {item['from']} — {item['subject']}{attach}{security} [{item['action_hint']}{' ↩' if item.get('reply_needed') else ''}]{deadline}{burst}{age}{stale}"
        )
    if board.get('focus') and (not current_only or not (board.get('focus') or {}).get('stale_attention')):
        item = board['focus']
        deadline = f" ⏰{item.get('deadline_hint')}" if item.get('deadline_hint') else ''
        attach = format_attachment_hint(item)
        security = format_security_alert_hint(item)
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        related_burst = board.get('focus_related_burst_count', 0)
        exact_burst = board.get('focus_burst_count', 0)
        burst = max(related_burst, exact_burst)
        burst_label = 'verwant' if related_burst > exact_burst else 'soortgelijk'
        burst_suffix = f" ({burst}x {burst_label})" if burst > 1 else ''
        focus_prefix = 'focus review' if review_worthy_only else 'focus nu'
        focus_line = (
            f"- {focus_prefix} ({board.get('focus_scope', 'mail')}): {item['from']} — {item['subject']}{attach}{security} "
            f"[{item['action_hint']}{' ↩' if item.get('reply_needed') else ''}]{deadline}{burst_suffix}{age}"
        )
        if item.get('stale_attention'):
            focus_line = f"- geen actuele focus, laatste kandidaat was: {item['from']} — {item['subject']}{attach}{security} [{item['action_hint']}{' ↩' if item.get('reply_needed') else ''}]{deadline}{burst_suffix}{age} [niet actueel]"
        if board.get('focus_draft'):
            focus_line += ' + concept'
        lines.append(focus_line)
    elif not current_only and board.get('focus_fallback_thread'):
        thread = board['focus_fallback_thread']
        participants = ', '.join((thread.get('participants') or [])[:2]) or thread.get('latest_from', 'onbekend')
        extra_people = max(0, len(thread.get('participants') or []) - 2)
        if extra_people:
            participants += f' (+{extra_people})'
        skipped = board.get('focus_skipped_ephemeral_count', 0)
        time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
        time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
        stale = ' [niet actueel]' if thread.get('stale_attention') else ''
        suffix = f", code-noise overgeslagen: {skipped}" if skipped else ''
        label = 'geen actuele focus, laatste betekenisvolle thread' if thread.get('stale_attention') else 'focus fallback'
        lines.append(
            f"- {label}: {participants} — {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{time_suffix}){format_attachment_hint(thread)}{suffix}{stale}"
        )
    if board['triage_reply']:
        item = board['triage_reply'][0]
        deadline = f" ⏰{item.get('deadline_hint')}" if item.get('deadline_hint') else ''
        attach = format_attachment_hint(item)
        burst = f" ({item.get('related_group_size', 0)}x verwant)" if (item.get('related_group_size', 0) or 0) > 1 else ''
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        lines.append(
            f"- reply nodig: {item['from']} — {item['subject']}{attach} [{item['action_hint']} ↩]{deadline}{burst}{age}"
        )
    if board['triage_high'] and (not current_only or not (board['triage_high'][0]).get('stale_attention')):
        item = board['triage_high'][0]
        deadline = f" ⏰{item.get('deadline_hint')}" if item.get('deadline_hint') else ''
        attach = format_attachment_hint(item)
        scope = board.get('triage_high_scope', 'unread+high')
        scope_suffix = '' if scope == 'unread+high' else f" ({scope})"
        burst = f" ({item.get('related_group_size', 0)}x verwant)" if (item.get('related_group_size', 0) or 0) > 1 else ''
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        stale = ' [niet actueel]' if item.get('stale_attention') else ''
        label = 'hoge prioriteit'
        if item.get('stale_attention') and not board.get('has_current_high_attention'):
            label = 'geen actuele hoge prioriteit, laatste recente high-prio'
        lines.append(
            f"- {label}{scope_suffix}: {item['from']} — {item['subject']}{attach}{format_security_alert_hint(item)} [{item['action_hint']}]{deadline}{burst}{age}{stale}"
        )
    next_step = board.get('next_step') or {}
    selected = next_step.get('selected_group') or {}
    if next_step.get('recommended_route') and next_step.get('recommended_route') != 'noop' and selected and (not current_only or (not selected.get('stale_attention') and not next_step.get('review_only'))):
        review_only = bool(next_step.get('review_only'))
        is_stale = bool(selected.get('stale_attention'))
        prefix = '- review-kandidaat:' if review_only or is_stale else '- volgende stap:'
        lines.append(f"{prefix} {format_next_step_candidate_hint(selected, include_age=True)}" + (' + concept' if next_step.get('selected_draft') else ''))
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
            command_label = 'review command' if review_only or is_stale else 'next-step command'
            lines.append(f"- {command_label}: {next_step.get('recommended_command')}")
    if not current_only:
        quick_view_command = 'python3 scripts/mail-dispatch.py latest --review-worthy --threads -n 5' if review_worthy_only else 'python3 scripts/mail-dispatch.py latest --meaningful --threads -n 5'
        lines.append(f'- inbox quick view: {quick_view_command}')
        if has_current_activity:
            now_command = 'python3 scripts/mail-dispatch.py triage --all --review-worthy --clusters -n 5' if review_worthy_only else 'python3 scripts/mail-dispatch.py now --clusters -n 5'
            lines.append(f'- inbox now: {now_command}')
    if board['drafts']:
        draft = board['drafts'][0]
        lines.append(f"- concept ({board.get('draft_scope', 'mail')}) klaar voor: {draft['sender']} — {draft['subject']}{format_attachment_hint(draft)}")
    if current_only and not has_current_activity:
        lines.append('- geen actuele mailaandacht')
    elif review_worthy_only and not has_current_activity and not board.get('next_step', {}).get('candidates'):
        lines.append('- geen reviewwaardige mailaandacht')

    next_step_suppressed = (board.get('next_step') or {}).get('suppressed_groups') or []
    security_suppressed = (board.get('security_alerts') or {}).get('suppressed_groups') or []
    latest_suppressed = board.get('latest_current_suppressed') or []
    latest_thread_suppressed = board.get('latest_threads_current_suppressed') or []
    if not has_current_activity and latest_suppressed:
        preview = '; '.join(summarize_suppressed_hint(group) for group in latest_suppressed[:2])
        remaining = max(0, len(latest_suppressed) - 2)
        suffix = f" +{remaining} meer" if remaining else ''
        lines.append(f"- onderdrukt latest: {preview}{suffix}")
    if not has_current_activity and latest_thread_suppressed:
        preview = '; '.join(summarize_suppressed_hint(group) for group in latest_thread_suppressed[:2])
        remaining = max(0, len(latest_thread_suppressed) - 2)
        suffix = f" +{remaining} meer" if remaining else ''
        lines.append(f"- onderdrukt threads: {preview}{suffix}")
    if not has_current_activity and next_step_suppressed:
        preview = '; '.join(summarize_suppressed_hint(group) for group in next_step_suppressed[:2])
        remaining = max(0, len(next_step_suppressed) - 2)
        suffix = f" +{remaining} meer" if remaining else ''
        lines.append(f"- onderdrukt next-step: {preview}{suffix}")
    if not has_current_activity and security_suppressed:
        preview = '; '.join(summarize_suppressed_hint(group) for group in security_suppressed[:2])
        remaining = max(0, len(security_suppressed) - 2)
        suffix = f" +{remaining} meer" if remaining else ''
        lines.append(f"- onderdrukt security: {preview}{suffix}")
    errors = board.get('errors') or {}
    if errors:
        lines.append(f"- deels gedegradeerd: {', '.join(sorted(errors))}")
    return '\n'.join(lines)


def help_payload():
    return {
        'quickstart': quickstart_payload(),
        'flags': [
            {
                'flag': '-n, --limit <n>',
                'description': 'maximaal aantal items per deelview (1-20)',
            },
            {
                'flag': '--json',
                'description': 'toon volledige board-payload als JSON',
            },
            {
                'flag': '--preview',
                'description': 'toon korte preview bij bovenste mail in tekstoutput',
            },
            {
                'flag': '--current-only',
                'description': 'toon alleen actuele mailaandacht en suppressed-uitleg als de mailbox nu leeg is',
            },
            {
                'flag': '--review-worthy',
                'description': 'toon alleen mail die na actualiteitsfiltering nog echt reviewwaardig is',
            },
        ],
        'notes': [
            'Gebruik standaard mailboard voor een compact totaaloverzicht van nieuw, unread, triage, focus en volgende stap.',
            'Gebruik --current-only als je juist wilt zien waarom er nu niets actueels overblijft.',
            'Gebruik --json voor machineleesbare suppressed-groepen, security-alerts en next-step context.',
        ],
    }


def render_help():
    payload = help_payload()
    lines = ['Mailboard']
    if payload.get('quickstart'):
        lines.append('- snelle start:')
        for item in payload['quickstart']:
            alias_suffix = ''
            if item.get('also'):
                alias_suffix = f" (ook: {', '.join(item['also'])})"
            lines.append(f"  - {item['command']}: {item['description']}{alias_suffix}")
    if payload.get('flags'):
        lines.append('- opties:')
        for item in payload['flags']:
            lines.append(f"  - {item['flag']}: {item['description']}")
    if payload.get('notes'):
        lines.append('- notities:')
        for note in payload['notes']:
            lines.append(f"  - {note}")
    return '\n'.join(lines)


def main():
    raw_args = sys.argv[1:]
    if '--help' in raw_args or '-h' in raw_args:
        if '--json' in raw_args:
            print(json.dumps(help_payload(), ensure_ascii=False, indent=2))
        else:
            print(render_help())
        return

    parser = argparse.ArgumentParser(description='Compact mailboard met latest/unread/new/drafts', add_help=False)
    parser.add_argument('-n', '--limit', type=int, default=5)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--preview', action='store_true', help='toon korte preview bij bovenste mail in tekstoutput')
    parser.add_argument('--current-only', action='store_true', help='onderdruk stale-only tekstregels en toon alleen actuele mailaandacht')
    parser.add_argument('--review-worthy', action='store_true', help='toon alleen mail die na actualiteitsfiltering nog echt reviewwaardig is')
    args = parser.parse_args()

    board = build_board(limit=max(1, min(args.limit, 20)), current_only=args.current_only, review_worthy_only=args.review_worthy)
    if args.json:
        print(json.dumps(board, ensure_ascii=False, indent=2))
    else:
        print(render_text(board, show_preview=args.preview, current_only=args.current_only, review_worthy_only=args.review_worthy))


if __name__ == '__main__':
    main()
