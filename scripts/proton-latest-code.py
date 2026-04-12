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
    return clean('\n'.join(plain_parts + html_parts))


def main():
    p = argparse.ArgumentParser(description='Find latest Proton verification code, optionally newer than a uid')
    p.add_argument('--min-uid', type=int, default=0)
    p.add_argument('--json', action='store_true')
    args = p.parse_args()

    M = open_inbox(readonly=True)
    status, data = M.uid('search', None, 'ALL')
    if status != 'OK':
        raise SystemExit('search failed')
    uids = [int(x) for x in (data[0] or b'').split() if x.isdigit() and int(x) > args.min_uid]
    found = None
    for uid in uids[::-1]:
        st, msgdata = M.uid('fetch', str(uid), '(RFC822)')
        if st != 'OK' or not msgdata or not msgdata[0]:
            continue
        msg = email.message_from_bytes(msgdata[0][1])
        sender_name, sender_email = parseaddr(dh(msg.get('From')))
        sender = clean(sender_name) or clean(sender_email) or clean(dh(msg.get('From')))
        subject = clean(dh(msg.get('Subject')))
        if 'proton' not in sender.lower() or 'verification code' not in subject.lower():
            continue
        text = extract_text(msg)
        m = re.search(r'\b(\d{6})\b', f'{subject}\n{text}')
        found = {
            'uid': uid,
            'from': sender,
            'subject': subject,
            'date': clean(dh(msg.get('Date'))),
            'code': m.group(1) if m else None,
            'snippet': text[:240],
        }
        break
    M.logout()
    if args.json:
        print(json.dumps(found or {}, ensure_ascii=False, indent=2))
    elif found:
        print(found['code'] or '')
    else:
        print('')

if __name__ == '__main__':
    main()
