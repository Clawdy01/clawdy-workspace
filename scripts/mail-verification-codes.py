#!/usr/bin/env python3
import argparse
import email
import json
import pathlib
import re
from collections import OrderedDict
from datetime import UTC, datetime
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime

from mail_heuristics import format_recency_hint
from mail_imap import open_inbox

BASE = pathlib.Path('/home/clawdy/.openclaw/workspace/state')
DEFAULT_PATTERNS = [
    r'\b(\d{6})\b',
]
CONTEXT_PATTERNS = [
    r'(?:verification code|verify(?:ing)? code|security code|one[- ]time code|code is|code:|enter it)\D{0,40}(\d{4,8})\b',
]
BLOCKED_CODE_PATTERNS = [
    r'^\d{4}$',
    r'^(?:0?\d|1[0-2])(?:[0-5]\d)$',
]
CURRENT_WINDOW_SECONDS = 6 * 3600


def dh(v):
    if not v:
        return ''
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


def extract_text(msg):
    plain_parts = []
    html_parts = []
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
            if part.get_content_type() == 'text/plain':
                plain_parts.append(text)
            elif part.get_content_type() == 'text/html':
                html_parts.append(html_to_text(text))
    else:
        payload = msg.get_payload(decode=True)
        if payload is not None:
            charset = msg.get_content_charset() or 'utf-8'
            text = payload.decode(charset, errors='replace')
            if msg.get_content_type() == 'text/html':
                html_parts.append(html_to_text(text))
            else:
                plain_parts.append(text)
    text = '\n'.join(plain_parts + html_parts)
    return clean(text)


def looks_like_noise_code(code):
    return any(re.fullmatch(pattern, code) for pattern in BLOCKED_CODE_PATTERNS)


def find_codes(text, patterns):
    hits = []
    lowered = text.lower()

    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.I):
            code = match.group(1) if match.groups() else match.group(0)
            if code not in hits:
                hits.append(code)

    for pattern in CONTEXT_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.I):
            code = match.group(1) if match.groups() else match.group(0)
            if looks_like_noise_code(code):
                continue
            if code not in hits:
                hits.append(code)

    if hits:
        return hits

    if any(term in lowered for term in ['verification code', 'security code', 'one-time code', 'one time code']):
        for match in re.finditer(r'\b(\d{4,8})\b', text):
            code = match.group(1)
            if looks_like_noise_code(code):
                continue
            if code not in hits:
                hits.append(code)
    return hits


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


def is_current_code(row, now=None):
    date_ts = row.get('date_ts')
    if date_ts is None:
        return True
    now_dt = now.astimezone(UTC) if isinstance(now, datetime) else datetime.now(UTC)
    age_seconds = max(0, int(now_dt.timestamp() - date_ts))
    return age_seconds <= CURRENT_WINDOW_SECONDS


def finalize_row(row):
    row['current'] = is_current_code(row)
    row['age_hint'] = format_recency_hint(row.get('date_ts'))
    row['code_count'] = len(row.get('codes') or [])
    return row


def collapse_rows(rows):
    groups = OrderedDict()
    for row in rows:
        key = f"{clean(row.get('sender_email')).lower()}::{normalize_subject(row.get('subject'))}"
        current = groups.get(key)
        if current is None:
            grouped = dict(row)
            grouped['group_key'] = key
            grouped['duplicate_count'] = 1
            grouped['collapsed_count'] = 0
            grouped['codes'] = list(row.get('codes') or [])[:5]
            groups[key] = finalize_row(grouped)
            continue

        current['duplicate_count'] += 1
        current['collapsed_count'] = current['duplicate_count'] - 1
        for code in row.get('codes') or []:
            if code not in current['codes']:
                current['codes'].append(code)
        current['codes'] = current['codes'][:5]
    return [finalize_row(row) for row in groups.values()]


def fetch_codes(limit=15, sender_filter=None, subject_filter=None, collapse=True, current_only=False):
    M = open_inbox(readonly=True)
    status, data = M.uid('search', None, 'ALL')
    if status != 'OK':
        raise SystemExit('ERROR: search failed')
    uids = [int(x) for x in (data[0] or b'').split() if x.isdigit()]
    rows = []
    patterns = list(DEFAULT_PATTERNS)
    for uid in uids[-limit:][::-1]:
        st, msgdata = M.uid('fetch', str(uid), '(RFC822)')
        if st != 'OK' or not msgdata or not msgdata[0]:
            continue
        raw = msgdata[0][1]
        msg = email.message_from_bytes(raw)
        sender_name, sender_email = parseaddr(dh(msg.get('From')))
        sender = clean(sender_name) or clean(sender_email) or clean(dh(msg.get('From')))
        subject = clean(dh(msg.get('Subject'))) or '(geen onderwerp)'
        hay_sender = f'{sender} {sender_email}'.lower()
        hay_subject = subject.lower()
        if sender_filter and sender_filter.lower() not in hay_sender:
            continue
        if subject_filter and subject_filter.lower() not in hay_subject:
            continue
        body = extract_text(msg)
        codes = find_codes(f'{subject}\n{body}', patterns)
        verification_likely = any(term in f'{hay_sender} {hay_subject} {body.lower()[:2000]}' for term in [
            'verification', 'verify', 'verification code', 'get verification code', 'security code', 'one-time', 'one time', 'login', 'sign in', 'proton'
        ])
        include = False
        if sender_filter or subject_filter:
            include = bool(codes or verification_likely)
        else:
            include = bool(verification_likely)
        if include:
            rows.append(finalize_row({
                'uid': uid,
                'from': sender,
                'sender_email': clean(sender_email),
                'subject': subject,
                'subject_normalized': normalize_subject(subject),
                'date': clean(dh(msg.get('Date'))),
                'date_ts': parse_date_timestamp(dh(msg.get('Date'))),
                'codes': codes[:5],
                'verification_likely': verification_likely,
                'snippet': body[:240],
                'duplicate_count': 1,
                'collapsed_count': 0,
            }))
    M.logout()
    result_rows = collapse_rows(rows) if collapse else rows
    if current_only:
        result_rows = [row for row in result_rows if row.get('current')]
    return result_rows


def summarize_suppressed_row(row):
    return {
        'uid': row.get('uid'),
        'from': row.get('from'),
        'sender_email': row.get('sender_email'),
        'subject': row.get('subject'),
        'codes': row.get('codes') or [],
        'duplicate_count': row.get('duplicate_count') or 1,
        'collapsed_count': row.get('collapsed_count') or 0,
        'age_hint': row.get('age_hint'),
        'current': bool(row.get('current')),
        'reason': 'niet actueel',
    }



def render(rows, current_only=False):
    if not rows:
        return 'Geen actuele verificatiecodes gevonden' if current_only else 'Geen verificatiecodes gevonden'
    total_messages = sum(int(row.get('duplicate_count') or 1) for row in rows)
    lines = [f"Verificatiecodes ({len(rows)} groepen, {total_messages} mails)"]
    for row in rows:
        code_text = ', '.join(row['codes']) if row['codes'] else 'geen code gevonden'
        details = []
        if row.get('age_hint'):
            details.append(row['age_hint'])
        if row.get('duplicate_count', 1) > 1:
            details.append(f"{row['duplicate_count']} vergelijkbare mails")
        detail_text = f" ({'; '.join(details)})" if details else ''
        lines.append(f"- #{row['uid']} {row['from']}: {row['subject']} [{code_text}]{detail_text}")
    return '\n'.join(lines)



def build_response(rows, *, current_only=False, explain_empty=False, fallback_rows=None, sender_filter=None, subject_filter=None):
    payload = {
        'items': rows,
        'count': len(rows),
        'filters': {
            'current_only': current_only,
            'sender': sender_filter,
            'subject': subject_filter,
        },
        'suppressed_groups': [],
    }
    if explain_empty and not rows and current_only:
        fallback_rows = fallback_rows or []
        payload['suppressed_groups'] = [summarize_suppressed_row(row) for row in fallback_rows[:3] if not row.get('current')]
    return payload



def main():
    parser = argparse.ArgumentParser(description='Zoek recente verificatiecodes in mailbox')
    parser.add_argument('-n', '--limit', type=int, default=15)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--sender')
    parser.add_argument('--subject')
    parser.add_argument('--all', action='store_true', help='toon alle matches zonder samenklappen per vergelijkbare mailgroep')
    parser.add_argument('--current-only', action='store_true', help='toon alleen nog actuele verificatiecodes (standaardvenster: 6 uur)')
    parser.add_argument('--explain-empty', action='store_true', help='leg bij lege current-only codechecks compact uit welke codegroepen bewust zijn onderdrukt')
    args = parser.parse_args()
    limit = max(1, min(args.limit, 50))
    fallback_rows = fetch_codes(
        limit=limit,
        sender_filter=args.sender,
        subject_filter=args.subject,
        collapse=not args.all,
        current_only=False,
    ) if (args.explain_empty and args.current_only) else None
    rows = fallback_rows if (fallback_rows is not None and not args.current_only) else fetch_codes(
        limit=limit,
        sender_filter=args.sender,
        subject_filter=args.subject,
        collapse=not args.all,
        current_only=args.current_only,
    )
    if fallback_rows is not None and args.current_only:
        rows = [row for row in fallback_rows if row.get('current')]
    if args.explain_empty:
        payload = build_response(
            rows,
            current_only=args.current_only,
            explain_empty=True,
            fallback_rows=fallback_rows,
            sender_filter=args.sender,
            subject_filter=args.subject,
        )
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            text = render(rows, current_only=args.current_only)
            if not rows and payload.get('suppressed_groups'):
                lines = [text]
                for index, group in enumerate(payload['suppressed_groups'], start=1):
                    code_text = ', '.join(group.get('codes') or []) or 'geen code gevonden'
                    age = group.get('age_hint')
                    age_suffix = f" ({age})" if age else ''
                    count = group.get('duplicate_count') or 1
                    count_suffix = f"; {count} vergelijkbare mails" if count > 1 else ''
                    lines.append(f"- suppressed{index}: {group.get('from')}: {group.get('subject')} [{code_text}]{age_suffix}{count_suffix} | reason={group.get('reason')}")
                text = '\n'.join(lines)
            print(text)
        return
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render(rows, current_only=args.current_only))


if __name__ == '__main__':
    main()
