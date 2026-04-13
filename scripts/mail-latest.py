#!/usr/bin/env python3
import argparse
import email
import json
import re
from collections import OrderedDict
from datetime import UTC
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime

from mail_imap import open_inbox
from mail_heuristics import (
    detect_urgency,
    extract_deadline_hint,
    extract_security_alert_details,
    format_attachment_hint,
    format_recency_hint,
    format_security_alert_hint,
    format_span_hint,
    group_needs_review,
    is_actionable_message,
    is_ephemeral_code_message,
    is_meaningful_message,
    is_no_reply_message,
    is_self_message,
    is_test_message,
    message_needs_review,
    needs_attention_now,
    reply_needed,
    sanitize_preview,
    security_group_key,
    suggest_action,
    summarize_security_alerts,
)


def dh(v):
    if not v:
        return ""
    parts = []
    for text, enc in decode_header(v):
        if isinstance(text, bytes):
            parts.append(text.decode(enc or 'utf-8', errors='replace'))
        else:
            parts.append(text)
    return ''.join(parts)


def clean(v):
    return ' '.join((v or '').split())


def html_to_text(value):
    value = re.sub(r'<script\b[^>]*>.*?</script>', ' ', value, flags=re.I | re.S)
    value = re.sub(r'<style\b[^>]*>.*?</style>', ' ', value, flags=re.I | re.S)
    value = re.sub(r'<[^>]+>', ' ', value)
    return clean(value)


def extract_preview(msg):
    candidates = []
    if msg.is_multipart():
        for part in msg.walk():
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
                return clean(text)[:160]
            if ctype == 'text/html':
                candidates.append(html_to_text(text))
    else:
        payload = msg.get_payload(decode=True)
        if payload is not None:
            charset = msg.get_content_charset() or 'utf-8'
            text = payload.decode(charset, errors='replace')
            if msg.get_content_type() == 'text/html':
                return html_to_text(text)[:160]
            return clean(text)[:160]
    for candidate in candidates:
        if candidate:
            return candidate[:160]
    return ''


def extract_attachment_info(msg):
    count = 0
    names = []
    seen = set()

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        filename = clean(dh(part.get_filename()))
        disposition = (part.get('Content-Disposition', '') or '').lower()
        if not filename and 'attachment' not in disposition:
            continue
        count += 1
        if filename and filename.lower() not in seen:
            seen.add(filename.lower())
            names.append(filename)

    return {
        'attachment_count': count,
        'attachment_names': names[:5],
    }


def parse_date_timestamp(value):
    value = clean(value)
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.timestamp()


def normalize_subject(value):
    value = clean(value or '')
    while True:
        updated = re.sub(r'^(?:(?:re|fw|fwd|aw|sv)\s*:\s*)+', '', value, flags=re.I).strip()
        if updated == value:
            break
        value = updated
    return value or '(geen onderwerp)'


def thread_key_for(row):
    normalized = normalize_subject(row.get('subject'))
    sender = clean(row.get('sender_email') or row.get('from') or '').lower()
    action = clean(row.get('action_hint')).lower()
    urgency = clean(row.get('urgency')).lower()
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


def group_threads(rows, limit):
    threads = OrderedDict()
    for row in rows:
        key = thread_key_for(row)
        thread = threads.setdefault(key, {
            'thread_key': key,
            'subject': normalize_subject(row.get('subject')),
            'latest_subject': row.get('subject') or '(geen onderwerp)',
            'latest_uid': row.get('uid'),
            'latest_from': row.get('from'),
            'latest_date': row.get('date'),
            'latest_date_ts': row.get('date_ts'),
            'latest_preview': row.get('preview'),
            'urgency': row.get('urgency'),
            'message_count': 0,
            'attachment_count': 0,
            'attachment_names': [],
            'participants': [],
            'subject_variants': [],
            'subject_variant_count': 0,
            'ephemeral_only': True,
            'no_reply_only': True,
            'action_hint': row.get('action_hint'),
            'reply_needed': row.get('reply_needed'),
            'deadline_hint': row.get('deadline_hint'),
            'security_alert_details': [],
            'security_alert_summary': '',
            'oldest_date': row.get('date'),
            'oldest_date_ts': row.get('date_ts'),
            'attention_now': False,
            'stale_attention': False,
        })
        thread['message_count'] += 1
        thread['attachment_count'] += int(row.get('attachment_count') or 0)
        current_ts = row.get('date_ts')
        latest_ts = thread.get('latest_date_ts')
        oldest_ts = thread.get('oldest_date_ts')
        if current_ts is not None and (latest_ts is None or current_ts > latest_ts):
            thread['latest_date_ts'] = current_ts
            thread['latest_date'] = row.get('date')
            thread['latest_uid'] = row.get('uid')
            thread['latest_from'] = row.get('from')
            thread['latest_preview'] = row.get('preview')
            thread['latest_subject'] = row.get('subject') or '(geen onderwerp)'
        if current_ts is not None and (oldest_ts is None or current_ts < oldest_ts):
            thread['oldest_date_ts'] = current_ts
            thread['oldest_date'] = row.get('date')
        subject = normalize_subject(row.get('subject'))
        if subject not in thread['subject_variants']:
            thread['subject_variants'].append(subject)
            thread['subject_variant_count'] = len(thread['subject_variants'])
        for name in row.get('attachment_names') or []:
            if name and name not in thread['attachment_names']:
                thread['attachment_names'].append(name)
        sender = row.get('from')
        if sender and sender not in thread['participants']:
            thread['participants'].append(sender)
        thread['ephemeral_only'] = thread['ephemeral_only'] and bool(row.get('ephemeral_code'))
        thread['no_reply_only'] = thread['no_reply_only'] and bool(row.get('no_reply'))
        if row.get('urgency') == 'high':
            thread['urgency'] = 'high'
        if row.get('reply_needed'):
            thread['reply_needed'] = True
        if not thread.get('deadline_hint') and row.get('deadline_hint'):
            thread['deadline_hint'] = row.get('deadline_hint')
        if not thread.get('action_hint') and row.get('action_hint'):
            thread['action_hint'] = row.get('action_hint')
        if row.get('security_alert_details'):
            thread['security_alert_details'].append(row['security_alert_details'])
        thread['attention_now'] = thread['attention_now'] or needs_attention_now(row)

    thread_list = list(threads.values())
    for thread in thread_list:
        if thread.get('security_alert_details'):
            detail_messages = [{'security_alert_details': detail} for detail in thread['security_alert_details']]
            thread['security_alert_summary'] = summarize_security_alerts(detail_messages)
        thread['latest_age_hint'] = format_recency_hint(thread.get('latest_date_ts'))
        thread['span_hint'] = format_span_hint(thread.get('oldest_date_ts'), thread.get('latest_date_ts'))
        thread['stale_attention'] = not thread.get('attention_now', False)
        thread['review_worthy'] = group_needs_review(thread)
    return thread_list[:limit]


def matches_any_filter(value, filters):
    if not filters:
        return True
    haystack = clean(value).lower()
    return any(filter_value in haystack for filter_value in filters)



def matches_exact_or_substring(value, filters):
    if not filters:
        return True
    haystack = clean(value).lower()
    return any(filter_value == haystack or filter_value in haystack for filter_value in filters)



def fetch_latest(
    limit,
    unread_only=False,
    meaningful_only=False,
    actionable_only=False,
    search_limit=None,
    threads=False,
    current_only=False,
    review_worthy_only=False,
    sender_filters=None,
    subject_filters=None,
    action_filters=None,
    urgency_filters=None,
):
    sender_filters = [clean(value).lower() for value in (sender_filters or []) if clean(value)]
    subject_filters = [clean(value).lower() for value in (subject_filters or []) if clean(value)]
    action_filters = [clean(value).lower() for value in (action_filters or []) if clean(value)]
    urgency_filters = [clean(value).lower() for value in (urgency_filters or []) if clean(value)]

    M = open_inbox(readonly=True)
    query = '(UNSEEN)' if unread_only else 'ALL'
    status, data = M.uid('search', None, query)
    if status != 'OK':
        raise SystemExit('ERROR: search failed')
    uids = [int(x) for x in (data[0] or b'').split() if x.isdigit()]
    rows = []
    max_rows = max(limit, search_limit or limit)
    for uid in uids[-max_rows:][::-1]:
        st, msgdata = M.uid('fetch', str(uid), '(RFC822)')
        if st != 'OK' or not msgdata or not msgdata[0]:
            continue
        raw = msgdata[0][1]
        msg = email.message_from_bytes(raw)
        sender_name, sender_email = parseaddr(dh(msg.get('From')))
        sender = clean(sender_name) or clean(sender_email) or clean(dh(msg.get('From')))
        subject = clean(dh(msg.get('Subject'))) or '(geen onderwerp)'
        preview = extract_preview(msg)
        date_value = clean(dh(msg.get('Date')))
        row = {
            'uid': uid,
            'from': sender,
            'sender_display': sender,
            'sender_email': clean(sender_email),
            'subject': subject,
            'date': date_value,
            'date_ts': parse_date_timestamp(date_value),
            'preview': preview,
            'urgency': detect_urgency(sender, subject, preview),
        }
        row.update(extract_attachment_info(msg))
        row['has_attachments'] = bool(row.get('attachment_count'))
        row['self_message'] = is_self_message(row)
        row['preview'] = sanitize_preview(row, preview)
        row['ephemeral_code'] = is_ephemeral_code_message(row)
        row['no_reply'] = is_no_reply_message(row)
        row['deadline_hint'] = extract_deadline_hint(row)
        row['action_hint'] = suggest_action(row)
        row['reply_needed'] = reply_needed(row)
        row['security_alert_details'] = extract_security_alert_details(row)
        row['age_hint'] = format_recency_hint(row.get('date_ts'))
        row['attention_now'] = needs_attention_now(row)
        row['stale_attention'] = not row['attention_now']
        if not matches_any_filter(f"{row.get('from')} {row.get('sender_email')}", sender_filters):
            continue
        if not matches_any_filter(row.get('subject'), subject_filters):
            continue
        if not matches_exact_or_substring(row.get('action_hint'), action_filters):
            continue
        if not matches_exact_or_substring(row.get('urgency'), urgency_filters):
            continue
        rows.append(row)

    M.logout()

    rows.sort(key=lambda row: (row.get('date_ts') is None, -(row.get('date_ts') or 0), -int(row.get('uid') or 0)))

    if meaningful_only:
        rows = [row for row in rows if is_meaningful_message(row)]
    if actionable_only:
        rows = [row for row in rows if is_actionable_message(row)]
    if current_only:
        rows = [row for row in rows if row.get('attention_now')]
    if review_worthy_only:
        rows = [row for row in rows if message_needs_review(row)]

    if threads:
        grouped = group_threads(rows, limit=max(limit, search_limit or limit))
        if meaningful_only or actionable_only or review_worthy_only:
            grouped = [thread for thread in grouped if thread.get('review_worthy')]
        if current_only:
            grouped = [thread for thread in grouped if thread.get('attention_now')]
        return grouped[:limit]
    return rows[:limit]


def render(rows, show_preview=False, threads=False):
    if not rows:
        return 'Geen mail gevonden'
    if threads:
        lines = [f'Laatste mailthreads ({len(rows)})']
        for row in rows:
            prefix = '‼️' if row.get('urgency') == 'high' else '-'
            participants = ', '.join((row.get('participants') or [])[:2]) or (row.get('latest_from') or 'onbekend')
            extra_people = max(0, len(row.get('participants') or []) - 2)
            if extra_people:
                participants += f' (+{extra_people})'
            noise = ' [code-thread]' if row.get('ephemeral_only') else (' [no-reply]' if row.get('no_reply_only') else '')
            attach = format_attachment_hint(row, include_names=False)
            variants = f" +{row.get('subject_variant_count', 0) - 1} variant(en)" if (row.get('subject_variant_count', 0) or 0) > 1 else ''
            time_bits = [bit for bit in [row.get('latest_age_hint'), row.get('span_hint')] if bit]
            time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
            stale = ' [niet actueel]' if row.get('stale_attention') else ''
            line = f"{prefix} #{row['latest_uid']} {participants}: {row['subject']} ({row['message_count']}x{variants}{time_suffix}){attach}{format_security_alert_hint(row)}{noise}{stale}"
            if show_preview and row.get('latest_preview'):
                line += f" — {row['latest_preview']}"
            lines.append(line)
        return '\n'.join(lines)
    lines = [f'Laatste mail ({len(rows)})']
    for row in rows:
        prefix = '‼️' if row.get('urgency') == 'high' else '-'
        attach = format_attachment_hint(row, include_names=False)
        age = f" ({row['age_hint']})" if row.get('age_hint') else ''
        stale = ' [niet actueel]' if row.get('stale_attention') else ''
        line = f"{prefix} #{row['uid']} {row['from']}: {row['subject']}{attach}{format_security_alert_hint(row)}{age}{stale}"
        if show_preview and row.get('preview'):
            line += f" — {row['preview']}"
        lines.append(line)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Laatste mails snel bekijken zonder state te wijzigen')
    parser.add_argument('-n', '--limit', type=int, default=5)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--unread', action='store_true', help='toon alleen ongelezen mails')
    parser.add_argument('--meaningful', action='store_true', help='sla vluchtige/noisy mail over, maar behoud belangrijke geautomatiseerde alerts in de inbox-scan')
    parser.add_argument('--actionable', action='store_true', help='toon alleen mails/threads met duidelijke actiehint, reply-signaal, deadline of belangrijke alert')
    parser.add_argument('--current-only', action='store_true', help='toon alleen mails/threads die volgens de heuristiek nog actueel aandacht vragen')
    parser.add_argument('--review-worthy', action='store_true', help='toon alleen mails/threads die na actualiteitsfiltering nog echt reviewwaardig zijn')
    parser.add_argument('--threads', action='store_true', help='groepeer recente mails op onderwerp/thread zodat drukke conversaties compacter zichtbaar zijn')
    parser.add_argument('--sender', action='append', help='filter op afzendernaam of e-mailadres, herhaalbaar')
    parser.add_argument('--subject', action='append', help='filter op onderwerptekst, herhaalbaar')
    parser.add_argument('--action', action='append', help='filter op action_hint, bijvoorbeeld "antwoord overwegen" of "security checken"')
    parser.add_argument('--urgency', action='append', help='filter op urgency, bijvoorbeeld high of normal')
    parser.add_argument('--search-limit', type=int, default=50, help='kijk verder terug als filters of current-only aan staan en de bovenste mails vooral noise of oude alerts zijn')
    args = parser.parse_args()
    rows = fetch_latest(
        max(1, min(args.limit, 20)),
        unread_only=args.unread,
        meaningful_only=args.meaningful,
        actionable_only=args.actionable,
        search_limit=max(1, min(args.search_limit, 200)),
        threads=args.threads,
        current_only=args.current_only,
        review_worthy_only=args.review_worthy,
        sender_filters=args.sender,
        subject_filters=args.subject,
        action_filters=args.action,
        urgency_filters=args.urgency,
    )
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render(rows, show_preview=args.preview, threads=args.threads))


if __name__ == '__main__':
    main()
