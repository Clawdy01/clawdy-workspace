#!/usr/bin/env python3
import json
import re
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

URGENT_TERMS = [
    'urgent', 'spoed', 'asap', 'immediately', 'important', 'belangrijk',
    'action required', 'actie vereist', 'payment due', 'factuur', 'invoice',
    'security alert', 'verify', 'verification', 'wachtwoord', 'password reset',
]

DEADLINE_PATTERNS = [
    (r'\b(vandaag|today|vanmiddag|this afternoon|vanavond|tonight|morgen|tomorrow)\b', 'kortetermijn'),
    (r'\b(eod|end of day|einde van de dag|voor het einde van de dag)\b', 'vandaag'),
    (r'\b(deadline|due today|due tomorrow|uiterlijk|voor \d{1,2}[:.]\d{2})\b', 'deadline'),
    (r'\b(this morning|vanochtend|this evening)\b', 'vandaag'),
]

WEEKDAY_TERMS = (
    'maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
)

MONTH_TERMS = (
    'jan', 'januari', 'january',
    'feb', 'februari', 'february',
    'mrt', 'maart', 'mar', 'march',
    'apr', 'april',
    'mei', 'may',
    'jun', 'juni', 'june',
    'jul', 'juli', 'july',
    'aug', 'augustus', 'august',
    'sep', 'sept', 'september',
    'okt', 'oct', 'oktober', 'october',
    'nov', 'november',
    'dec', 'december',
)

DEADLINE_PREFIX_PATTERN = (
    r'(?:uiterlijk|tegen|by|before|no later than|deadline(?: is)?|due(?: date)?)'
)
DATE_TOKEN_PATTERN = (
    r'(?:'
    r'(?:' + '|'.join(WEEKDAY_TERMS) + r')'
    r'|\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?'
    r'|\d{1,2}\s+(?:' + '|'.join(MONTH_TERMS) + r')(?:\s+\d{2,4})?'
    r'|(?:' + '|'.join(MONTH_TERMS) + r')\s+\d{1,2}(?:,?\s+\d{2,4})?'
    r')'
)

QUESTION_TRIGGERS = [
    '?', 'kan je', 'kun je', 'could you', 'please reply', 'laat je weten', 'wil je', 'can you',
]

EPHEMERAL_CODE_PATTERNS = [
    r'\bverification code\b',
    r'\bverify email\b',
    r'\benter this code\b',
    r'\bone[- ]?time (passcode|password|code)\b',
    r'\botp\b',
    r'\b2fa\b',
    r'\bauthentication code\b',
    r'\bsecurity code\b',
]

NO_REPLY_PATTERNS = [
    r'\bno[- ]?reply\b',
    r'\bdo not reply\b',
    r'\bautomated\b',
    r'\bauto(?:matisch|mated)? message\b',
]

TEST_MESSAGE_PATTERNS = [
    r'\btestmail\b',
    r'\btest mail\b',
    r'\bdit is een test\b',
    r'\bthis is a test\b',
    r'\btest message\b',
]

ACTION_PRIORITY = {
    'login-alert checken': 0,
    'snel lezen': 1,
    'account activeren': 2,
    'code gebruiken': 3,
    'deadline checken': 4,
    'security checken': 5,
    'financieel checken': 6,
    'agenda checken': 7,
    'antwoord overwegen': 8,
    'ter info': 9,
}

LOCAL_TZ = ZoneInfo('Europe/Amsterdam')


ACTIVATION_PATTERNS = [
    r'\bverify your email\b',
    r'\bverify email\b',
    r'\bconfirm your email\b',
    r'\bconfirm email\b',
    r'\bactivate your account\b',
    r'\bactivation link\b',
    r'\bfinish creating your account\b',
]


@lru_cache(maxsize=1)
def mailbox_username():
    config_path = Path('/home/clawdy/.openclaw/workspace/state/mail-config.json')
    try:
        config = json.loads(config_path.read_text())
    except Exception:
        return ''
    return (config.get('username') or '').strip().lower()


def _haystack(*parts):
    return ' '.join((part or '').strip().lower() for part in parts if part)


def message_haystack(message):
    return _haystack(
        message.get('sender_email'),
        message.get('sender_name'),
        message.get('sender_display') or message.get('from'),
        message.get('subject'),
        message.get('preview'),
    )


def message_content_haystack(message):
    return _haystack(
        message.get('sender_name'),
        message.get('sender_display') or message.get('from'),
        message.get('subject'),
        message.get('preview'),
        ' '.join(message.get('attachment_names') or []),
    )


def attachment_count(message):
    raw = message.get('attachment_count')
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str) and raw.isdigit():
        return int(raw)
    names = message.get('attachment_names') or []
    return len(names)


def attachment_names_lower(message):
    return [str(name).strip().lower() for name in (message.get('attachment_names') or []) if str(name).strip()]


def has_attachment_extension(message, *extensions):
    normalized = tuple(ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions)
    for name in attachment_names_lower(message):
        for ext in normalized:
            if name.endswith(ext):
                return True
    return False


def format_attachment_hint(message, include_names=False):
    count = attachment_count(message)
    if count <= 0:
        return ''

    names = [name for name in (message.get('attachment_names') or []) if name]
    if include_names and names:
        shown = ', '.join(names[:2])
        extra = count - min(len(names), 2)
        if extra > 0:
            shown += f' +{extra}'
        return f' 📎{shown}'
    return f' 📎{count}'


def _coerce_timestamp(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def format_recency_hint(value, now=None):
    ts = _coerce_timestamp(value)
    if ts is None:
        return ''

    now_dt = now.astimezone(UTC) if isinstance(now, datetime) else datetime.now(UTC)
    then_dt = datetime.fromtimestamp(ts, UTC)
    delta_seconds = max(0, int((now_dt - then_dt).total_seconds()))

    if delta_seconds < 90:
        return 'zojuist'
    if delta_seconds < 3600:
        return f'{max(1, delta_seconds // 60)}m geleden'
    if delta_seconds < 36 * 3600:
        local_then = then_dt.astimezone(LOCAL_TZ)
        local_now = now_dt.astimezone(LOCAL_TZ)
        day_label = 'vandaag' if local_then.date() == local_now.date() else 'gisteren'
        return f'{day_label} {local_then:%H:%M}'
    return then_dt.astimezone(LOCAL_TZ).strftime('%Y-%m-%d %H:%M')


def message_age_seconds(message, now=None):
    ts = _coerce_timestamp((message or {}).get('date_ts'))
    if ts is None:
        return None
    now_dt = now.astimezone(UTC) if isinstance(now, datetime) else datetime.now(UTC)
    then_dt = datetime.fromtimestamp(ts, UTC)
    return max(0, int((now_dt - then_dt).total_seconds()))


def attention_window_seconds(message):
    message = message or {}
    action = message.get('action_hint') or suggest_action(message)

    if is_ephemeral_code_message(message):
        return 6 * 3600
    if action in {'login-alert checken', 'security checken', 'account activeren'}:
        return 12 * 3600
    if extract_deadline_hint(message):
        return 7 * 24 * 3600
    if reply_needed(message):
        return 3 * 24 * 3600
    if message.get('urgency') == 'high':
        return 18 * 3600
    return 72 * 3600



def has_attention_signal(message):
    message = message or {}
    action = message.get('action_hint') or suggest_action(message)
    if is_ephemeral_code_message(message):
        return False
    if reply_needed(message):
        return True
    if extract_deadline_hint(message):
        return True
    if message.get('urgency') == 'high' and action != 'ter info':
        return True
    return action in {
        'login-alert checken',
        'snel lezen',
        'account activeren',
        'deadline checken',
        'security checken',
        'financieel checken',
        'agenda checken',
        'antwoord overwegen',
    }



def needs_attention_now(message, now=None):
    message = message or {}
    if not has_attention_signal(message):
        return False

    age_seconds = message_age_seconds(message, now=now)
    if age_seconds is None:
        return True

    return age_seconds <= attention_window_seconds(message)


def is_stale_attention(message, now=None):
    return not needs_attention_now(message, now=now)


def format_span_hint(start_value, end_value):
    start_ts = _coerce_timestamp(start_value)
    end_ts = _coerce_timestamp(end_value)
    if start_ts is None or end_ts is None:
        return ''

    span_seconds = max(0, int(abs(end_ts - start_ts)))
    if span_seconds < 90:
        return 'korte burst'
    if span_seconds < 3600:
        return f'{max(1, span_seconds // 60)}m span'
    if span_seconds < 48 * 3600:
        hours = span_seconds // 3600
        minutes = (span_seconds % 3600) // 60
        if minutes:
            return f'{hours}u {minutes}m span'
        return f'{hours}u span'
    days = span_seconds // 86400
    hours = (span_seconds % 86400) // 3600
    if hours:
        return f'{days}d {hours}u span'
    return f'{days}d span'


def extract_deadline_hint(message):
    haystack = message_content_haystack(message)
    for pattern, label in DEADLINE_PATTERNS:
        match = re.search(pattern, haystack, flags=re.I)
        if match:
            return match.group(0).strip() or label

    explicit_date_deadline = re.search(
        rf'\b{DEADLINE_PREFIX_PATTERN}\s+{DATE_TOKEN_PATTERN}(?:\s+om\s+\d{{1,2}}[:.]\d{{2}}|\s+at\s+\d{{1,2}}[:.]\d{{2}}|\s+\d{{1,2}}[:.]\d{{2}})?\b',
        haystack,
        flags=re.I,
    )
    if explicit_date_deadline:
        return explicit_date_deadline.group(0).strip()

    explicit_day_time_deadline = re.search(
        rf'\b{DEADLINE_PREFIX_PATTERN}\s+\d{{1,2}}[:.]\d{{2}}\b',
        haystack,
        flags=re.I,
    )
    if explicit_day_time_deadline:
        return explicit_day_time_deadline.group(0).strip()

    return None


def extract_security_alert_details(message):
    haystack = ' '.join(
        part for part in [
            message.get('subject'),
            message.get('preview'),
            message.get('body_preview'),
        ] if part
    )
    if not haystack:
        return {}

    details = {}

    ip_match = re.search(r'\bIP Address\s*:\s*([0-9a-fA-F:.]+)', haystack, flags=re.I)
    if ip_match:
        details['ip_address'] = ip_match.group(1).strip()

    device_match = re.search(r'\bDevice Type\s*:\s*([^\n]+?)(?=\s+(?:Browser|Operating System|OS|Location|IP Address|$))', haystack, flags=re.I)
    if device_match:
        device = ' '.join(device_match.group(1).split())
        if device:
            details['device_type'] = device

    browser_match = re.search(r'\bBrowser\s*:\s*([^\n]+?)(?=\s+(?:Operating System|OS|Location|IP Address|$))', haystack, flags=re.I)
    if browser_match:
        browser = ' '.join(browser_match.group(1).split())
        if browser:
            details['browser'] = browser

    location_match = re.search(r'\bLocation\s*:\s*([^\n]+?)(?=\s+(?:Operating System|OS|IP Address|$))', haystack, flags=re.I)
    if location_match:
        location = ' '.join(location_match.group(1).split())
        if location:
            details['location'] = location

    date_match = re.search(r'\bDate\s*:\s*([^\n]+?)(?=\s+(?:IP Address|Device Type|Browser|Operating System|OS|Location|$))', haystack, flags=re.I)
    if date_match:
        when = ' '.join(date_match.group(1).split())
        if when:
            details['event_time'] = when

    return details


def summarize_security_alerts(messages):
    ips = []
    devices = []
    browsers = []
    for message in messages or []:
        details = message.get('security_alert_details') or extract_security_alert_details(message)
        ip = details.get('ip_address')
        device = details.get('device_type')
        browser = details.get('browser')
        if ip and ip not in ips:
            ips.append(ip)
        if device and device not in devices:
            devices.append(device)
        if browser and browser not in browsers:
            browsers.append(browser)

    summary = []
    if ips:
        shown = ', '.join(ips[:2])
        if len(ips) > 2:
            shown += f' +{len(ips) - 2}'
        summary.append(f'IP {shown}')
    if devices:
        shown = ', '.join(devices[:2])
        if len(devices) > 2:
            shown += f' +{len(devices) - 2}'
        summary.append(f'device {shown}')
    elif browsers:
        shown = ', '.join(browsers[:2])
        if len(browsers) > 2:
            shown += f' +{len(browsers) - 2}'
        summary.append(f'browser {shown}')
    return ', '.join(summary)


def format_security_alert_hint(message):
    if not message:
        return ''

    summary = message.get('security_alert_summary')
    if summary:
        return f' {{{summary}}}'

    details = message.get('security_alert_details') or extract_security_alert_details(message)
    parts = []
    if details.get('ip_address'):
        parts.append(details['ip_address'])
    if details.get('device_type'):
        parts.append(details['device_type'])
    elif details.get('browser'):
        parts.append(details['browser'])
    if not parts:
        return ''
    return f" {{{', '.join(parts[:2])}}}"


def detect_urgency(sender, subject, preview):
    haystack = _haystack(sender, subject, preview)
    if any(term in haystack for term in URGENT_TERMS):
        return 'high'
    if any(term in haystack for term in ['new device logged in', 'unknown browser', 'suspicious login', 'new sign in', 'new login']):
        return 'high'
    if extract_deadline_hint({'from': sender, 'subject': subject, 'preview': preview}):
        return 'high'
    return 'normal'


def is_self_message(message):
    username = mailbox_username()
    if not username:
        return False
    sender_email = (message.get('sender_email') or '').strip().lower()
    if sender_email and sender_email == username:
        return True
    sender_display = _haystack(
        message.get('sender_display') or message.get('from'),
        message.get('sender_name'),
    )
    return bool(sender_display and username in sender_display)


def sanitize_preview(message, preview):
    preview = (preview or '').strip()
    if not preview:
        return ''
    if is_self_message(message):
        return '[eigen mailinhoud verborgen]'
    return preview


def is_ephemeral_code_message(message):
    haystack = message_haystack(message)
    return any(re.search(pattern, haystack, flags=re.I) for pattern in EPHEMERAL_CODE_PATTERNS)


def is_no_reply_message(message):
    haystack = message_haystack(message)
    return any(re.search(pattern, haystack, flags=re.I) for pattern in NO_REPLY_PATTERNS)


def is_test_message(message):
    haystack = message_content_haystack(message)
    return any(re.search(pattern, haystack, flags=re.I) for pattern in TEST_MESSAGE_PATTERNS)


def is_meaningful_message(message):
    if is_self_message(message):
        return False
    if is_test_message(message):
        return False
    if is_ephemeral_code_message(message):
        return False
    if not is_no_reply_message(message):
        return True

    action = message.get('action_hint') or suggest_action(message)
    deadline_hint = message.get('deadline_hint') or extract_deadline_hint(message)
    if reply_needed(message):
        return True
    if deadline_hint:
        return True
    if message.get('urgency') == 'high' and action != 'ter info':
        return True
    return action in {
        'login-alert checken',
        'snel lezen',
        'account activeren',
        'deadline checken',
        'security checken',
        'financieel checken',
        'agenda checken',
    }


def should_offer_reply_draft(message):
    if is_self_message(message):
        return False
    if is_test_message(message):
        return False
    if is_ephemeral_code_message(message):
        return False
    if is_no_reply_message(message) and not reply_needed(message):
        return False
    return True


def suggest_action(message):
    haystack = message_content_haystack(message)

    if message.get('urgency') == 'high' and extract_deadline_hint(message):
        return 'deadline checken'
    if is_ephemeral_code_message(message):
        return 'code gebruiken'
    if any(term in haystack for term in ['new device logged in', 'unknown browser', 'suspicious login', 'new sign in', 'new login']):
        return 'login-alert checken'
    if any(re.search(pattern, haystack, flags=re.I) for pattern in ACTIVATION_PATTERNS):
        return 'account activeren'
    if any(term in haystack for term in ['factuur', 'invoice', 'payment', 'betaal', 'subscription']):
        return 'financieel checken'
    if has_attachment_extension(message, '.ics', '.ical', '.ifb', '.vcs'):
        return 'agenda checken'
    if any(term in haystack for term in ['meeting', 'afspraak', 'calendar', 'uitnodiging', 'invite']):
        return 'agenda checken'
    if any(term in haystack for term in ['verify', 'verification', 'password', 'security', 'login', 'sign in', 'logged in', 'new device', 'unknown browser', 'suspicious', '2fa', 'mfa', 'code']):
        return 'security checken'
    if message.get('urgency') == 'high':
        return 'snel lezen'
    if extract_deadline_hint(message):
        return 'deadline checken'
    if any(term in haystack for term in ['question', 'vraag', 'kan je', 'could you', 'please reply', 'laat je weten', 'wil je', 'can you', '?']):
        return 'antwoord overwegen'
    return 'ter info'


def reply_needed(message):
    if (message.get('action_hint') or '') == 'antwoord overwegen':
        return True
    text = message_content_haystack(message)
    return any(trigger in text for trigger in QUESTION_TRIGGERS)


def is_actionable_message(message, include_ephemeral=False):
    action = message.get('action_hint') or suggest_action(message)
    deadline_hint = message.get('deadline_hint') or extract_deadline_hint(message)
    ephemeral = bool(message.get('ephemeral_code')) or is_ephemeral_code_message(message)

    if is_self_message(message):
        return False
    if is_test_message(message):
        return False
    if ephemeral and not include_ephemeral:
        return False
    if reply_needed(message):
        return True
    if deadline_hint:
        return True
    if message.get('urgency') == 'high' and action != 'ter info':
        return True
    return action in {
        'login-alert checken',
        'snel lezen',
        'account activeren',
        'deadline checken',
        'security checken',
        'financieel checken',
        'agenda checken',
        'antwoord overwegen',
        'code gebruiken',
    }


def format_stale_attention_hint(message):
    if not message:
        return ''
    return ' [niet actueel]' if message.get('stale_attention') else ''


def format_next_step_candidate_hint(candidate, include_age=False):
    if not candidate:
        return ''

    sender = candidate.get('label') or candidate.get('sender') or candidate.get('from') or 'onbekend'
    subject = candidate.get('subject') or candidate.get('latest_subject') or '(geen onderwerp)'
    action = candidate.get('action_hint') or candidate.get('recommended_route') or 'ter info'
    count = int(candidate.get('count') or candidate.get('message_count') or 0)
    count_hint = f' x{count}' if count > 1 else ''
    security = format_security_alert_hint(candidate)
    age_value = candidate.get('age_hint') or candidate.get('latest_age_hint')
    age = f' ({age_value})' if include_age and age_value else ''
    draft = ' + concept' if candidate.get('has_draft') or candidate.get('selected_draft') else ''
    stale = format_stale_attention_hint(candidate)
    return f'{sender} — {subject} [{action}]{count_hint}{security}{age}{draft}{stale}'


def format_next_step_command_hint(candidate):
    if not candidate:
        return ''
    command = candidate.get('recommended_command')
    if not command:
        return ''
    label = 'review-command' if candidate.get('review_only') or candidate.get('stale_attention') else 'command'
    return f'{label}={command}'


def format_next_step_alternative_commands(candidates, limit=2):
    rendered = []
    for candidate in candidates or []:
        hint = format_next_step_command_hint(candidate)
        if not hint:
            continue
        rendered.append(f'alt{len(rendered) + 1} {hint}')
        if len(rendered) >= max(0, limit):
            break
    return '; '.join(rendered)


def format_cluster_hint(cluster, include_age=False):
    if not cluster:
        return ''

    sender = cluster.get('from') or cluster.get('sender') or 'onbekend'
    action = cluster.get('action_hint') or 'ter info'
    count = int(cluster.get('count') or 0)
    count_text = f'{count}x' if count > 1 else '1x'
    security = format_security_alert_hint(cluster)
    age = ''
    if include_age and cluster.get('latest_age_hint'):
        age = f" ({cluster['latest_age_hint']})"
    stale = format_stale_attention_hint(cluster)
    return f'{sender} [{action}] {count_text}{security}{age}{stale}'
