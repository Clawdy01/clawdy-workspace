#!/usr/bin/env python3
import argparse
import email
import html
import json
import re
import shlex
import subprocess
from collections import OrderedDict
from email.header import decode_header
from email.utils import parseaddr
from pathlib import Path
from urllib.parse import urlparse

from mail_draft_helpers import draft_for_thread
from mail_imap import open_inbox
from mail_heuristics import (
    format_attachment_hint,
    format_recency_hint,
    format_security_alert_hint,
    format_span_hint,
    group_needs_review,
    security_group_key,
    summarize_security_alerts,
)

ROOT = Path('/home/clawdy/.openclaw/workspace')
MAIL_LATEST = ROOT / 'scripts' / 'mail-latest.py'


def run_json(command, label):
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'{label} failed: {proc.returncode}')
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'invalid json from {label}: {exc}')


def dh(value):
    if not value:
        return ''
    parts = []
    for text, enc in decode_header(value):
        if isinstance(text, bytes):
            parts.append(text.decode(enc or 'utf-8', errors='replace'))
        else:
            parts.append(text)
    return ''.join(parts)


def clean(value):
    return ' '.join((value or '').split())


def html_to_text(value):
    value = re.sub(r'<script\b[^>]*>.*?</script>', ' ', value, flags=re.I | re.S)
    value = re.sub(r'<style\b[^>]*>.*?</style>', ' ', value, flags=re.I | re.S)
    value = re.sub(r'<[^>]+>', ' ', value)
    return clean(value)


def extract_text_and_links(msg):
    plain_parts = []
    html_parts = []
    links = []
    if msg.is_multipart():
        parts = msg.walk()
    else:
        parts = [msg]

    for part in parts:
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition', '').lower().startswith('attachment'):
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        charset = part.get_content_charset() or 'utf-8'
        text = payload.decode(charset, errors='replace')
        ctype = part.get_content_type()
        if ctype == 'text/plain':
            plain_parts.append(text)
            links.extend(re.findall(r'https?://[^\s<>")\]]+', text, flags=re.I))
        elif ctype == 'text/html':
            html_parts.append(html_to_text(text))
            links.extend(re.findall(r'href=["\'](https?://[^"\']+)["\']', text, flags=re.I))

    text = clean('\n'.join(plain_parts + html_parts))
    return text, links


def normalize_url(value):
    url = html.unescape((value or '').strip()).rstrip('.,);]')
    if not url.lower().startswith(('http://', 'https://')):
        return ''
    return url


def action_link_score(url, *, subject='', action_hint='', sender_email='', body=''):
    lowered = url.lower()
    score = 0
    if lowered.startswith('https://'):
        score += 2
    if any(term in lowered for term in ['verify', 'activate', 'confirm', 'login', 'signin', 'sign-in', 'security', 'password', 'vault']):
        score += 8
    if any(term in lowered for term in ['unsubscribe', 'preferences', 'privacy', 'terms', 'support', 'help', 'status', 'logo', 'image', 'cdn', 'community.']):
        score -= 10
    if sender_email:
        domain = sender_email.split('@')[-1].lower()
        host = (urlparse(url).hostname or '').lower()
        if domain and (host == domain or host.endswith('.' + domain)):
            score += 6
    combined = f'{subject} {action_hint} {body[:1200]}'.lower()
    if 'account activeren' in action_hint.lower() or 'verify' in combined or 'activate' in combined or 'confirm' in combined:
        if any(term in lowered for term in ['verify', 'activate', 'confirm']):
            score += 8
    if 'login-alert checken' in action_hint.lower() or 'security' in combined:
        if any(term in lowered for term in ['login', 'device', 'security', 'review']):
            score += 6
    return score


def extract_action_links(message, max_links=3):
    uid = message.get('uid')
    if uid is None:
        return []

    mailbox = open_inbox(readonly=True)
    try:
        status, msgdata = mailbox.uid('fetch', str(uid), '(RFC822)')
        if status != 'OK' or not msgdata or not msgdata[0]:
            return []
        raw = msgdata[0][1]
        msg = email.message_from_bytes(raw)
        sender_name, sender_email = parseaddr(dh(msg.get('From')))
        sender_email = clean(sender_email).lower()
        subject = clean(dh(msg.get('Subject'))) or (message.get('subject') or '')
        body_text, raw_links = extract_text_and_links(msg)
    finally:
        try:
            mailbox.logout()
        except Exception:
            pass

    unique = []
    seen = set()
    for candidate in raw_links:
        normalized = normalize_url(candidate)
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(normalized)

    ranked = sorted(
        unique,
        key=lambda url: action_link_score(
            url,
            subject=subject,
            action_hint=message.get('action_hint') or '',
            sender_email=sender_email,
            body=body_text,
        ),
        reverse=True,
    )
    links = []
    for url in ranked:
        score = action_link_score(
            url,
            subject=subject,
            action_hint=message.get('action_hint') or '',
            sender_email=sender_email,
            body=body_text,
        )
        if score < 6:
            continue
        links.append(url)
        if len(links) >= max_links:
            break
    return links


def normalize_subject(value):
    value = ' '.join((value or '').split())
    while True:
        updated = re.sub(r'^(?:(?:re|fw|fwd|aw|sv)\s*:\s*)+', '', value, flags=re.I).strip()
        if updated == value:
            break
        value = updated
    return value or '(geen onderwerp)'


def thread_key_for(row):
    normalized = normalize_subject(row.get('subject'))
    sender = ' '.join((row.get('sender_email') or row.get('from') or '').split()).lower()
    action = ' '.join((row.get('action_hint') or '').split()).lower()
    urgency = ' '.join((row.get('urgency') or '').split()).lower()
    date_ts = row.get('date_ts') or 0
    security_key = security_group_key(row)

    if sender and action and security_key:
        return f'security::{sender}::{action}::{security_key}'
    if sender and action and row.get('no_reply') and urgency == 'high':
        bucket = int(date_ts // (6 * 3600)) if date_ts else 0
        return f'alert::{sender}::{action}::{bucket}'
    if normalized == '(geen onderwerp)' and sender:
        return f'{sender}::{normalized}'
    return normalized.lower()


def load_rows(limit, search_limit, meaningful_only=False, current_only=False, unread_only=False):
    command = [
        'python3', str(MAIL_LATEST), '--json', '-n', str(search_limit), '--search-limit', str(search_limit)
    ]
    if meaningful_only:
        command.append('--meaningful')
    if current_only:
        command.append('--current-only')
    if unread_only:
        command.append('--unread')
    rows = run_json(command, 'mail-latest') or []
    return rows[:max(limit, search_limit)]


def build_threads(rows):
    threads = OrderedDict()
    for row in rows:
        key = thread_key_for(row)
        thread = threads.setdefault(key, {
            'thread_key': key,
            'subject': normalize_subject(row.get('subject')),
            'latest_subject': row.get('subject') or '(geen onderwerp)',
            'subject_variants': [],
            'subject_variant_count': 0,
            'latest_uid': row.get('uid'),
            'latest_from': row.get('from'),
            'latest_date': row.get('date'),
            'latest_date_ts': row.get('date_ts'),
            'oldest_date_ts': row.get('date_ts'),
            'latest_age_hint': '',
            'span_hint': '',
            'latest_preview': row.get('preview'),
            'urgency': row.get('urgency'),
            'action_hint': row.get('action_hint'),
            'reply_needed': bool(row.get('reply_needed')),
            'deadline_hint': row.get('deadline_hint'),
            'message_count': 0,
            'participants': [],
            'messages': [],
            'attachment_count': 0,
            'attachment_names': [],
            'security_alert_details': [],
            'security_alert_summary': '',
            'expected_security_change': True,
            'attention_now': False,
            'stale_attention': False,
            'no_reply_only': True,
            'review_worthy': False,
        })
        thread['message_count'] += 1
        thread['attachment_count'] += int(row.get('attachment_count') or 0)
        current_ts = row.get('date_ts')
        latest_ts = thread.get('latest_date_ts')
        if current_ts is not None and (latest_ts is None or current_ts > latest_ts):
            thread['latest_uid'] = row.get('uid')
            thread['latest_from'] = row.get('from')
            thread['latest_date'] = row.get('date')
            thread['latest_date_ts'] = current_ts
            thread['latest_preview'] = row.get('preview')
            thread['latest_subject'] = row.get('subject') or '(geen onderwerp)'
        subject = row.get('subject') or '(geen onderwerp)'
        if subject not in thread['subject_variants']:
            thread['subject_variants'].append(subject)
            thread['subject_variant_count'] = len(thread['subject_variants'])
        if row.get('urgency') == 'high':
            thread['urgency'] = 'high'
        if row.get('reply_needed'):
            thread['reply_needed'] = True
        if not thread.get('deadline_hint') and row.get('deadline_hint'):
            thread['deadline_hint'] = row.get('deadline_hint')
        if not thread.get('action_hint') and row.get('action_hint'):
            thread['action_hint'] = row.get('action_hint')
        if row.get('from') and row.get('from') not in thread['participants']:
            thread['participants'].append(row['from'])
        for name in row.get('attachment_names') or []:
            if name and name not in thread['attachment_names']:
                thread['attachment_names'].append(name)
        if row.get('security_alert_details'):
            thread['security_alert_details'].append(row['security_alert_details'])
        thread['expected_security_change'] = thread['expected_security_change'] and bool(row.get('expected_security_change'))
        current_ts = row.get('date_ts')
        oldest_ts = thread.get('oldest_date_ts')
        if current_ts is not None and (oldest_ts is None or current_ts < oldest_ts):
            thread['oldest_date_ts'] = current_ts
        thread['attention_now'] = thread['attention_now'] or bool(row.get('attention_now'))
        thread['no_reply_only'] = thread['no_reply_only'] and bool(row.get('no_reply'))
        thread['messages'].append(dict(row))

    thread_list = list(threads.values())
    for thread in thread_list:
        if thread.get('security_alert_details'):
            detail_messages = [{'security_alert_details': detail} for detail in thread['security_alert_details']]
            thread['security_alert_summary'] = summarize_security_alerts(detail_messages)
        thread['latest_age_hint'] = format_recency_hint(thread.get('latest_date_ts'))
        thread['span_hint'] = format_span_hint(thread.get('oldest_date_ts'), thread.get('latest_date_ts'))
        thread['messages'].sort(key=lambda item: (item.get('date_ts') is None, -(item.get('date_ts') or 0), -int(item.get('uid') or 0)))
        thread['stale_attention'] = not thread.get('attention_now', False)
        thread['review_worthy'] = group_needs_review(thread)
    thread_list.sort(key=lambda item: (item.get('latest_date_ts') is None, -(item.get('latest_date_ts') or 0), -int(item.get('latest_uid') or 0)))
    return thread_list


def matches_filter(thread, *, uid_filter=None, sender_filter=None, subject_filter=None, action_filter=None):
    if uid_filter is not None:
        message_uids = {int(msg.get('uid')) for msg in (thread.get('messages') or []) if msg.get('uid') is not None}
        latest_uid = thread.get('latest_uid')
        if uid_filter not in message_uids and latest_uid != uid_filter:
            return False

    sender_filter = (sender_filter or '').strip().lower()
    subject_filter = (subject_filter or '').strip().lower()
    action_filter = (action_filter or '').strip().lower()
    if sender_filter:
        haystacks = [
            (thread.get('latest_from') or '').lower(),
            ' '.join((thread.get('participants') or [])).lower(),
            ' '.join((msg.get('sender_email') or '') for msg in (thread.get('messages') or [])).lower(),
        ]
        if not any(sender_filter in haystack for haystack in haystacks):
            return False
    if subject_filter:
        haystacks = [
            (thread.get('subject') or '').lower(),
            (thread.get('latest_subject') or '').lower(),
        ]
        if not any(subject_filter in haystack for haystack in haystacks):
            return False
    if action_filter:
        actions = [(msg.get('action_hint') or '').lower() for msg in (thread.get('messages') or [])]
        if not any(action_filter in action for action in actions):
            return False
    return True


def pick_thread(threads, *, uid_filter=None, sender_filter=None, subject_filter=None, action_filter=None, current_only=False, review_worthy_only=False):
    filtered = [
        thread for thread in threads
        if matches_filter(thread, uid_filter=uid_filter, sender_filter=sender_filter, subject_filter=subject_filter, action_filter=action_filter)
    ]
    if review_worthy_only:
        filtered = [thread for thread in filtered if thread.get('review_worthy')]
    if current_only:
        current = [thread for thread in filtered if thread.get('attention_now')]
        return (current[0], filtered) if current else (None, filtered)
    preferred = [thread for thread in filtered if thread.get('review_worthy')]
    if preferred:
        return preferred[0], filtered
    return (filtered[0], filtered) if filtered else (None, filtered)


def attach_action_links(thread):
    thread = thread or {}
    messages = thread.get('messages') or []
    combined = []
    seen = set()
    for item in messages[:3]:
        links = extract_action_links(item, max_links=3)
        item['action_links'] = links
        for url in links:
            key = url.lower()
            if key in seen:
                continue
            seen.add(key)
            combined.append(url)
    thread['action_links'] = combined[:5]
    return thread


def shell_join(parts):
    return ' '.join(shlex.quote(str(part)) for part in parts)


def render_text(result, show_preview=False, show_draft=False, message_limit=8):
    thread = result.get('thread')
    if not thread:
        reason = result.get('reason') or 'geen passende mailthread gevonden'
        route = result.get('recommended_route') or 'noop'
        command = result.get('recommended_command')
        lines = ['Mail thread']
        lines.append(f"- next={route}, reason={reason}")
        if command:
            lines.append(f"- check={command}")
        return '\n'.join(lines)

    participants = ', '.join((thread.get('participants') or [])[:3]) or (thread.get('latest_from') or 'onbekend')
    extra_people = max(0, len(thread.get('participants') or []) - 3)
    if extra_people:
        participants += f' (+{extra_people})'
    deadline = f" ⏰{thread.get('deadline_hint')}" if thread.get('deadline_hint') else ''
    stale = ' [niet actueel]' if thread.get('stale_attention') else ''
    reply = ' ↩' if thread.get('reply_needed') else ''
    variant_suffix = f", +{thread.get('subject_variant_count', 0) - 1} variant(en)" if (thread.get('subject_variant_count', 0) or 0) > 1 else ''
    time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
    time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
    lines = [
        f"Mailthread: {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{variant_suffix}{time_suffix})"
        f"\nVan: {participants}"
        f"\nFocus: {thread.get('action_hint') or 'ter info'}{reply}{deadline}{format_attachment_hint(thread)}{format_security_alert_hint(thread)}{stale}"
    ]

    messages = thread.get('messages') or []
    for item in messages[:max(1, message_limit)]:
        urgency = '‼️' if item.get('urgency') == 'high' else '-'
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        reply_hint = ' ↩' if item.get('reply_needed') else ''
        stale = ' [niet actueel]' if item.get('stale_attention') else ''
        line = (
            f"{urgency} #{item.get('uid')} {item.get('from')}: {item.get('subject')}"
            f" [{item.get('action_hint') or 'ter info'}{reply_hint}]"
            f"{format_attachment_hint(item)}{format_security_alert_hint(item)}{age}{stale}"
        )
        if show_preview and item.get('preview'):
            line += f" — {item['preview'][:160]}"
        lines.append(line)
        for link in (item.get('action_links') or [])[:2]:
            lines.append(f"  link: {link}")

    remaining = len(messages) - max(1, message_limit)
    if remaining > 0:
        lines.append(f"... +{remaining} oudere mail(s) in deze thread")

    if thread.get('action_links'):
        lines.append(f"Actielinks: {', '.join(thread.get('action_links')[:3])}")

    draft = result.get('draft')
    if show_draft and draft and draft.get('draft'):
        lines.append('')
        lines.append(f"Concept: {draft['draft']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Bekijk snel één recente mailthread met message-timeline')
    parser.add_argument('-n', '--limit', type=int, default=25, help='hoeveel recente mails maximaal meenemen in de thread-zoekruimte')
    parser.add_argument('--search-limit', type=int, default=50, help='hoe ver terug kijken in de mailbox')
    parser.add_argument('--meaningful', action='store_true', help='filter code/noise/self/test weg voor threadselectie')
    parser.add_argument('--current-only', action='store_true', help='kies alleen een thread die nu nog actueel aandacht vraagt')
    parser.add_argument('--review-worthy', action='store_true', help='beperk threadselectie tot threads die nog echt reviewwaardig zijn')
    parser.add_argument('--unread', action='store_true', help='beperk de zoekruimte tot unread mail')
    parser.add_argument('--uid', type=int, help='kies exact de thread waar dit message uid in zit')
    parser.add_argument('--sender', help='filter op afzender of sender email')
    parser.add_argument('--subject', help='filter op onderwerp')
    parser.add_argument('--action', help='filter op actiehint, bijvoorbeeld "reply" of "login-alert"')
    parser.add_argument('--messages', type=int, default=8, help='hoeveel berichten uit de gekozen thread tonen')
    parser.add_argument('--preview', action='store_true', help='toon ook previews per bericht')
    parser.add_argument('--draft', action='store_true', help='toon ook een bestaand concept dat bij deze thread hoort')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    search_limit = max(1, min(args.search_limit, 200))
    rows = load_rows(
        limit=max(1, min(args.limit, 200)),
        search_limit=search_limit,
        meaningful_only=args.meaningful,
        current_only=False,
        unread_only=args.unread,
    )
    threads = build_threads(rows)
    thread, filtered_threads = pick_thread(
        threads,
        uid_filter=args.uid,
        sender_filter=args.sender,
        subject_filter=args.subject,
        action_filter=args.action,
        current_only=args.current_only,
        review_worthy_only=args.review_worthy,
    )
    if thread:
        thread = attach_action_links(thread)

    draft = draft_for_thread(thread) if args.draft and thread else None

    command = ['python3', 'scripts/mail-dispatch.py', 'thread']
    if args.uid is not None:
        command += ['--uid', str(args.uid)]
    if args.sender:
        command += ['--sender', args.sender]
    if args.subject:
        command += ['--subject', args.subject]
    if args.action:
        command += ['--action', args.action]
    command += ['--messages', str(max(1, min(args.messages, 30)))]
    if args.meaningful:
        command.append('--meaningful')
    if args.current_only:
        command.append('--current-only')
    if args.review_worthy:
        command.append('--review-worthy')
    if args.unread:
        command.append('--unread')
    if args.preview:
        command.append('--preview')
    if args.draft:
        command.append('--draft')

    reason = None
    recommended_route = 'review-thread'
    recommended_command = shell_join(command)
    if not thread:
        recommended_route = 'noop'
        if args.review_worthy and args.current_only:
            reason = 'geen actuele reviewwaardige mailthread'
        elif args.review_worthy:
            reason = 'geen reviewwaardige mailthread'
        elif args.current_only:
            reason = 'geen actuele mailthread'
        else:
            reason = 'geen passende mailthread gevonden'
        fallback_command = ['python3', 'scripts/mail-dispatch.py', 'latest']
        if args.meaningful:
            fallback_command.append('--meaningful')
        if args.review_worthy:
            fallback_command.append('--review-worthy')
        elif args.current_only:
            fallback_command.append('--current-only')
        if args.unread:
            fallback_command.append('--unread')
        if args.sender:
            fallback_command += ['--sender', args.sender]
        if args.subject:
            fallback_command += ['--subject', args.subject]
        if args.action:
            fallback_command += ['--action', args.action]
        if args.search_limit != 50:
            fallback_command += ['--search-limit', str(search_limit)]
        recommended_command = shell_join(fallback_command)

    result = {
        'search_limit': search_limit,
        'thread_count': len(threads),
        'filtered_thread_count': len(filtered_threads),
        'thread': thread,
        'draft': draft,
        'command': shell_join(command),
        'recommended_route': recommended_route,
        'recommended_command': recommended_command,
        'reason': reason,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result, show_preview=args.preview, show_draft=args.draft, message_limit=max(1, min(args.messages, 30))))


if __name__ == '__main__':
    main()
