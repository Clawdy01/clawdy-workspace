#!/usr/bin/env python3
import argparse
import email
import json
import pathlib
import re
from email.header import decode_header
from email.utils import parseaddr

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


def fetch_codes(limit=15, sender_filter=None, subject_filter=None):
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
            rows.append({
                'uid': uid,
                'from': sender,
                'subject': subject,
                'date': clean(dh(msg.get('Date'))),
                'codes': codes[:5],
                'verification_likely': verification_likely,
                'snippet': body[:240],
            })
    M.logout()
    return rows


def render(rows):
    if not rows:
        return 'Geen verificatiecodes gevonden'
    lines = [f'Verificatiecodes ({len(rows)})']
    for row in rows:
        code_text = ', '.join(row['codes']) if row['codes'] else 'geen code gevonden'
        lines.append(f"- #{row['uid']} {row['from']}: {row['subject']} [{code_text}]")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Zoek recente verificatiecodes in mailbox')
    parser.add_argument('-n', '--limit', type=int, default=15)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--sender')
    parser.add_argument('--subject')
    args = parser.parse_args()
    rows = fetch_codes(limit=max(1, min(args.limit, 50)), sender_filter=args.sender, subject_filter=args.subject)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render(rows))


if __name__ == '__main__':
    main()
