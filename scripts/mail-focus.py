#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

from mail_heuristics import (
    format_attachment_hint,
    format_security_alert_hint,
    is_self_message,
    is_test_message,
    message_needs_review,
    needs_attention_now,
    summarize_security_alerts,
)


def normalize_subject(value):
    value = ' '.join((value or '').split())
    while True:
        updated = re.sub(r'^(?:(?:re|fw|fwd|aw|sv)\s*:\s*)+', '', value, flags=re.I).strip()
        if updated == value:
            break
        value = updated
    return value or '(geen onderwerp)'


def burst_count(items, item):
    if not item:
        return 0
    subject = normalize_subject(item.get('subject'))
    sender = (item.get('sender_email') or item.get('from') or '').strip().lower()
    count = 0
    for candidate in items or []:
        candidate_subject = normalize_subject(candidate.get('subject'))
        candidate_sender = (candidate.get('sender_email') or candidate.get('from') or '').strip().lower()
        if candidate_subject == subject and candidate_sender == sender:
            count += 1
    return count


def related_burst_items(items, item):
    if not item:
        return []
    sender = (item.get('sender_email') or item.get('from') or '').strip().lower()
    action = (item.get('action_hint') or '').strip().lower()
    if not sender or not action:
        subject = normalize_subject(item.get('subject'))
        return [
            candidate for candidate in (items or [])
            if normalize_subject(candidate.get('subject')) == subject
            and (candidate.get('sender_email') or candidate.get('from') or '').strip().lower() == sender
        ]

    focus_ts = item.get('date_ts')
    related = []
    for candidate in items or []:
        candidate_sender = (candidate.get('sender_email') or candidate.get('from') or '').strip().lower()
        candidate_action = (candidate.get('action_hint') or '').strip().lower()
        if candidate_sender != sender or candidate_action != action:
            continue
        candidate_ts = candidate.get('date_ts')
        if focus_ts and candidate_ts and abs(focus_ts - candidate_ts) > 6 * 3600:
            continue
        related.append(candidate)
    return related


def related_burst_count(items, item):
    return len(related_burst_items(items, item))


def load_burst_window(scope, limit, search_limit):
    burst_limit = max(limit, min(search_limit, 50))
    return load_triage_window(limit=burst_limit, unread_only=(scope == 'unread'))

ROOT = Path('/home/clawdy/.openclaw/workspace')
MAIL_TRIAGE = ROOT / 'scripts' / 'mail-triage.py'
MAIL_DRAFTS = ROOT / 'scripts' / 'mail-drafts.py'
MAIL_LATEST = ROOT / 'scripts' / 'mail-latest.py'


def pick_focus_item(items, allow_informational=True, current_only=False):
    items = items or []
    if not items:
        return None
    for item in items:
        if item.get('ephemeral_code'):
            continue
        if item.get('self_message') or is_self_message(item):
            continue
        if is_test_message(item):
            continue
        if current_only and not needs_attention_now(item):
            continue
        if allow_informational:
            return item
        if message_needs_review(item):
            return item
    return None


def load_triage_window(limit=10, unread_only=True):
    cmd = ['python3', str(MAIL_TRIAGE), '--json', '-n', str(limit)]
    if not unread_only:
        cmd.append('--all')
    return run_json(cmd, 'mail-triage')


def run_json(command, error_label):
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'{error_label} failed: {proc.returncode}')
    return json.loads(proc.stdout)


def load_meaningful_threads(limit, search_limit, current_only=False):
    command = [
        'python3', str(MAIL_LATEST), '--json', '--meaningful', '--threads',
        '-n', str(limit), '--search-limit', str(search_limit),
    ]
    if current_only:
        command.append('--current-only')
    return run_json(command, 'mail-latest') or []



def thread_is_useful_fallback(thread, current_only=False):
    thread = thread or {}
    if not thread:
        return False
    if current_only:
        return bool(thread.get('attention_now'))
    return bool(thread.get('review_worthy'))



def find_focus(limit=10, search_limit=50):
    limit = max(1, min(limit, 20))
    search_limit = max(limit, min(search_limit, 200))

    triage = load_triage_window(limit=limit, unread_only=True)
    scope = 'unread'
    item = None
    if not triage.get('items'):
        scope = 'latest'
        effective_limit = limit
        triage = load_triage_window(limit=effective_limit, unread_only=False)
        item = pick_focus_item(triage.get('items'), allow_informational=False, current_only=True)
        while not item and triage.get('count', 0) >= effective_limit and effective_limit < search_limit:
            effective_limit = min(search_limit, effective_limit * 2)
            triage = load_triage_window(limit=effective_limit, unread_only=False)
            item = pick_focus_item(triage.get('items'), allow_informational=False, current_only=True)
    else:
        item = pick_focus_item(triage.get('items'), allow_informational=False)

    drafts = run_json(
        ['python3', str(MAIL_DRAFTS), '--json', '-n', str(min(search_limit, max(limit, triage.get('count', 0) or limit)))] + (['--all'] if scope == 'latest' else ['--unread']),
        'mail-drafts',
    )

    if scope != 'unread':
        item = pick_focus_item(triage.get('items'), allow_informational=False, current_only=True)

    draft = None
    if item:
        for candidate in drafts.get('drafts') or []:
            if candidate.get('uid') == item.get('uid'):
                draft = candidate
                break

    items = triage.get('items') or []
    skipped_ephemeral = 0
    if item:
        for candidate in items:
            if candidate.get('uid') == item.get('uid'):
                break
            if candidate.get('ephemeral_code'):
                skipped_ephemeral += 1
    else:
        skipped_ephemeral = sum(1 for candidate in items if candidate.get('ephemeral_code'))

    meaningful_threads = []
    fallback_scope = None
    if not item:
        meaningful_threads = [
            thread for thread in load_meaningful_threads(limit, search_limit, current_only=True)
            if thread_is_useful_fallback(thread, current_only=True)
        ]
        if meaningful_threads:
            fallback_scope = 'current'
        else:
            meaningful_threads = [
                thread for thread in load_meaningful_threads(limit, search_limit, current_only=False)
                if thread_is_useful_fallback(thread, current_only=False)
            ]
            if meaningful_threads:
                fallback_scope = 'meaningful'

    burst_window = load_burst_window(scope, limit, search_limit)

    burst_items = (burst_window or {}).get('items') or items
    related_items = related_burst_items(burst_items, item)
    focus_item = dict(item) if item else None
    related_security_summary = summarize_security_alerts(related_items)
    if focus_item:
        focus_item['attention_now'] = needs_attention_now(focus_item)
        focus_item['stale_attention'] = not focus_item['attention_now']
    if focus_item and related_security_summary:
        focus_item['security_alert_summary'] = related_security_summary

    return {
        'scope': scope,
        'triage_count': triage.get('count', 0),
        'reply_needed_count': triage.get('reply_needed_count', 0),
        'high_count': triage.get('high_count', 0),
        'search_limit': search_limit,
        'skipped_ephemeral_count': skipped_ephemeral,
        'focus': focus_item,
        'focus_burst_count': burst_count(burst_items, item),
        'focus_related_burst_count': len(related_items),
        'draft': draft,
        'fallback_scope': fallback_scope,
        'fallback_thread': meaningful_threads[0] if meaningful_threads else None,
    }


def render_text(result, show_preview=False, show_draft=False):
    item = result.get('focus')
    if not item:
        skipped = result.get('skipped_ephemeral_count', 0)
        fallback = result.get('fallback_thread') or {}
        if fallback:
            participants = ', '.join((fallback.get('participants') or [])[:2]) or (fallback.get('latest_from') or 'onbekend')
            extra_people = max(0, len(fallback.get('participants') or []) - 2)
            if extra_people:
                participants += f' (+{extra_people})'
            time_bits = [bit for bit in [fallback.get('latest_age_hint'), fallback.get('span_hint')] if bit]
            time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
            stale = ' [niet actueel]' if fallback.get('stale_attention') else ''
            label = 'actuele betekenisvolle thread' if not fallback.get('stale_attention') else 'laatste betekenisvolle thread'
            return (
                'Geen directe mail-focus, '
                f"maar {label} is: {participants} — {fallback.get('subject', '(geen onderwerp)')} ({fallback.get('message_count', 0)}x{time_suffix}){stale}."
            )
        if skipped:
            return f'Geen duidelijke mail-focus gevonden, laatste window is vooral code-mail ({skipped}).'
        return 'Geen duidelijke mail-focus gevonden.'

    action = item.get('action_hint') or 'ter info'
    reply = ' ↩' if item.get('reply_needed') else ''
    deadline = f" ⏰{item.get('deadline_hint')}" if item.get('deadline_hint') else ''
    attach = format_attachment_hint(item)
    security = format_security_alert_hint(item)
    age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
    related_burst = result.get('focus_related_burst_count', 0)
    exact_burst = result.get('focus_burst_count', 0)
    burst = max(related_burst, exact_burst)
    burst_label = 'verwant' if related_burst > exact_burst else 'soortgelijk'
    burst_suffix = f" ({burst}x {burst_label})" if burst > 1 else ''
    stale = ' [niet actueel]' if item.get('stale_attention') else ''
    line = (
        f"Mail focus ({result.get('scope', 'mail')}): {item.get('from', 'onbekend')}"
        f" — {item.get('subject', '(geen onderwerp)')}{attach}{security} [{action}{reply}]{deadline}{burst_suffix}{age}{stale}"
    )
    if show_preview and item.get('preview'):
        line += f" — {item['preview'][:140]}"

    lines = [line]
    draft = result.get('draft')
    if show_draft and draft and draft.get('draft'):
        lines.append(f"Concept: {draft['draft']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Bepaal de ene beste mail om nu als eerste op te pakken')
    parser.add_argument('-n', '--limit', type=int, default=10)
    parser.add_argument('--search-limit', type=int, default=50, help='kijk verder terug als het eerste venster alleen code/noise bevat')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--draft', action='store_true', help='toon ook het bijpassende conceptantwoord als beschikbaar')
    args = parser.parse_args()

    result = find_focus(limit=args.limit, search_limit=args.search_limit)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result, show_preview=args.preview, show_draft=args.draft))


if __name__ == '__main__':
    main()
