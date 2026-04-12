#!/usr/bin/env python3
import email
import json
import pathlib
import re
import sys
from email.header import decode_header
from email.utils import parseaddr

from mail_imap import load_mail_config, open_inbox
from mail_heuristics import detect_urgency, is_self_message, sanitize_preview


def dh(v):
    if not v:
        return ""
    parts = []
    for text, enc in decode_header(v):
        if isinstance(text, bytes):
            parts.append(text.decode(enc or "utf-8", errors="replace"))
        else:
            parts.append(text)
    return "".join(parts)


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "")).strip()


def html_to_text(value):
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return clean_text(value)


def extract_preview(msg):
    candidates = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition", "").lower().startswith("attachment"):
                continue
            try:
                payload = part.get_payload(decode=True)
            except Exception:
                payload = None
            if payload is None:
                continue
            charset = part.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")
            ctype = part.get_content_type()
            if ctype == "text/plain":
                return clean_text(text)[:160]
            if ctype == "text/html":
                candidates.append(html_to_text(text))
    else:
        try:
            payload = msg.get_payload(decode=True)
        except Exception:
            payload = None
        if payload is not None:
            charset = msg.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")
            if msg.get_content_type() == "text/html":
                return html_to_text(text)[:160]
            return clean_text(text)[:160]
    for candidate in candidates:
        if candidate:
            return candidate[:160]
    return ""


base = pathlib.Path("/home/clawdy/.openclaw/workspace/state")
conf = load_mail_config()
state_path = base / "mail-state.json"
state = {"last_uid": 0, "notified_uids": []}
if state_path.exists():
    try:
        state.update(json.loads(state_path.read_text()))
    except Exception:
        pass

notified_uids = {
    int(uid)
    for uid in state.get("notified_uids", [])
    if str(uid).isdigit()
}

M = open_inbox(readonly=True)
status, data = M.uid("search", None, "ALL")
if status != "OK":
    print("ERROR: search failed")
    sys.exit(1)

uids = [int(x) for x in (data[0] or b"").split() if x.isdigit()]
last_uid = int(state.get("last_uid", 0))
new = [u for u in uids if u > last_uid and u not in notified_uids]
if not new:
    print("NO_NEW_MAIL")
    M.logout()
    sys.exit(0)

summary = []
for uid in new[-10:]:
    st, msgdata = M.uid("fetch", str(uid), "(RFC822)")
    if st != "OK" or not msgdata or not msgdata[0]:
        continue
    raw = msgdata[0][1]
    msg = email.message_from_bytes(raw)
    sender_name, sender_email = parseaddr(dh(msg.get("From")))
    sender_name = clean_text(sender_name)
    sender_email = clean_text(sender_email)
    sender_display = sender_name or sender_email or dh(msg.get("From"))
    subject = clean_text(dh(msg.get("Subject")))
    preview = extract_preview(msg)
    item = {
        "uid": uid,
        "from": dh(msg.get("From")),
        "sender_name": sender_name,
        "sender_email": sender_email,
        "sender_display": sender_display,
        "subject": subject,
        "date": dh(msg.get("Date")),
        "preview": preview,
        "urgency": detect_urgency(sender_display, subject, preview),
    }
    item["self_message"] = is_self_message(item)
    item["preview"] = sanitize_preview(item, preview)
    summary.append(item)

state["last_uid"] = max(uids) if uids else last_uid
state["notified_uids"] = sorted((notified_uids | set(new)))[-500:]
state_path.write_text(json.dumps(state, indent=2) + "\n")
print(json.dumps({"new_count": len(new), "messages": summary}, ensure_ascii=False))
M.logout()
