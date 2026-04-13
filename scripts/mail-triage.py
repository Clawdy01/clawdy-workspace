#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

from mail_heuristics import (
    ACTION_PRIORITY,
    extract_deadline_hint,
    format_attachment_hint,
    format_cluster_hint,
    format_recency_hint,
    format_security_alert_hint,
    is_ephemeral_code_message,
    is_self_message,
    is_test_message,
    needs_attention_now,
    reply_needed,
    suggest_action,
    summarize_security_alerts,
    group_needs_review,
)

ROOT = Path('/home/clawdy/.openclaw/workspace')
MAIL_LATEST = ROOT / 'scripts' / 'mail-latest.py'


def normalize_subject(value):
    value = ' '.join((value or '').split())
    while True:
        updated = re.sub(r'^(?:(?:re|fw|fwd|aw|sv)\s*:\s*)+', '', value, flags=re.I).strip()
        if updated == value:
            break
        value = updated
    return value or '(geen onderwerp)'


def related_group_key(item):
    sender = (item.get('sender_email') or item.get('from') or '').strip().lower()
    action = (item.get('action_hint') or '').strip().lower()
    urgency = (item.get('urgency') or '').strip().lower()
    if sender and action:
        return ('sender-action', sender, action, urgency)
    return ('subject', sender, normalize_subject(item.get('subject')), urgency)


def summarize_related_groups(groups, limit=None):
    summaries = []
    for items in groups.values():
        if not items:
            continue
        latest = max(items, key=lambda item: (item.get('date_ts') or 0, int(item.get('uid') or 0)))
        summary = {
            'from': latest.get('from'),
            'sender': latest.get('from'),
            'sender_email': latest.get('sender_email'),
            'action_hint': latest.get('action_hint'),
            'urgency': latest.get('urgency'),
            'count': len(items),
            'latest_subject': latest.get('subject'),
            'latest_uid': latest.get('uid'),
            'latest_date_ts': latest.get('date_ts'),
            'latest_age_hint': format_recency_hint(latest.get('date_ts')),
            'latest_preview': latest.get('preview'),
            'security_alert_summary': summarize_security_alerts(items),
            'attention_now': any(needs_attention_now(item) for item in items),
            'stale_attention': not any(needs_attention_now(item) for item in items),
            'reply_needed': any(item.get('reply_needed') for item in items),
            'deadline_hint': next((item.get('deadline_hint') for item in items if item.get('deadline_hint')), None),
            'no_reply_only': all(item.get('no_reply') for item in items),
            'unread_count': sum(1 for item in items if item.get('unread')),
        }
        summary['review_worthy'] = group_needs_review(summary)
        summaries.append(summary)

    summaries.sort(
        key=lambda group: (
            0 if group.get('attention_now') else 1,
            -int(group.get('count') or 0),
            0 if group.get('urgency') == 'high' else 1,
            ACTION_PRIORITY.get(group.get('action_hint'), 99),
            -(group.get('latest_date_ts') or 0),
        )
    )
    return summaries[:limit] if limit else summaries


def run_latest(limit=10, unread_only=True, search_limit=50):
    fetch_limit = max(limit, search_limit)
    cmd = ['python3', str(MAIL_LATEST), '-n', str(fetch_limit), '--json', '--search-limit', str(search_limit)]
    if unread_only:
        cmd.append('--unread')
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'mail-latest failed: {proc.returncode}')
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'Invalid JSON from mail-latest: {exc}\n{proc.stdout}')


def triage(limit=10, unread_only=True, reply_only=False, high_only=False, current_only=False, search_limit=50, clusters_only=False):
    rows = run_latest(limit=limit, unread_only=unread_only, search_limit=search_limit)
    items = []
    for row in rows:
        item = dict(row)
        item['deadline_hint'] = extract_deadline_hint(item)
        item['ephemeral_code'] = is_ephemeral_code_message(item)
        item['action_hint'] = suggest_action(item)
        item['reply_needed'] = reply_needed(item)
        item['attention_now'] = needs_attention_now(item)
        item['stale_attention'] = not item['attention_now']
        if is_self_message(item):
            continue
        if is_test_message(item):
            continue
        items.append(item)

    groups = {}
    for item in items:
        groups.setdefault(related_group_key(item), []).append(item)
    for item in items:
        group = groups.get(related_group_key(item), [])
        item['related_group_size'] = len(group)

    items.sort(
        key=lambda item: (
            0 if item.get('reply_needed') else 1,
            0 if item.get('attention_now') else 1,
            0 if not item.get('ephemeral_code') else 1,
            0 if item.get('urgency') == 'high' else 1,
            -int(item.get('related_group_size') or 0),
            ACTION_PRIORITY.get(item.get('action_hint'), 99),
            -(item.get('date_ts') or 0),
            -int(item.get('uid') or 0),
        )
    )

    if high_only:
        items = [item for item in items if item.get('urgency') == 'high']
    if reply_only:
        items = [item for item in items if item.get('reply_needed')]
    if current_only:
        items = [item for item in items if item.get('attention_now')]

    total_items = list(items)
    total_count = len(total_items)
    total_high_count = sum(1 for item in total_items if item.get('urgency') == 'high')
    total_high_attention_now_count = sum(1 for item in total_items if item.get('urgency') == 'high' and item.get('attention_now'))
    total_high_stale_attention_count = sum(1 for item in total_items if item.get('urgency') == 'high' and item.get('stale_attention'))
    total_reply_needed_count = sum(1 for item in total_items if item.get('reply_needed'))
    total_attention_now_count = sum(1 for item in total_items if item.get('attention_now'))
    total_stale_attention_count = sum(1 for item in total_items if item.get('stale_attention'))
    total_related_group_count = len({related_group_key(item) for item in total_items})
    filtered_groups = {}
    for item in total_items:
        filtered_groups.setdefault(related_group_key(item), []).append(item)
    related_groups = summarize_related_groups(filtered_groups)
    top_related_groups = related_groups[:3]

    items = related_groups[:limit] if clusters_only else total_items[:limit]

    scope = 'unread' if unread_only else 'latest'
    if high_only:
        scope += '+high'
    if reply_only:
        scope += '+reply'
    if current_only:
        scope += '+current'

    return {
        'scope': scope,
        'mode': 'clusters' if clusters_only else 'items',
        'count': len(items),
        'total_count': total_count,
        'high_count': sum(1 for item in items if item.get('urgency') == 'high'),
        'total_high_count': total_high_count,
        'reply_needed_count': sum(1 for item in items if item.get('reply_needed')),
        'total_reply_needed_count': total_reply_needed_count,
        'attention_now_count': sum(1 for item in items if item.get('attention_now')),
        'total_attention_now_count': total_attention_now_count,
        'total_high_attention_now_count': total_high_attention_now_count,
        'stale_attention_count': sum(1 for item in items if item.get('stale_attention')),
        'total_stale_attention_count': total_stale_attention_count,
        'total_high_stale_attention_count': total_high_stale_attention_count,
        'related_group_count': len({related_group_key(item) for item in items}),
        'total_related_group_count': total_related_group_count,
        'groups': related_groups,
        'group_count': len(related_groups),
        'top_related_groups': top_related_groups,
        'items': items,
    }


def render_text(result, show_preview=False):
    items = result.get('items') or []
    if result.get('mode') == 'clusters':
        if not items:
            return f"Mail clusters ({result.get('scope', 'mail')}): 0 clusters"

        lines = [
            f"Mail clusters ({result.get('scope', 'mail')}): {result.get('count', 0)} clusters (totaal {result.get('group_count', result.get('count', 0))}), hoge mails {result.get('total_high_count', 0)} (actueel {result.get('total_high_attention_now_count', 0)}, niet actueel {result.get('total_high_stale_attention_count', 0)}), reply {result.get('total_reply_needed_count', 0)}"
        ]
        for group in items[:10]:
            urgency = '‼️' if group.get('urgency') == 'high' else '•'
            age = f" ({group.get('latest_age_hint')})" if group.get('latest_age_hint') else ''
            subject = group.get('latest_subject') or '(geen onderwerp)'
            line = f"{urgency} {format_cluster_hint(group, include_age=False)}: {subject}{age}"
            if show_preview and group.get('latest_preview'):
                line += f" — {group['latest_preview'][:140]}"
            lines.append(line)
        return '\n'.join(lines)

    if not items:
        return f"Mail triage ({result.get('scope', 'mail')}): 0 items, hoog 0, reply 0"

    lines = [
        f"Mail triage ({result.get('scope', 'mail')}): {result.get('count', 0)} items (totaal {result.get('total_count', result.get('count', 0))}), hoog {result.get('high_count', 0)}, reply {result.get('reply_needed_count', 0)}"
    ]
    top_groups = result.get('top_related_groups') or []
    if top_groups:
        group_bits = [format_cluster_hint(group, include_age=True) for group in top_groups[:2]]
        remaining = max(0, len(top_groups) - len(group_bits))
        suffix = f" +{remaining} cluster(s)" if remaining else ''
        lines.append(f"Clusters: {'; '.join(group_bits)}{suffix}")
    for item in items[:10]:
        urgency = '‼️' if item.get('urgency') == 'high' else '•'
        reply = ' ↩' if item.get('reply_needed') else ''
        deadline = f" ⏰{item.get('deadline_hint')}" if item.get('deadline_hint') else ''
        attach = format_attachment_hint(item)
        security = format_security_alert_hint(item)
        burst = f" ({item.get('related_group_size', 0)}x verwant)" if (item.get('related_group_size', 0) or 0) > 1 else ''
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        stale = ' [niet actueel]' if item.get('stale_attention') else ''
        line = f"{urgency} #{item.get('uid', '?')} {item.get('from', 'onbekend')}: {item.get('subject', '(geen onderwerp)')}{attach}{security} [{item.get('action_hint', 'ter info')}{reply}]{deadline}{burst}{age}{stale}"
        if show_preview and item.get('preview'):
            line += f" — {item['preview'][:140]}"
        lines.append(line)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Prioriteer ongelezen of recente mail met actiehints en reply-signalen')
    parser.add_argument('-n', '--limit', type=int, default=10)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--all', '--recent', dest='all', action='store_true', help='gebruik recente mail in plaats van alleen ongelezen')
    parser.add_argument('--reply-only', action='store_true', help='toon alleen mails waar waarschijnlijk antwoord op nodig is')
    parser.add_argument('--high-only', action='store_true', help='toon alleen high-urgency mails')
    parser.add_argument('--current-only', action='store_true', help='toon alleen mails of clusters die volgens de heuristiek nu nog actueel aandacht vragen')
    parser.add_argument('--clusters', '--clusters-only', dest='clusters', action='store_true', help='toon gegroepeerde mailclusters in plaats van losse mails')
    parser.add_argument('--search-limit', type=int, default=50, help='kijk verder terug in recente mail om burst/urgentie beter samen te vatten')
    args = parser.parse_args()

    result = triage(
        limit=max(1, min(args.limit, 20)),
        unread_only=not args.all,
        reply_only=args.reply_only,
        high_only=args.high_only,
        current_only=args.current_only,
        search_limit=max(1, min(args.search_limit, 200)),
        clusters_only=args.clusters,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result, show_preview=args.preview))


if __name__ == '__main__':
    main()
