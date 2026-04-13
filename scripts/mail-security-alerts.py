#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPTS = ROOT / 'scripts'
MAIL_TRIAGE = SCRIPTS / 'mail-triage.py'

SECURITY_ACTIONS = {
    'login-alert checken',
    'security checken',
}


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
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def shell_join(parts):
    return ' '.join(shlex.quote(str(part)) for part in parts)


def build_thread_command(group):
    args = ['python3', 'scripts/mail-dispatch.py', 'thread']
    latest_uid = (group or {}).get('latest_uid')
    sender = (group or {}).get('sender_email') or (group or {}).get('sender') or (group or {}).get('from')
    action = (group or {}).get('action_hint')
    if latest_uid is not None:
        args += ['--uid', str(latest_uid)]
    if sender:
        args += ['--sender', sender]
    if action:
        args += ['--action', action]
    args += ['--messages', '5']
    return shell_join(args)


def group_key(group):
    return (
        group.get('latest_uid'),
        group.get('sender_email') or group.get('sender') or group.get('from'),
        group.get('latest_subject'),
        group.get('security_alert_summary'),
    )


def is_security_group(group):
    if not group:
        return False
    if group.get('security_alert_summary'):
        return True
    action = (group.get('action_hint') or '').strip().lower()
    return action in SECURITY_ACTIONS


def collapse_parallel_security_groups(groups):
    collapsed = []
    seen_security_streams = set()
    for group in groups or []:
        sender = (group.get('sender_email') or group.get('sender') or group.get('from') or '').strip().lower()
        action = (group.get('action_hint') or '').strip().lower()
        should_collapse = bool(
            sender
            and action == 'security checken'
            and group.get('security_alert_summary')
            and group.get('no_reply_only')
            and not group.get('reply_needed')
            and not group.get('deadline_hint')
        )
        if not should_collapse:
            collapsed.append(group)
            continue

        stream_key = (sender, action)
        if stream_key in seen_security_streams:
            continue
        seen_security_streams.add(stream_key)
        collapsed.append(group)
    return collapsed


def filter_security_groups(groups):
    seen = set()
    filtered = []
    for group in collapse_parallel_security_groups(groups):
        if not is_security_group(group):
            continue
        if not (group.get('attention_now') or group.get('review_worthy')):
            continue
        key = group_key(group)
        if key in seen:
            continue
        seen.add(key)
        filtered.append(group)
    return filtered


def suppression_reason(group, *, current_only=False):
    group = group or {}
    if current_only and not group.get('attention_now'):
        return 'niet actueel'
    if group.get('expected_security_change'):
        return 'verwachte bekende securitywijziging'
    if not group.get('review_worthy'):
        if group.get('stale_attention'):
            return 'niet actueel en niet reviewwaardig'
        return 'niet reviewwaardig'
    if group.get('no_reply_only') and not group.get('reply_needed') and not group.get('deadline_hint'):
        return 'no-reply zonder vervolgsignaal'
    return 'geen duidelijke security-alert vervolgstap'


def summarize_group(group):
    return {
        'sender': group.get('sender') or group.get('from'),
        'sender_email': group.get('sender_email'),
        'subject': group.get('latest_subject') or group.get('subject'),
        'action_hint': group.get('action_hint'),
        'count': group.get('count') or 1,
        'urgency': group.get('urgency'),
        'latest_age_hint': group.get('latest_age_hint') or group.get('age_hint'),
        'stale_attention': bool(group.get('stale_attention')),
        'attention_now': bool(group.get('attention_now')),
        'review_worthy': bool(group.get('review_worthy')),
        'expected_security_change': bool(group.get('expected_security_change')),
        'security_alert_summary': group.get('security_alert_summary'),
        'latest_uid': group.get('latest_uid'),
        'recommended_command': build_thread_command(group),
    }


def summarize_suppressed_group(group, *, current_only=False):
    summary = summarize_group(group)
    summary['reason'] = suppression_reason(group, current_only=current_only)
    return summary


def build_summary(limit=5, current_only=False):
    limit = max(1, min(limit, 10))
    current = run_json(
        ['python3', str(MAIL_TRIAGE), '--json', '--all', '--current-only', '--review-worthy', '--clusters', '-n', str(limit), '--search-limit', '50'],
        default={},
        timeout=30,
    ) or {}
    recent = run_json(
        ['python3', str(MAIL_TRIAGE), '--json', '--all', '--review-worthy', '--clusters', '-n', str(limit), '--search-limit', '50'],
        default={},
        timeout=30,
    ) or {}
    raw_current = run_json(
        ['python3', str(MAIL_TRIAGE), '--json', '--all', '--current-only', '--clusters', '-n', str(limit * 2), '--search-limit', '50'],
        default={},
        timeout=30,
    ) or {}
    raw_recent = run_json(
        ['python3', str(MAIL_TRIAGE), '--json', '--all', '--clusters', '-n', str(limit * 2), '--search-limit', '50'],
        default={},
        timeout=30,
    ) or {}

    current_groups = filter_security_groups(current.get('groups') or current.get('items') or [])
    recent_groups = filter_security_groups(recent.get('groups') or recent.get('items') or [])
    raw_current_groups = [group for group in collapse_parallel_security_groups(raw_current.get('groups') or raw_current.get('items') or []) if is_security_group(group)]
    raw_recent_groups = [group for group in collapse_parallel_security_groups(raw_recent.get('groups') or raw_recent.get('items') or []) if is_security_group(group)]

    current_keys = {group_key(group) for group in current_groups}
    recent_only_groups = [group for group in recent_groups if group_key(group) not in current_keys]

    selected = current_groups[0] if current_groups else (None if current_only else (recent_only_groups[0] if recent_only_groups else None))
    selected_summary = summarize_group(selected) if selected else None

    suppressed_groups = []
    seen_suppressed = set()
    raw_groups = raw_current_groups if current_only else raw_recent_groups
    visible_keys = {group_key(group) for group in (current_groups if current_only else recent_groups)}
    for group in raw_groups:
        key = group_key(group)
        if key in visible_keys or key in seen_suppressed:
            continue
        seen_suppressed.add(key)
        suppressed_groups.append(summarize_suppressed_group(group, current_only=current_only))
        if len(suppressed_groups) >= limit:
            break

    recommended_route = 'noop'
    if current_only:
        reason = 'geen actuele security-alert mailcluster'
    else:
        reason = 'geen duidelijke security-alert mailcluster'
    if selected:
        if selected.get('attention_now') and not selected.get('stale_attention'):
            recommended_route = 'security-alert-now'
            reason = 'er is een actuele security-alert mailcluster die nu review verdient'
        else:
            recommended_route = 'security-alert-review'
            reason = 'er is geen actuele alert, maar wel een recente security-alert cluster om kort na te lopen'

    return {
        'current_only': current_only,
        'current_count': len(current_groups),
        'recent_count': len(recent_groups),
        'recent_only_count': len(recent_only_groups),
        'stale_count': sum(1 for group in recent_groups if group.get('stale_attention')),
        'attention_now_count': sum(1 for group in current_groups if group.get('attention_now') and not group.get('stale_attention')),
        'suppressed_count': len(suppressed_groups),
        'recommended_route': recommended_route,
        'recommended_command': selected_summary.get('recommended_command') if selected_summary else None,
        'reason': reason,
        'selected_group': selected_summary,
        'current_groups': [summarize_group(group) for group in current_groups[:limit]],
        'recent_groups': [] if current_only else [summarize_group(group) for group in recent_groups[:limit]],
        'suppressed_groups': suppressed_groups,
    }


def render_group(group):
    if not group:
        return '-'
    sender = group.get('sender') or group.get('sender_email') or 'onbekend'
    subject = group.get('subject') or '(geen onderwerp)'
    count = group.get('count') or 1
    age = group.get('latest_age_hint') or '?'
    security = group.get('security_alert_summary')
    suffix = f' {{{security}}}' if security else ''
    stale = ' [niet actueel]' if group.get('stale_attention') else ''
    return f"{sender} — {subject} [{group.get('action_hint') or 'security'}] x{count} ({age}){suffix}{stale}"


def render_text(summary):
    lines = ['Mail security alerts']
    lines.append(
        f"- current={summary.get('current_count', 0)}, recent={summary.get('recent_count', 0)}, stale={summary.get('stale_count', 0)}, suppressed={summary.get('suppressed_count', 0)}, reason={summary.get('reason')}"
    )
    selected = summary.get('selected_group')
    if selected:
        lines.append(f"- selected={render_group(selected)}")
    if summary.get('recommended_command'):
        lines.append(f"- command={summary.get('recommended_command')}")
    if not selected:
        for index, group in enumerate((summary.get('suppressed_groups') or [])[:3], start=1):
            lines.append(f"- suppressed{index}={render_group(group)} | reason={group.get('reason')}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Vat actuele en recente security-alert mailclusters samen')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('-n', '--limit', type=int, default=5)
    parser.add_argument('--current-only', action='store_true', help='toon alleen security-alerts die nu nog actueel aandacht vragen')
    args = parser.parse_args()

    summary = build_summary(limit=args.limit, current_only=args.current_only)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
