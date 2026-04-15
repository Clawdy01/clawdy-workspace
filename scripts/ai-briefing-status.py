#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import posixpath
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

ROOT = Path('/home/clawdy/.openclaw')
JOBS_PATH = ROOT / 'cron' / 'jobs.json'
RUNS_DIR = ROOT / 'cron' / 'runs'
AGENTS_DIR = ROOT / 'agents'
DEFAULT_TZ = 'Europe/Amsterdam'
TARGET_JOB_NAME = 'daily-ai-update'
EXPECTED_SCHEDULE_EXPR = '0 9 * * *'
EXPECTED_DELIVERY_CHANNEL = 'telegram'
EXPECTED_DELIVERY_TO = '16584407'
EXPECTED_DELIVERY_MODE = 'announce'
EXPECTED_SESSION_TARGET = 'isolated'
EXPECTED_WAKE_MODE = 'now'
EXPECTED_AGENT_ID = 'main'
EXPECTED_SESSION_KEY = f'agent:{EXPECTED_AGENT_ID}:{EXPECTED_DELIVERY_CHANNEL}:direct:{EXPECTED_DELIVERY_TO}'
REQUIRED_CATEGORY_MARKERS = [
    '1) frontier modelreleases en modelupdates',
    '2) nieuwe AI-tools en productfeatures',
    '3) open-source modellen/frameworks/inference tooling',
    '4) agents/automation/coding workflows',
    '5) multimodal, voice, image, video en on-device/lokale AI',
    '6) belangrijke researchdoorbraken of capabilities',
    '7) enterprise/security/regulatory ontwikkelingen alleen als ze praktische impact hebben',
]
REQUIRED_PROMPT_MARKERS = [
    'Gebruik eerst web_search breed',
    'val terug op gerichte web_fetch',
    'meerdere primaire bronnen',
    'vermijd dubbele items',
    'als meerdere bronnen over dezelfde ontwikkeling gaan, bundel dat tot één item',
    'Geef bij de belangrijkste items waar mogelijk minstens twee bron-URLs',
    'uit minstens twee verschillende domeinen',
    'marketing zonder echte verandering',
    'focus op echt nieuwe ontwikkelingen uit de afgelopen 48 uur',
    'Noem per item ook de bron plus publicatiedatum of update-datum als die vindbaar is',
    'zo niet, herschrijf of verwijder de foutieve items eerst',
    'Als één item faalt op labels, URL(s) of datumregel',
    'Relevant voor Christian',
    "Wat moeten wij hiermee?",
    "Wat ik vandaag het belangrijkst vind",
    'bronnenlijst met URLs',
]
REQUIRED_FORMAT_MARKERS = [
    'in het Nederlands',
    'Lever in dit formaat: titel',
    'wat is er nieuw',
    'waarom is dit belangrijk',
    "Elke echte ontwikkeling MOET beginnen met exact 'Titel:'",
    'Titel:',
    'Bron:',
    'Datum:',
    'Wat is er nieuw:',
    'Waarom is dit belangrijk:',
    'Relevant voor Christian:',
    "elk 'Titel:'-blok moet direct een geldige 'Bron:' regel",
    'Gebruik dit patroon letterlijk per item:',
    'Bron: https://example.com/item | https://example.org/item',
    'FOUT voorbeeld, niet doen:',
    'OpenAI blog (https://openai.com/news/)',
    'FOUT voorbeeld, ook niet doen:',
    "- Wat is er nieuw",
    "- Waarom is dit belangrijk",
    "- Relevant voor Christian",
    "geen bulletlabels als '- Wat is er nieuw'",
    'Gebruik geen alternatieve labels, geen genummerde itemkoppen, geen bullet-only itemstructuur',
    "De briefing is mislukt als je minder dan 3 items met letterlijk 'Titel:' oplevert.",
    'Verplicht zelfcheck-blok vóór versturen:',
    'Verplicht top-3 zelfcheck:',
    'Publiceer nooit een half-geldig item.',
]
REQUIRED_TOOLS_ALLOW = {'web_search', 'web_fetch'}
REQUIRED_OUTPUT_MARKERS = [
    'Wat moeten wij hiermee?',
    'Wat ik vandaag het belangrijkst vind',
]
REQUIRED_OUTPUT_ITEM_MARKERS = [
    'titel:',
    'wat is er nieuw',
    'waarom is dit belangrijk',
]
REQUIRED_OUTPUT_EXACT_FIELD_PREFIXES = [
    'Titel:',
    'Bron:',
    'Datum:',
    'Wat is er nieuw:',
    'Waarom is dit belangrijk:',
    'Relevant voor Christian:',
]
REQUIRED_OUTPUT_MARKER_ALTERNATIVES = [
    ('bronnenlijst', 'bronnen'),
]
MIN_SOURCE_URLS = 3
MIN_DATED_ITEMS_FOR_STRONG_SIGNAL = 2
PRIMARY_SOURCE_DOMAINS = {
    'openai.com',
    'anthropic.com',
    'googleblog.com',
    'deepmind.google',
    'ai.google.dev',
    'developers.googleblog.com',
    'about.fb.com',
    'ai.meta.com',
    'meta.com',
    'microsoft.com',
    'news.microsoft.com',
    'nvidia.com',
    'developer.nvidia.com',
    'nvidianews.nvidia.com',
    'huggingface.co',
    'stability.ai',
    'runwayml.com',
    'midjourney.com',
    'elevenlabs.io',
    'x.ai',
    'mistral.ai',
    'github.com',
    'arxiv.org',
}
PRIMARY_SOURCE_FAMILIES = {
    'openai.com': 'openai',
    'anthropic.com': 'anthropic',
    'googleblog.com': 'google',
    'deepmind.google': 'google',
    'ai.google.dev': 'google',
    'developers.googleblog.com': 'google',
    'about.fb.com': 'meta',
    'ai.meta.com': 'meta',
    'meta.com': 'meta',
    'microsoft.com': 'microsoft',
    'news.microsoft.com': 'microsoft',
    'nvidia.com': 'nvidia',
    'developer.nvidia.com': 'nvidia',
    'nvidianews.nvidia.com': 'nvidia',
    'huggingface.co': 'huggingface',
    'stability.ai': 'stability',
    'runwayml.com': 'runway',
    'midjourney.com': 'midjourney',
    'elevenlabs.io': 'elevenlabs',
    'x.ai': 'xai',
    'mistral.ai': 'mistral',
    'github.com': 'github',
    'arxiv.org': 'arxiv',
}
CATEGORY_THEME_KEYWORDS = [
    ('frontier-modelupdates', ['frontier', 'modelupdate', 'model update', 'modelrelease', 'model release', 'gpt', 'claude', 'gemini']),
    ('tools-productfeatures', ['tool', 'productfeature', 'product feature', 'feature', 'assistant', 'workspace', 'copilot']),
    ('open-source-tooling', ['open-source', 'open source', 'hugging face', 'huggingface', 'llama', 'mistral', 'inference', 'vllm', 'ollama']),
    ('agents-automation-coding', ['agent', 'automation', 'workflow', 'coding', 'codegen', 'repo', 'tool calling']),
    ('multimodal-voice-image-video-local', ['multimodal', 'voice', 'audio', 'image', 'video', 'vision', 'on-device', 'on device', 'local model', 'lokale ai']),
    ('research-capabilities', ['research', 'paper', 'benchmark', 'capabilit', 'doorbraak', 'arxiv']),
    ('enterprise-security-regulatory', ['enterprise', 'security', 'regulatory', 'compliance', 'governance', 'policy', 'privacy']),
]
DATE_PATTERN = re.compile(
    r'(?:\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}\s+'
    r'(?:jan(?:uari)?|feb(?:ruari)?|mrt|maart|apr(?:il)?|mei|jun(?:i)?|jul(?:i)?|aug(?:ustus)?|'
    r'sep(?:tember)?|okt(?:ober)?|nov(?:ember)?|dec(?:ember)?|'
    r'jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|'
    r'aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{4}\b|'
    r'\b(?:jan(?:uari)?|feb(?:ruari)?|mrt|maart|apr(?:il)?|mei|jun(?:i)?|jul(?:i)?|aug(?:ustus)?|'
    r'sep(?:tember)?|okt(?:ober)?|nov(?:ember)?|dec(?:ember)?|'
    r'jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|'
    r'aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b)',
    re.IGNORECASE,
)
MIN_CATEGORY_THEME_COVERAGE = 3
RECENT_ITEM_MAX_AGE_DAYS = 7
FUTURE_DATE_TOLERANCE_DAYS = 1
MIN_RECENT_ITEMS_FOR_STRONG_SIGNAL = 2
MIN_TOP3_EVIDENCED_ITEMS_FOR_STRONG_SIGNAL = 3
FRESH_ITEM_MAX_AGE_HOURS = 48
MIN_FRESH_TOP3_ITEMS_FOR_STRONG_SIGNAL = 2
MIN_TOP3_MULTI_SOURCE_ITEMS_FOR_STRONG_SIGNAL = 3
MIN_TOP3_MULTI_DOMAIN_SOURCE_ITEMS_FOR_STRONG_SIGNAL = 3
PROOF_TARGET_RUNS = 3

MONTH_NAME_TO_NUMBER = {
    'jan': 1, 'januari': 1, 'january': 1,
    'feb': 2, 'februari': 2, 'february': 2,
    'mrt': 3, 'maart': 3, 'mar': 3, 'march': 3,
    'apr': 4, 'april': 4,
    'mei': 5, 'may': 5,
    'jun': 6, 'juni': 6, 'june': 6,
    'jul': 7, 'juli': 7, 'july': 7,
    'aug': 8, 'augustus': 8, 'august': 8,
    'sep': 9, 'september': 9,
    'okt': 10, 'oct': 10, 'oktober': 10, 'october': 10,
    'nov': 11, 'november': 11,
    'dec': 12, 'december': 12,
}


def load_jobs():
    data = json.loads(JOBS_PATH.read_text())
    return data.get('jobs', []) if isinstance(data, dict) else data


def fmt_ts(ms, tz_name):
    if not ms:
        return None
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone(ZoneInfo(tz_name))
    return dt.strftime('%Y-%m-%d %H:%M %Z')


def age_hint(ms, now_ms):
    if not ms:
        return None
    delta = max(0, int((now_ms - ms) / 1000))
    if delta < 60:
        return 'zojuist'
    minutes = delta // 60
    if minutes < 60:
        return f'{minutes} min geleden'
    hours = minutes // 60
    if hours < 48:
        return f'{hours} uur geleden'
    days = hours // 24
    return f'{days} d geleden'


def future_hint(ms, now_ms):
    if not ms:
        return None
    delta = int((ms - now_ms) / 1000)
    if delta <= 0:
        return 'nu'
    minutes = delta // 60
    if minutes < 60:
        return f'over {minutes} min'
    hours, remaining_minutes = divmod(minutes, 60)
    if hours < 24:
        if remaining_minutes:
            return f'over {hours}u {remaining_minutes}m'
        return f'over {hours} uur'
    days, remaining_hours = divmod(hours, 24)
    if days < 7 and remaining_hours:
        return f'over {days} d {remaining_hours} u'
    return f'over {days} d'


def duration_hint(ms):
    if ms is None:
        return None
    total_seconds = max(0, int(ms / 1000))
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f'{hours}u {minutes}m'
    if minutes:
        return f'{minutes}m {seconds}s'
    return f'{seconds}s'


def parse_cron_hour_minute(expr):
    parts = (expr or '').split()
    if len(parts) != 5:
        return None, None
    minute_raw, hour_raw = parts[0], parts[1]
    if not minute_raw.isdigit() or not hour_raw.isdigit():
        return None, None
    return int(hour_raw), int(minute_raw)


def previous_expected_run_at(next_run_at, expr):
    if not next_run_at:
        return None
    parts = (expr or '').split()
    if len(parts) != 5:
        return None
    minute_raw, hour_raw, day_raw, month_raw, weekday_raw = parts
    if not minute_raw.isdigit() or not hour_raw.isdigit():
        return None
    if day_raw != '*' or month_raw != '*' or weekday_raw != '*':
        return None
    return next_run_at - 24 * 60 * 60 * 1000


def expected_next_run_at(now_ms, expr, tz_name):
    hour, minute = parse_cron_hour_minute(expr)
    parts = (expr or '').split()
    if hour is None or minute is None or len(parts) != 5:
        return None
    _, _, day_raw, month_raw, weekday_raw = parts
    if day_raw != '*' or month_raw != '*' or weekday_raw != '*':
        return None

    tz = ZoneInfo(tz_name)
    now_dt = datetime.fromtimestamp(now_ms / 1000, tz=timezone.utc).astimezone(tz)
    candidate = now_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate.timestamp() * 1000 <= now_ms:
        from datetime import timedelta
        candidate = candidate + timedelta(days=1)
    return int(candidate.astimezone(timezone.utc).timestamp() * 1000)


def projected_proof_target_due_at(next_run_at, remaining_runs, expr):
    if not next_run_at or remaining_runs is None or remaining_runs <= 0:
        return None
    parts = (expr or '').split()
    if len(parts) != 5:
        return None
    minute_raw, hour_raw, day_raw, month_raw, weekday_raw = parts
    if not minute_raw.isdigit() or not hour_raw.isdigit():
        return None
    if day_raw != '*' or month_raw != '*' or weekday_raw != '*':
        return None
    day_ms = 24 * 60 * 60 * 1000
    return next_run_at + ((remaining_runs - 1) * day_ms) + (15 * 60 * 1000)


def projected_proof_run_slots(next_run_at, remaining_runs, expr):
    if not next_run_at or remaining_runs is None or remaining_runs <= 0:
        return []
    parts = (expr or '').split()
    if len(parts) != 5:
        return []
    minute_raw, hour_raw, day_raw, month_raw, weekday_raw = parts
    if not minute_raw.isdigit() or not hour_raw.isdigit():
        return []
    if day_raw != '*' or month_raw != '*' or weekday_raw != '*':
        return []
    day_ms = 24 * 60 * 60 * 1000
    return [next_run_at + (index * day_ms) for index in range(remaining_runs)]


def audit_next_run(job, next_run_at, now_ms, tz_name):
    reasons = []
    if not job.get('enabled'):
        return {
            'ok': True,
            'expected_hour': None,
            'expected_minute': None,
            'next_run_local_hour': None,
            'next_run_local_minute': None,
            'hours_until_next_run': None,
            'reasons': reasons,
            'text': 'job uit, next-run audit niet relevant',
        }

    schedule_expr = ((job.get('schedule') or {}).get('expr')) or ''
    expected_hour, expected_minute = parse_cron_hour_minute(schedule_expr)
    hours_until_next_run = None
    next_run_local_hour = None
    next_run_local_minute = None
    expected_next_run = expected_next_run_at(now_ms, schedule_expr, tz_name)
    previous_expected_run = previous_expected_run_at(expected_next_run, schedule_expr)
    next_run_delta_ms = None
    allowed_pending_current_slot = False
    pending_current_slot_grace_ms = 15 * 60 * 1000

    if not next_run_at:
        reasons.append('nextRunAtMs ontbreekt')
    else:
        next_dt = datetime.fromtimestamp(next_run_at / 1000, tz=timezone.utc).astimezone(ZoneInfo(tz_name))
        next_run_local_hour = next_dt.hour
        next_run_local_minute = next_dt.minute
        hours_until_next_run = round((next_run_at - now_ms) / 3600000, 1)
        allowed_pending_current_slot = bool(
            previous_expected_run
            and next_run_at == previous_expected_run
            and now_ms >= next_run_at
            and now_ms <= (next_run_at + pending_current_slot_grace_ms)
        )
        if expected_hour is not None and next_dt.hour != expected_hour:
            reasons.append(f'next run uur is {next_dt.hour:02d}:{next_dt.minute:02d}')
        if expected_minute is not None and next_dt.minute != expected_minute:
            reasons.append(f'next run minuut is {next_dt.hour:02d}:{next_dt.minute:02d}')
        if hours_until_next_run < -0.1 and not allowed_pending_current_slot:
            reasons.append(f'next run ligt {abs(hours_until_next_run):.1f} uur in het verleden')
        elif hours_until_next_run > 36:
            reasons.append(f'next run ligt verdacht ver weg ({hours_until_next_run:.1f} uur)')
        if expected_next_run is not None:
            next_run_delta_ms = next_run_at - expected_next_run
            if abs(next_run_delta_ms) > 60 * 1000 and not allowed_pending_current_slot:
                reasons.append(
                    f"next run slot wijkt {duration_hint(abs(next_run_delta_ms))} af van verwacht {fmt_ts(expected_next_run, tz_name)}"
                )

    text = 'next run slot ok'
    if reasons:
        text = '; '.join(reasons)
    elif next_run_at and allowed_pending_current_slot:
        text = f'next run staat nog op huidig dagslot binnen grace ({fmt_ts(next_run_at, tz_name)})'
    elif next_run_at:
        text = f'next run slot ok ({fmt_ts(next_run_at, tz_name)})'

    return {
        'ok': not reasons,
        'expected_hour': expected_hour,
        'expected_minute': expected_minute,
        'next_run_local_hour': next_run_local_hour,
        'next_run_local_minute': next_run_local_minute,
        'hours_until_next_run': hours_until_next_run,
        'expected_next_run_at': expected_next_run,
        'expected_next_run_at_text': fmt_ts(expected_next_run, tz_name),
        'previous_expected_run_at': previous_expected_run,
        'previous_expected_run_at_text': fmt_ts(previous_expected_run, tz_name),
        'allowed_pending_current_slot': allowed_pending_current_slot,
        'pending_current_slot_grace_ms': pending_current_slot_grace_ms,
        'next_run_delta_ms': next_run_delta_ms,
        'next_run_delta_text': duration_hint(abs(next_run_delta_ms)) if next_run_delta_ms is not None else None,
        'reasons': reasons,
        'text': text,
    }


def audit_storage(job_id):
    reasons = []
    jobs_exists = JOBS_PATH.exists()
    runs_dir_exists = RUNS_DIR.exists()
    runs_dir_is_dir = RUNS_DIR.is_dir()
    run_file = RUNS_DIR / f'{job_id}.jsonl'
    run_parent = run_file.parent

    jobs_readable = jobs_exists and JOBS_PATH.is_file()
    runs_dir_writable = False
    run_parent_writable = False

    if not jobs_exists:
        reasons.append('jobs.json ontbreekt')
    elif not JOBS_PATH.is_file():
        reasons.append('jobs.json is geen bestand')

    if not runs_dir_exists:
        reasons.append('cron/runs ontbreekt')
    elif not runs_dir_is_dir:
        reasons.append('cron/runs is geen map')

    if runs_dir_exists and runs_dir_is_dir:
        runs_dir_writable = run_parent.is_dir() and os.access(run_parent, os.W_OK)
        run_parent_writable = runs_dir_writable
        if not runs_dir_writable:
            reasons.append('cron/runs niet schrijfbaar')

    text = 'storage ok'
    if reasons:
        text = '; '.join(reasons)
    elif run_parent_writable:
        text = 'storage ok (jobs.json aanwezig, cron/runs schrijfbaar)'

    return {
        'ok': not reasons,
        'jobs_exists': jobs_exists,
        'jobs_readable': jobs_readable,
        'runs_dir_exists': runs_dir_exists,
        'runs_dir_is_dir': runs_dir_is_dir,
        'runs_dir_writable': runs_dir_writable,
        'run_parent_writable': run_parent_writable,
        'run_file_path': str(run_file),
        'reasons': reasons,
        'text': text,
    }


def audit_uniqueness(jobs, target_job):
    reasons = []
    target_id = target_job.get('id')
    target_name = target_job.get('name')
    target_schedule = target_job.get('schedule') or {}
    target_delivery = target_job.get('delivery') or {}
    target_expr = target_schedule.get('expr')
    target_tz = target_schedule.get('tz') or DEFAULT_TZ
    target_channel = target_delivery.get('channel')
    target_to = str(target_delivery.get('to') or '')

    duplicate_name_jobs = []
    colliding_delivery_jobs = []
    for other in jobs:
        if other.get('id') == target_id:
            continue
        other_schedule = other.get('schedule') or {}
        other_delivery = other.get('delivery') or {}
        if other.get('name') == target_name:
            duplicate_name_jobs.append({
                'id': other.get('id'),
                'enabled': bool(other.get('enabled')),
            })
        if (
            bool(other.get('enabled'))
            and other_schedule.get('kind') == 'cron'
            and other_schedule.get('expr') == target_expr
            and (other_schedule.get('tz') or DEFAULT_TZ) == target_tz
            and (other_delivery.get('channel') or '') == target_channel
            and str(other_delivery.get('to') or '') == target_to
        ):
            colliding_delivery_jobs.append({
                'id': other.get('id'),
                'name': other.get('name'),
                'delivery_mode': other_delivery.get('mode'),
            })

    if duplicate_name_jobs:
        reasons.append(f"{len(duplicate_name_jobs)} extra job(s) met naam {target_name}")
    if colliding_delivery_jobs:
        reasons.append(
            f"{len(colliding_delivery_jobs)} extra cronjob(s) met zelfde schedule+delivery naar {target_channel}:{target_to}"
        )

    if reasons:
        text = '; '.join(reasons)
    else:
        text = 'uniqueness ok (geen dubbele jobnaam of delivery-collision)'

    return {
        'ok': not reasons,
        'duplicate_name_jobs': duplicate_name_jobs,
        'colliding_delivery_jobs': colliding_delivery_jobs,
        'reasons': reasons,
        'text': text,
    }


def split_summary_item_blocks(summary_text):
    if not isinstance(summary_text, str):
        return []
    direct_title_re = re.compile(r'(?im)^(?:\s*\d+[\.)]\s+)?titel:\s*')
    title_starts = list(direct_title_re.finditer(summary_text))
    blocks = []
    if title_starts:
        for index, match in enumerate(title_starts):
            start = match.end()
            end = title_starts[index + 1].start() if index + 1 < len(title_starts) else len(summary_text)
            block = summary_text[start:end].strip()
            if block:
                blocks.append('Titel: ' + block)
        if blocks:
            return blocks

    lines = summary_text.splitlines()
    category_heading_re = re.compile(r'^\s*\d+\)\s+')
    title_re = re.compile(r'(?im)^titel:\s*(.+)$')
    category_start = None
    stop_section_markers = {
        'wat moeten wij hiermee?',
        'wat ik vandaag het belangrijkst vind',
        'bronnenlijst',
        'bronnen',
    }
    for index, raw_line in enumerate(lines):
        line = raw_line.strip()
        if category_heading_re.match(line):
            category_start = index
            continue
        lowered = line.lower()
        if category_start is not None and lowered in stop_section_markers:
            break
        if category_start is None or not lowered.startswith('bron:'):
            continue

        title = None
        search_index = index - 1
        while search_index > category_start:
            candidate = lines[search_index].strip()
            candidate_lower = candidate.lower()
            if not candidate:
                search_index -= 1
                continue
            if candidate.startswith('-') or candidate_lower.startswith('relevant voor christian'):
                break
            if candidate_lower.startswith(('bron:', 'wat is er nieuw', 'waarom is dit belangrijk')):
                search_index -= 1
                continue
            if category_heading_re.match(candidate):
                break
            match = title_re.search(candidate)
            title = match.group(1).strip() if match else candidate
            break
        if not title:
            continue

        end = len(lines)
        for next_index in range(index + 1, len(lines)):
            candidate = lines[next_index].strip()
            candidate_lower = candidate.lower()
            if category_heading_re.match(candidate) or candidate_lower in stop_section_markers:
                end = next_index
                break
            if candidate_lower.startswith('bron:'):
                end = next_index
                break

        block_lines = [f'Titel: {title}']
        if index < end:
            block_lines.extend(lines[index:end])
        block = '\n'.join(line.rstrip() for line in block_lines).strip()
        if block and block not in blocks:
            blocks.append(block)
    return blocks


def extract_item_title(block):
    if not isinstance(block, str):
        return None
    match = re.search(r'(?im)^titel:\s*(.+)$', block)
    if not match:
        return None
    title = match.group(1).strip()
    return title or None


def normalize_title_key(title):
    if not isinstance(title, str):
        return ''
    normalized = title.strip().lower()
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.strip()


def extract_source_line_text(block):
    for line in (block or '').splitlines():
        stripped = line.strip()
        if stripped.lower().startswith('bron:'):
            return stripped
    return None


def extract_date_line_text(block):
    for line in (block or '').splitlines():
        stripped = line.strip()
        if stripped.lower().startswith('datum:'):
            return stripped
    return None


def split_source_line_tokens(line):
    if not isinstance(line, str):
        return []
    body = re.sub(r'(?i)^bron:\s*', '', line).strip()
    if not body:
        return []
    return [token for token in re.split(r'\s*\|\s*|\s+', body) if token]


def extract_source_urls_from_line(line):
    return [token for token in split_source_line_tokens(line) if re.fullmatch(r'https?://\S+', token)]


def source_url_has_trailing_punctuation(url):
    if not isinstance(url, str) or not url:
        return False
    return url[-1] in '.,;:!?)]}'


def is_valid_source_line(line):
    if not isinstance(line, str):
        return False
    stripped = line.strip()
    if not stripped.lower().startswith('bron:'):
        return False
    urls = extract_source_urls_from_line(stripped)
    if not urls:
        return False
    return not analyze_source_line_issues(stripped)


def count_prefixed_lines(text, prefixes, *, case_sensitive=False):
    counts = {prefix: 0 for prefix in prefixes}
    if not isinstance(text, str):
        return counts
    if case_sensitive:
        for raw_line in text.splitlines():
            stripped = raw_line.strip()
            for prefix in prefixes:
                if stripped.startswith(prefix):
                    counts[prefix] += 1
        return counts
    normalized_prefixes = [(prefix, prefix.lower()) for prefix in prefixes]
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        lowered = stripped.lower()
        for prefix, lowered_prefix in normalized_prefixes:
            if lowered.startswith(lowered_prefix):
                counts[prefix] += 1
    return counts


def extract_prefixed_line_sequence(text, prefixes, *, case_sensitive=False):
    if not isinstance(text, str):
        return []
    sequence = []
    if case_sensitive:
        for raw_line in text.splitlines():
            stripped = raw_line.strip()
            for prefix in prefixes:
                if stripped.startswith(prefix):
                    sequence.append(prefix)
                    break
        return sequence
    normalized_prefixes = [(prefix, prefix.lower()) for prefix in prefixes]
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        lowered = stripped.lower()
        for prefix, lowered_prefix in normalized_prefixes:
            if lowered.startswith(lowered_prefix):
                sequence.append(prefix)
                break
    return sequence


def analyze_source_line_issues(line):
    if not isinstance(line, str):
        return []
    stripped = line.strip()
    if not stripped:
        return []
    body = re.sub(r'(?i)^bron:\s*', '', stripped).strip()
    if not body:
        return ['leeg']

    issues = []
    lower = body.lower()
    urls = extract_source_urls_from_line(stripped)
    if not urls:
        issues.append('geen_url')

    if '|' in body:
        pipe_parts = [part.strip() for part in body.split('|')]
        if any(not part for part in pipe_parts):
            issues.append('lege_separator')
    body_without_urls_for_separator = body
    for url in sorted(urls, key=len, reverse=True):
        body_without_urls_for_separator = body_without_urls_for_separator.replace(url, ' ')
    if re.search(r'(^|\s)/(\s|$)', body_without_urls_for_separator):
        issues.append('slash_separator')
    if re.search(r'[•·●◦▪▫‣∙]', body_without_urls_for_separator):
        issues.append('bullet_separator')
    if ',' in body:
        issues.append('komma')
    if ';' in body:
        issues.append('puntkomma')
    if '(' in body or ')' in body:
        issues.append('haakjes')
    if '<' in body or '>' in body:
        issues.append('hoekhaken')
    if '[' in body or ']' in body:
        issues.append('vierkante_haken')
    if any(char in body for char in ('"', "'", '“', '”', '‘', '’')):
        issues.append('aanhalingstekens')
    if '`' in body:
        issues.append('backticks')
    if any(source_url_has_trailing_punctuation(url) for url in urls):
        issues.append('url_leesteken')
    if 'update-datum' in lower:
        issues.append('update_datum')
    if 'extra context' in lower:
        issues.append('extra_context')
    if re.search(r'\bvia\b', lower):
        issues.append('via_context')
    if DATE_PATTERN.search(body):
        issues.append('datumtekst')

    body_without_urls = body_without_urls_for_separator
    body_without_urls = re.sub(r'[|,;()/]', ' ', body_without_urls)
    body_without_urls = re.sub(r'\s+', ' ', body_without_urls).strip()
    if body_without_urls and re.search(r'[A-Za-zÀ-ÿ]', body_without_urls):
        issues.append('vrije_tekst')

    return issues


def format_issue_counts(counter):
    if not counter:
        return None
    labels = {
        'geen_url': 'geen URL',
        'lege_separator': 'lege separator',
        'slash_separator': 'slash-separator',
        'bullet_separator': 'bullet-separator',
        'komma': 'komma',
        'puntkomma': 'puntkomma',
        'haakjes': 'haakjes',
        'hoekhaken': 'hoekhaken',
        'vierkante_haken': 'vierkante haken',
        'aanhalingstekens': 'aanhalingstekens',
        'backticks': 'backticks',
        'url_leesteken': 'URL-leesteken',
        'update_datum': 'update-datum',
        'extra_context': 'extra context',
        'via_context': 'via',
        'datumtekst': 'datumtekst',
        'vrije_tekst': 'vrije tekst',
        'leeg': 'leeg',
    }
    parts = []
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        parts.append(f"{labels.get(key, key)} {count}x")
    return ', '.join(parts)


def normalize_year(year):
    year = int(year)
    if year < 100:
        return 2000 + year if year < 70 else 1900 + year
    return year


def parse_date_match_to_ms(raw_text, reference_dt):
    text = (raw_text or '').strip().replace(',', '')
    if not text:
        return None

    iso = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', text)
    if iso:
        year, month, day = map(int, iso.groups())
    else:
        numeric = re.fullmatch(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', text)
        if numeric:
            day, month, year = numeric.groups()
            day = int(day)
            month = int(month)
            year = normalize_year(year)
        else:
            named = re.fullmatch(r'(\d{1,2})\s+([A-Za-zÀ-ÿ]+)\s+(\d{4})', text, re.IGNORECASE)
            if named:
                day, month_name, year = named.groups()
                day = int(day)
                month = MONTH_NAME_TO_NUMBER.get(month_name.lower())
                year = int(year)
            else:
                named_us = re.fullmatch(r'([A-Za-zÀ-ÿ]+)\s+(\d{1,2})\s+(\d{4})', text, re.IGNORECASE)
                if not named_us:
                    return None
                month_name, day, year = named_us.groups()
                day = int(day)
                month = MONTH_NAME_TO_NUMBER.get(month_name.lower())
                year = int(year)

    if not month:
        return None

    try:
        dt = datetime(year, month, day, tzinfo=reference_dt.tzinfo)
    except ValueError:
        return None
    return int(dt.astimezone(timezone.utc).timestamp() * 1000)


def latest_block_date_ms(block, reference_ms=None):
    if not isinstance(block, str) or not block.strip():
        return None
    reference_dt = datetime.fromtimestamp((reference_ms or int(datetime.now(tz=timezone.utc).timestamp() * 1000)) / 1000, tz=timezone.utc)
    parsed = [
        parse_date_match_to_ms(match.group(0), reference_dt)
        for match in DATE_PATTERN.finditer(block)
    ]
    parsed = [value for value in parsed if value is not None]
    return max(parsed) if parsed else None


TRACKING_QUERY_PARAM_PREFIXES = ('utm_',)
TRACKING_QUERY_PARAMS = {
    'fbclid',
    'gclid',
    'mc_cid',
    'mc_eid',
    'mkt_tok',
    'ref_src',
    's_cid',
}


UNRESERVED_URL_CHARACTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~')


def decode_unreserved_url_path(path):
    if not isinstance(path, str) or '%' not in path:
        return path

    def replace(match):
        decoded = unquote(match.group(0))
        if len(decoded) == 1 and decoded in UNRESERVED_URL_CHARACTERS:
            return decoded
        return match.group(0).upper()

    return re.sub(r'%[0-9A-Fa-f]{2}', replace, path)


def normalize_url_path_dot_segments(path):
    if not isinstance(path, str) or not path:
        return '/'
    collapsed = re.sub(r'/+', '/', path)
    normalized = posixpath.normpath(collapsed)
    if path.startswith('/') and not normalized.startswith('/'):
        normalized = f'/{normalized}'
    if normalized in ('.', ''):
        return '/'
    return normalized


def canonicalize_source_url(url):
    if not isinstance(url, str):
        return None
    raw = url.strip()
    if not raw:
        return None
    try:
        parts = urlsplit(raw)
    except ValueError:
        return raw
    if not parts.scheme or not parts.netloc:
        return raw
    filtered_query = sorted(
        (
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in TRACKING_QUERY_PARAMS and not key.lower().startswith(TRACKING_QUERY_PARAM_PREFIXES)
        ),
        key=lambda item: (item[0], item[1]),
    )
    hostname = (parts.hostname or '').lower().rstrip('.')
    if hostname.startswith('www.'):
        hostname = hostname[4:]
    port = parts.port
    username = parts.username
    password = parts.password
    default_port = (parts.scheme.lower() == 'https' and port == 443) or (parts.scheme.lower() == 'http' and port == 80)
    if not hostname:
        normalized_netloc = parts.netloc.lower()
    else:
        auth = ''
        if username is not None:
            auth = username
            if password is not None:
                auth += f':{password}'
            auth += '@'
        port_suffix = '' if port is None or default_port else f':{port}'
        normalized_netloc = f'{auth}{hostname}{port_suffix}'
    normalized_path = decode_unreserved_url_path(parts.path or '/')
    normalized_path = normalize_url_path_dot_segments(normalized_path)
    if normalized_path != '/':
        normalized_path = re.sub(
            r'/(?:(?:index|default)\.(?:html?|aspx?))$',
            '',
            normalized_path,
            flags=re.IGNORECASE,
        ) or '/'
        if normalized_path != '/' and normalized_path.endswith('/'):
            normalized_path = normalized_path.rstrip('/') or '/'
    normalized_query = urlencode(filtered_query, doseq=True)
    return urlunsplit((parts.scheme.lower(), normalized_netloc, normalized_path, normalized_query, ''))



def primary_source_family(domain):
    if not isinstance(domain, str) or not domain:
        return None
    normalized = domain.lower()
    for root, family in PRIMARY_SOURCE_FAMILIES.items():
        if normalized == root or normalized.endswith(f'.{root}'):
            return family
    return None


def audit_summary_output(summary_text, reference_ms=None):
    if not isinstance(summary_text, str) or not summary_text.strip():
        return {
            'available': False,
            'ok': True,
            'missing_markers': [],
            'item_marker_counts': {},
            'item_count': 0,
            'item_marker_min_count': 0,
            'source_url_count': 0,
            'unique_source_url_count': 0,
            'source_urls': [],
            'source_domains': [],
            'source_domain_count': 0,
            'item_titles': [],
            'unique_item_titles': [],
            'unique_item_title_count': 0,
            'duplicate_item_title_count': 0,
            'duplicate_item_title_examples': [],
            'items_with_source_count': 0,
            'items_without_source_count': 0,
            'items_with_multiple_sources_count': 0,
            'items_with_valid_source_line_count': 0,
            'items_with_invalid_source_line_count': 0,
            'items_missing_source_line_count': 0,
            'invalid_source_line_issue_counts': {},
            'items_invalid_source_line_examples': [],
            'first3_items_with_source_count': 0,
            'first3_items_with_multiple_sources_count': 0,
            'first3_items_with_valid_source_line_count': 0,
            'first3_items_with_invalid_source_line_count': 0,
            'top3_invalid_source_line_issue_counts': {},
            'top3_invalid_source_line_examples': [],
            'first3_source_urls': [],
            'first3_unique_source_url_count': 0,
            'first3_source_domains': [],
            'first3_source_domain_count': 0,
        'first3_primary_source_domains': [],
        'first3_primary_source_domain_count': 0,
        'first3_primary_source_families': [],
        'first3_primary_source_family_count': 0,
        'primary_source_domains': [],
        'primary_source_domain_count': 0,
        'primary_source_families': [],
        'primary_source_family_count': 0,
            'dated_item_count': 0,
            'undated_item_count': 0,
            'recent_dated_item_count': 0,
            'recent_dated_first3_count': 0,
            'fresh_dated_item_count': 0,
            'fresh_dated_first3_count': 0,
            'future_dated_item_count': 0,
            'future_dated_first3_count': 0,
            'first3_evidenced_item_count': 0,
            'first3_primary_fresh_item_count': 0,
            'recent_item_max_age_days': RECENT_ITEM_MAX_AGE_DAYS,
            'fresh_item_max_age_hours': FRESH_ITEM_MAX_AGE_HOURS,
            'future_date_tolerance_days': FUTURE_DATE_TOLERANCE_DAYS,
            'category_theme_hits': [],
            'category_theme_count': 0,
            'reasons': [],
            'text': 'geen briefinginhoud om te auditen',
        }

    normalized_text = summary_text.lower()
    missing_markers = [marker for marker in REQUIRED_OUTPUT_MARKERS if marker.lower() not in normalized_text]
    item_marker_counts = {
        marker: normalized_text.count(marker.lower())
        for marker in REQUIRED_OUTPUT_ITEM_MARKERS
    }
    exact_field_line_counts = count_prefixed_lines(
        summary_text,
        REQUIRED_OUTPUT_EXACT_FIELD_PREFIXES,
        case_sensitive=True,
    )
    numbered_title_heading_matches = re.findall(r'(?im)^\s*\d+[\.)]\s+titel:\s*(.+)$', summary_text)
    numbered_title_heading_count = len(numbered_title_heading_matches)
    numbered_title_heading_examples = [title.strip() for title in numbered_title_heading_matches[:3] if title.strip()]
    missing_alternative_groups = [
        list(group)
        for group in REQUIRED_OUTPUT_MARKER_ALTERNATIVES
        if not any(marker.lower() in normalized_text for marker in group)
    ]
    item_blocks = split_summary_item_blocks(summary_text)
    item_count = len(item_blocks)
    effective_item_marker_counts = dict(item_marker_counts)
    effective_item_marker_counts['titel:'] = max(effective_item_marker_counts.get('titel:', 0), item_count)
    item_marker_min_count = min(effective_item_marker_counts.values()) if effective_item_marker_counts else 0
    item_marker_counts = effective_item_marker_counts
    item_titles = [title for title in (extract_item_title(block) for block in item_blocks) if title]
    title_entries = []
    for title in item_titles:
        key = normalize_title_key(title)
        if key:
            title_entries.append((title, key))
    unique_item_titles = []
    seen_title_keys = set()
    for title, key in title_entries:
        if key in seen_title_keys:
            continue
        seen_title_keys.add(key)
        unique_item_titles.append(title)
    title_key_counts = Counter(key for _, key in title_entries)
    title_key_to_example = {}
    for title, key in title_entries:
        title_key_to_example.setdefault(key, title)
    duplicate_item_title_examples = [
        {'title': title_key_to_example[key], 'count': count}
        for key, count in title_key_counts.most_common()
        if count > 1
    ]
    unique_item_title_count = len(seen_title_keys)
    duplicate_item_title_count = max(0, len(title_entries) - unique_item_title_count)

    block_titles = []
    for index, block in enumerate(item_blocks, start=1):
        title = extract_item_title(block) or f'item {index}'
        block_titles.append(title)

    block_exact_field_sequences = [
        extract_prefixed_line_sequence(
            block,
            REQUIRED_OUTPUT_EXACT_FIELD_PREFIXES,
            case_sensitive=True,
        )
        for block in item_blocks
    ]
    block_exact_field_order_ok = [
        sequence == REQUIRED_OUTPUT_EXACT_FIELD_PREFIXES
        for sequence in block_exact_field_sequences
    ]
    items_with_exact_field_order_count = sum(1 for is_ok in block_exact_field_order_ok if is_ok)
    items_with_field_order_mismatch_count = max(0, len(item_blocks) - items_with_exact_field_order_count)
    items_field_order_mismatch_examples = [
        {
            'title': title,
            'sequence': sequence,
        }
        for title, is_ok, sequence in zip(block_titles, block_exact_field_order_ok, block_exact_field_sequences)
        if not is_ok
    ][:3]

    now_ms = reference_ms or int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    block_source_lines = [extract_source_line_text(block) for block in item_blocks]
    block_source_line_urls = [extract_source_urls_from_line(line) for line in block_source_lines]
    block_has_source_line = [bool(line) for line in block_source_lines]
    block_valid_source_line = [is_valid_source_line(line) for line in block_source_lines]
    block_date_lines = [extract_date_line_text(block) for block in item_blocks]
    block_has_date_line = [bool(line) for line in block_date_lines]
    block_date_line_values = [latest_block_date_ms(line, reference_ms=now_ms) for line in block_date_lines]
    block_invalid_source_line = [
        bool(line) and not is_valid
        for line, is_valid in zip(block_source_lines, block_valid_source_line)
    ]
    block_source_line_issue_lists = [
        analyze_source_line_issues(line) if is_invalid else []
        for line, is_invalid in zip(block_source_lines, block_invalid_source_line)
    ]
    invalid_source_line_issue_counts = Counter(
        issue
        for issues in block_source_line_issue_lists
        for issue in issues
    )
    top3_invalid_source_line_issue_counts = Counter(
        issue
        for issues in block_source_line_issue_lists[:3]
        for issue in issues
    )
    block_source_urls = [re.findall(r'https?://\S+', block) for block in item_blocks]
    block_valid_source_urls = [
        urls if is_valid else []
        for urls, is_valid in zip(block_source_line_urls, block_valid_source_line)
    ]
    block_canonical_valid_source_urls = [
        [canonicalize_source_url(url) or url for url in urls]
        for urls in block_valid_source_urls
    ]
    block_source_domains = [
        sorted({
            re.sub(r'^www\.', '', url.split('/')[2].lower())
            for url in urls
            if len(url.split('/')) > 2 and url.split('/')[2]
        })
        for urls in block_canonical_valid_source_urls
    ]
    block_unique_source_domain_counts = [len(domains) for domains in block_source_domains]
    block_source_counts = [len(urls) for urls in block_source_urls]
    block_valid_source_url_counts = [len(urls) for urls in block_valid_source_urls]
    block_unique_source_url_counts = [len(set(urls)) for urls in block_canonical_valid_source_urls]
    items_with_source_count = sum(1 for count in block_source_counts if count > 0)
    items_without_source_count = max(0, len(item_blocks) - items_with_source_count)
    items_with_multiple_sources_count = sum(1 for count in block_unique_source_url_counts if count >= 2)
    items_with_multi_domain_sources_count = sum(1 for count in block_unique_source_domain_counts if count >= 2)
    items_with_valid_source_line_count = sum(1 for is_valid in block_valid_source_line if is_valid)
    items_with_invalid_source_line_count = sum(1 for is_invalid in block_invalid_source_line if is_invalid)
    items_missing_source_line_count = sum(1 for has_line in block_has_source_line if not has_line)
    first3_items_with_source_count = sum(1 for count in block_source_counts[:3] if count > 0)
    first3_items_with_multiple_sources_count = sum(1 for count in block_unique_source_url_counts[:3] if count >= 2)
    first3_items_with_multi_domain_sources_count = sum(
        1 for count in block_unique_source_domain_counts[:3] if count >= 2
    )
    first3_items_with_valid_source_line_count = sum(1 for is_valid in block_valid_source_line[:3] if is_valid)
    first3_items_with_invalid_source_line_count = sum(1 for is_invalid in block_invalid_source_line[:3] if is_invalid)
    source_urls = [url for urls in block_valid_source_urls for url in urls]
    canonical_source_urls = [url for urls in block_canonical_valid_source_urls for url in urls]
    unique_source_urls = sorted(set(canonical_source_urls))
    source_url_count = len(source_urls)
    unique_source_url_count = len(unique_source_urls)
    first3_source_urls = [url for urls in block_valid_source_urls[:3] for url in urls]
    first3_canonical_source_urls = [url for urls in block_canonical_valid_source_urls[:3] for url in urls]
    first3_unique_source_url_count = len(set(first3_canonical_source_urls))
    source_domains = sorted({domain for domains in block_source_domains for domain in domains})
    source_domain_count = len(source_domains)
    first3_source_domains = sorted({domain for domains in block_source_domains[:3] for domain in domains})
    block_has_primary_source = [
        any(
            domain == root or domain.endswith(f'.{root}')
            for domain in domains
            for root in PRIMARY_SOURCE_DOMAINS
        )
        for domains in block_source_domains
    ]
    first3_items_with_primary_source_count = sum(1 for has_primary in block_has_primary_source[:3] if has_primary)
    valid_source_domains = sorted({domain for domains in block_source_domains for domain in domains})
    valid_first3_source_domains = sorted({domain for domains in block_source_domains[:3] for domain in domains})
    primary_source_domains = sorted({
        domain for domain in valid_source_domains
        if any(domain == root or domain.endswith(f'.{root}') for root in PRIMARY_SOURCE_DOMAINS)
    })
    primary_source_families = sorted({
        family for family in (primary_source_family(domain) for domain in valid_source_domains) if family
    })
    primary_source_domain_count = len(primary_source_domains)
    primary_source_family_count = len(primary_source_families)
    first3_source_domain_count = len(first3_source_domains)
    first3_primary_source_domains = sorted({
        domain for domain in valid_first3_source_domains
        if any(domain == root or domain.endswith(f'.{root}') for root in PRIMARY_SOURCE_DOMAINS)
    })
    first3_primary_source_families = sorted({
        family for family in (primary_source_family(domain) for domain in valid_first3_source_domains) if family
    })
    first3_primary_source_domain_count = len(first3_primary_source_domains)
    first3_primary_source_family_count = len(first3_primary_source_families)
    dated_item_count = sum(1 for block in item_blocks if DATE_PATTERN.search(block))
    undated_item_count = max(0, len(item_blocks) - dated_item_count)
    explicit_dated_item_count = sum(1 for has_line in block_has_date_line if has_line)
    explicit_undated_item_count = max(0, len(item_blocks) - explicit_dated_item_count)
    recent_cutoff_ms = now_ms - RECENT_ITEM_MAX_AGE_DAYS * 24 * 60 * 60 * 1000
    fresh_cutoff_ms = now_ms - FRESH_ITEM_MAX_AGE_HOURS * 60 * 60 * 1000
    future_cutoff_ms = now_ms + FUTURE_DATE_TOLERANCE_DAYS * 24 * 60 * 60 * 1000
    block_date_values = [latest_block_date_ms(block, reference_ms=now_ms) for block in item_blocks]
    recent_dated_item_count = sum(1 for value in block_date_values if value is not None and value >= recent_cutoff_ms)
    recent_dated_first3_count = sum(
        1 for value in block_date_values[:3] if value is not None and value >= recent_cutoff_ms
    )
    explicit_recent_dated_item_count = sum(
        1 for value in block_date_line_values if value is not None and value >= recent_cutoff_ms
    )
    explicit_recent_dated_first3_count = sum(
        1 for value in block_date_line_values[:3] if value is not None and value >= recent_cutoff_ms
    )
    fresh_dated_item_count = sum(1 for value in block_date_values if value is not None and value >= fresh_cutoff_ms)
    fresh_dated_first3_count = sum(
        1 for value in block_date_values[:3] if value is not None and value >= fresh_cutoff_ms
    )
    explicit_fresh_dated_item_count = sum(
        1 for value in block_date_line_values if value is not None and value >= fresh_cutoff_ms
    )
    explicit_fresh_dated_first3_count = sum(
        1 for value in block_date_line_values[:3] if value is not None and value >= fresh_cutoff_ms
    )
    future_dated_item_count = sum(1 for value in block_date_values if value is not None and value > future_cutoff_ms)
    future_dated_first3_count = sum(
        1 for value in block_date_values[:3] if value is not None and value > future_cutoff_ms
    )
    explicit_future_dated_item_count = sum(
        1 for value in block_date_line_values if value is not None and value > future_cutoff_ms
    )
    explicit_future_dated_first3_count = sum(
        1 for value in block_date_line_values[:3] if value is not None and value > future_cutoff_ms
    )
    first3_evidenced_item_count = sum(
        1
        for is_valid, date_value in zip(block_valid_source_line[:3], block_date_line_values[:3])
        if is_valid and date_value is not None and date_value >= recent_cutoff_ms
    )
    items_missing_source_examples = [
        title
        for title, source_count in zip(block_titles, block_source_counts)
        if source_count <= 0
    ][:3]
    items_invalid_source_line_examples = [
        {
            'title': title,
            'source_line': source_line,
            'issues': issues,
        }
        for title, source_line, is_invalid, issues in zip(
            block_titles,
            block_source_lines,
            block_invalid_source_line,
            block_source_line_issue_lists,
        )
        if is_invalid and source_line
    ][:3]
    top3_missing_source_examples = [
        title
        for title, source_count in zip(block_titles[:3], block_source_counts[:3])
        if source_count <= 0
    ][:3]
    top3_invalid_source_line_examples = [
        {
            'title': title,
            'source_line': source_line,
            'issues': issues,
        }
        for title, source_line, is_invalid, issues in zip(
            block_titles[:3],
            block_source_lines[:3],
            block_invalid_source_line[:3],
            block_source_line_issue_lists[:3],
        )
        if is_invalid and source_line
    ][:3]
    top3_missing_multi_source_examples = [
        title
        for title, unique_source_count in zip(block_titles[:3], block_unique_source_url_counts[:3])
        if unique_source_count < 2
    ][:3]
    top3_missing_multi_domain_source_examples = [
        title
        for title, unique_domain_count in zip(block_titles[:3], block_unique_source_domain_counts[:3])
        if unique_domain_count < 2
    ][:3]
    top3_missing_primary_source_examples = [
        title
        for title, has_primary in zip(block_titles[:3], block_has_primary_source[:3])
        if not has_primary
    ][:3]
    items_missing_date_line_examples = [
        title
        for title, has_line in zip(block_titles, block_has_date_line)
        if not has_line
    ][:3]
    top3_missing_date_line_examples = [
        title
        for title, has_line in zip(block_titles[:3], block_has_date_line[:3])
        if not has_line
    ][:3]
    top3_missing_recent_date_examples = [
        title
        for title, date_value in zip(block_titles[:3], block_date_line_values[:3])
        if date_value is None or date_value < recent_cutoff_ms
    ][:3]
    top3_missing_primary_fresh_examples = [
        title
        for title, domains, date_value in zip(block_titles[:3], block_source_domains[:3], block_date_line_values[:3])
        if not (
            date_value is not None
            and date_value >= fresh_cutoff_ms
            and any(
                domain == root or domain.endswith(f'.{root}')
                for domain in domains
                for root in PRIMARY_SOURCE_DOMAINS
            )
        )
    ][:3]
    first3_primary_fresh_item_count = sum(
        1
        for domains, date_value in zip(block_source_domains[:3], block_date_line_values[:3])
        if (
            date_value is not None
            and date_value >= fresh_cutoff_ms
            and any(
                domain == root or domain.endswith(f'.{root}')
                for domain in domains
                for root in PRIMARY_SOURCE_DOMAINS
            )
        )
    )
    category_theme_hits = [
        name
        for name, keywords in CATEGORY_THEME_KEYWORDS
        if any(keyword in normalized_text for keyword in keywords)
    ]
    category_theme_count = len(category_theme_hits)
    reasons = []
    if missing_markers:
        reasons.append(f"{len(missing_markers)} verplichte sectie(s) missen")
    if item_marker_min_count < 3:
        reasons.append(
            'te weinig briefingitems met titel/nieuw/belangrijk-structuur '
            f"(min {item_marker_min_count}, verwacht minstens 3)"
        )
    if item_count:
        exact_field_mismatches = [
            f'{prefix} {exact_field_line_counts.get(prefix, 0)}/{item_count}'
            for prefix in REQUIRED_OUTPUT_EXACT_FIELD_PREFIXES
            if exact_field_line_counts.get(prefix, 0) != item_count
        ]
        if exact_field_mismatches:
            reasons.append(
                'verplichte exacte veldlabels per item kloppen niet '
                f"({', '.join(exact_field_mismatches)})"
            )
    if item_count and items_with_exact_field_order_count < item_count:
        reason = (
            'niet elk item volgt de exacte labelvolgorde '
            f'({items_with_exact_field_order_count}/{item_count})'
        )
        if items_field_order_mismatch_examples:
            examples_text = ', '.join(
                f"{example['title']} -> {' > '.join(example['sequence'])}"
                for example in items_field_order_mismatch_examples
            )
            reason += f': {examples_text}'
        reasons.append(reason)
    if numbered_title_heading_count:
        reason = f'genummerde itemkoppen gevonden ({numbered_title_heading_count})'
        if numbered_title_heading_examples:
            reason += f": {', '.join(numbered_title_heading_examples)}"
        reasons.append(reason)
    if missing_alternative_groups:
        reasons.append(f"{len(missing_alternative_groups)} verplichte outputanker(s) missen")
    if source_url_count < MIN_SOURCE_URLS:
        reasons.append(f'te weinig geldige bron-URLs op geldige Bron:-regels ({source_url_count})')
    if item_count and unique_source_url_count < item_count:
        reasons.append(
            f'te weinig unieke bron-URLs voor aantal items ({unique_source_url_count}/{item_count})'
        )
    if item_count and unique_item_title_count < item_count:
        duplicate_examples_text = ', '.join(
            f"{example['title']} x{example['count']}"
            for example in duplicate_item_title_examples[:3]
        )
        reason = f'niet alle itemtitels zijn uniek ({unique_item_title_count}/{item_count})'
        if duplicate_examples_text:
            reason += f': {duplicate_examples_text}'
        reasons.append(reason)
    if item_count and items_with_source_count < item_count:
        reason = f'niet elk item heeft een zichtbare bron-URL ({items_with_source_count}/{item_count})'
        if items_missing_source_examples:
            reason += f": {', '.join(items_missing_source_examples)}"
        reasons.append(reason)
    if item_count and items_with_valid_source_line_count < item_count:
        reason = (
            'niet elk item heeft een geldige Bron:-regel met alleen URLs '
            f'({items_with_valid_source_line_count}/{item_count})'
        )
        if items_invalid_source_line_examples:
            examples_text = ', '.join(
                f"{example['title']} -> {example['source_line']}"
                for example in items_invalid_source_line_examples[:3]
            )
            reason += f': {examples_text}'
            issue_summary = format_issue_counts(invalid_source_line_issue_counts)
            if issue_summary:
                reason += f' (patronen: {issue_summary})'
        elif items_missing_source_line_count:
            reason += f'; ontbrekende Bron:-regel {items_missing_source_line_count}'
        reasons.append(reason)
    if item_count >= 3 and first3_items_with_source_count < 3:
        reason = f'niet elk top-3 item heeft een zichtbare bron-URL ({first3_items_with_source_count}/3)'
        if top3_missing_source_examples:
            reason += f": {', '.join(top3_missing_source_examples)}"
        reasons.append(reason)
    if item_count >= 3 and first3_items_with_valid_source_line_count < 3:
        reason = (
            'niet elk top-3 item heeft een geldige Bron:-regel met alleen URLs '
            f'({first3_items_with_valid_source_line_count}/3)'
        )
        if top3_invalid_source_line_examples:
            examples_text = ', '.join(
                f"{example['title']} -> {example['source_line']}"
                for example in top3_invalid_source_line_examples[:3]
            )
            reason += f': {examples_text}'
            issue_summary = format_issue_counts(top3_invalid_source_line_issue_counts)
            if issue_summary:
                reason += f' (top3 patronen: {issue_summary})'
        elif first3_items_with_invalid_source_line_count:
            reason += f'; ongeldige Bron:-regels {first3_items_with_invalid_source_line_count}'
        reasons.append(reason)
    if item_count >= 3 and first3_unique_source_url_count < 3:
        reasons.append(
            f'top-3 items hergebruiken bron-URLs ({first3_unique_source_url_count}/3 uniek)'
        )
    if item_count >= 3 and first3_items_with_multiple_sources_count < MIN_TOP3_MULTI_SOURCE_ITEMS_FOR_STRONG_SIGNAL:
        reason = (
            f'te weinig top-3 items met meerdere bron-URLs ({first3_items_with_multiple_sources_count}/3, verwacht minstens {MIN_TOP3_MULTI_SOURCE_ITEMS_FOR_STRONG_SIGNAL})'
        )
        if top3_missing_multi_source_examples:
            reason += f": {', '.join(top3_missing_multi_source_examples)}"
        reasons.append(reason)
    if item_count >= 3 and first3_items_with_multi_domain_sources_count < MIN_TOP3_MULTI_DOMAIN_SOURCE_ITEMS_FOR_STRONG_SIGNAL:
        reason = (
            'te weinig top-3 items met bron-URLs uit meerdere domeinen '
            f'({first3_items_with_multi_domain_sources_count}/3, verwacht minstens {MIN_TOP3_MULTI_DOMAIN_SOURCE_ITEMS_FOR_STRONG_SIGNAL})'
        )
        if top3_missing_multi_domain_source_examples:
            reason += f": {', '.join(top3_missing_multi_domain_source_examples)}"
        reasons.append(reason)
    if source_url_count and source_domain_count < 2:
        reasons.append(f'te weinig unieke brondomeinen ({source_domain_count})')
    if item_count >= 3 and first3_source_domain_count < 2:
        reasons.append(f'te weinig unieke brondomeinen in top 3 ({first3_source_domain_count})')
    if source_url_count and primary_source_domain_count < 1:
        reasons.append('geen herkenbare primaire bron tussen URLs')
    if item_count >= 3 and first3_primary_source_domain_count < 1:
        reasons.append('geen herkenbare primaire bron in top 3 items')
    if item_count >= 3 and first3_items_with_primary_source_count < 3:
        reason = (
            'niet elk top-3 item heeft een herkenbare primaire bron '
            f'({first3_items_with_primary_source_count}/3)'
        )
        if top3_missing_primary_source_examples:
            reason += f": {', '.join(top3_missing_primary_source_examples)}"
        reasons.append(reason)
    if item_count >= 3 and first3_primary_source_family_count < 2:
        reasons.append(f'te weinig primaire bronfamilies in top 3 ({first3_primary_source_family_count})')
    if item_count >= 3 and dated_item_count < MIN_DATED_ITEMS_FOR_STRONG_SIGNAL:
        reasons.append(
            f'te weinig items met zichtbare datumvermelding ({dated_item_count}/{item_count}, verwacht minstens {MIN_DATED_ITEMS_FOR_STRONG_SIGNAL})'
        )
    if item_count and explicit_dated_item_count < item_count:
        reason = f'niet elk item heeft een expliciete Datum:-regel ({explicit_dated_item_count}/{item_count})'
        if items_missing_date_line_examples:
            reason += f": {', '.join(items_missing_date_line_examples)}"
        reasons.append(reason)
    if item_count >= 3 and explicit_recent_dated_first3_count < MIN_RECENT_ITEMS_FOR_STRONG_SIGNAL:
        reason = (
            f'te weinig top-3 items met expliciete Datum:-regel binnen {RECENT_ITEM_MAX_AGE_DAYS} dagen '
            f'({explicit_recent_dated_first3_count}/3)'
        )
        if top3_missing_recent_date_examples:
            reason += f": {', '.join(top3_missing_recent_date_examples)}"
        reasons.append(reason)
    if item_count >= 3 and fresh_dated_first3_count < MIN_FRESH_TOP3_ITEMS_FOR_STRONG_SIGNAL:
        reasons.append(
            f'te weinig verse items in top 3 ({fresh_dated_first3_count}/3 binnen {FRESH_ITEM_MAX_AGE_HOURS} uur)'
        )
    if item_count >= 3 and first3_evidenced_item_count < MIN_TOP3_EVIDENCED_ITEMS_FOR_STRONG_SIGNAL:
        reasons.append(
            f'te weinig top-3 items met zowel bron als recente datum ({first3_evidenced_item_count}/3)'
        )
    if item_count >= 3 and first3_primary_fresh_item_count < MIN_FRESH_TOP3_ITEMS_FOR_STRONG_SIGNAL:
        reason = (
            f'te weinig top-3 items met primaire bron én verse datum ({first3_primary_fresh_item_count}/3 binnen {FRESH_ITEM_MAX_AGE_HOURS} uur)'
        )
        if top3_missing_primary_fresh_examples:
            reason += f": {', '.join(top3_missing_primary_fresh_examples)}"
        reasons.append(reason)
    if future_dated_item_count:
        reasons.append(
            f'verdachte toekomstige datums in briefing ({future_dated_item_count} item(s), tolerantie {FUTURE_DATE_TOLERANCE_DAYS} dag)'
        )
    if category_theme_count < MIN_CATEGORY_THEME_COVERAGE:
        reasons.append(f'te weinig briefingcategorieën zichtbaar ({category_theme_count}/{len(CATEGORY_THEME_KEYWORDS)})')

    ok_text = (
        f'briefing-output ok ({item_count} items, {source_url_count} geldige bron-URLs, {unique_source_url_count} uniek, '
        f'titels {unique_item_title_count}/{item_count} uniek, items met juiste labelvolgorde {items_with_exact_field_order_count}/{item_count}, items met bron {items_with_source_count}/{item_count}, '
        f'geldige Bron:-regels {items_with_valid_source_line_count}/{item_count}, '
        f'items met meerdere bron-URLs {items_with_multiple_sources_count}/{item_count}, '
        f'items met multi-domein bronregels {items_with_multi_domain_sources_count}/{item_count}, '
        f'top3 bron-URLs {first3_unique_source_url_count}/3 uniek, top3 met meerdere bron-URLs {first3_items_with_multiple_sources_count}/3, '
        f'top3 met multi-domein bronregels {first3_items_with_multi_domain_sources_count}/3, '
        f'top3 met primaire bron {first3_items_with_primary_source_count}/3, '
        f'{source_domain_count} domeinen, top3 {first3_source_domain_count} domeinen, '
        f'top3 primaire bron-domeinen {first3_primary_source_domain_count}, {primary_source_domain_count} primaire bron-domeinen, '
        f'top3 primaire bronfamilies {first3_primary_source_family_count}, {primary_source_family_count} primaire bronfamilies, '
        f'datums {dated_item_count}/{item_count}, expliciete Datum-regels {explicit_dated_item_count}/{item_count}, '
        f'expliciet vers top3 {explicit_fresh_dated_first3_count}/3, expliciet recent top3 {explicit_recent_dated_first3_count}/3, '
        f'toekomstige datums {future_dated_item_count}, expliciet toekomstige datums {explicit_future_dated_item_count}, top3 met bron+recente datum {first3_evidenced_item_count}/3, '
        f'top3 met primaire bron+verse datum {first3_primary_fresh_item_count}/3, '
        f"exacte veldlabels Titel/Bron/Datum/Nieuw/Belangrijk/Relevant "
        f"{exact_field_line_counts['Titel:']}/{item_count}, {exact_field_line_counts['Bron:']}/{item_count}, "
        f"{exact_field_line_counts['Datum:']}/{item_count}, {exact_field_line_counts['Wat is er nieuw:']}/{item_count}, "
        f"{exact_field_line_counts['Waarom is dit belangrijk:']}/{item_count}, {exact_field_line_counts['Relevant voor Christian:']}/{item_count}, "
        f"{category_theme_count}/{len(CATEGORY_THEME_KEYWORDS)} categorie-thema's zichtbaar, "
        f"complete structuur {item_marker_min_count}x)"
    )

    return {
        'available': True,
        'ok': not reasons,
        'missing_markers': missing_markers,
        'item_marker_counts': item_marker_counts,
        'exact_field_line_counts': exact_field_line_counts,
        'item_count': item_count,
        'item_marker_min_count': item_marker_min_count,
        'missing_alternative_groups': missing_alternative_groups,
        'numbered_title_heading_count': numbered_title_heading_count,
        'numbered_title_heading_examples': numbered_title_heading_examples,
        'items_with_exact_field_order_count': items_with_exact_field_order_count,
        'items_with_field_order_mismatch_count': items_with_field_order_mismatch_count,
        'items_field_order_mismatch_examples': items_field_order_mismatch_examples,
        'source_url_count': source_url_count,
        'unique_source_url_count': unique_source_url_count,
        'source_urls': source_urls,
        'source_domains': source_domains,
        'source_domain_count': source_domain_count,
        'item_titles': item_titles,
        'unique_item_titles': unique_item_titles,
        'unique_item_title_count': unique_item_title_count,
        'duplicate_item_title_count': duplicate_item_title_count,
        'duplicate_item_title_examples': duplicate_item_title_examples,
        'items_with_source_count': items_with_source_count,
        'items_without_source_count': items_without_source_count,
        'items_missing_source_examples': items_missing_source_examples,
        'items_with_multiple_sources_count': items_with_multiple_sources_count,
        'items_with_multi_domain_sources_count': items_with_multi_domain_sources_count,
        'items_with_valid_source_line_count': items_with_valid_source_line_count,
        'items_with_invalid_source_line_count': items_with_invalid_source_line_count,
        'items_missing_source_line_count': items_missing_source_line_count,
        'invalid_source_line_issue_counts': dict(invalid_source_line_issue_counts),
        'items_invalid_source_line_examples': items_invalid_source_line_examples,
        'first3_items_with_source_count': first3_items_with_source_count,
        'top3_missing_source_examples': top3_missing_source_examples,
        'first3_items_with_multiple_sources_count': first3_items_with_multiple_sources_count,
        'first3_items_with_multi_domain_sources_count': first3_items_with_multi_domain_sources_count,
        'first3_items_with_valid_source_line_count': first3_items_with_valid_source_line_count,
        'first3_items_with_invalid_source_line_count': first3_items_with_invalid_source_line_count,
        'first3_items_with_primary_source_count': first3_items_with_primary_source_count,
        'top3_invalid_source_line_issue_counts': dict(top3_invalid_source_line_issue_counts),
        'top3_invalid_source_line_examples': top3_invalid_source_line_examples,
        'top3_missing_multi_source_examples': top3_missing_multi_source_examples,
        'top3_missing_multi_domain_source_examples': top3_missing_multi_domain_source_examples,
        'top3_missing_primary_source_examples': top3_missing_primary_source_examples,
        'first3_source_urls': first3_source_urls,
        'first3_unique_source_url_count': first3_unique_source_url_count,
        'first3_source_domains': first3_source_domains,
        'first3_source_domain_count': first3_source_domain_count,
        'first3_primary_source_domains': first3_primary_source_domains,
        'first3_primary_source_domain_count': first3_primary_source_domain_count,
        'first3_primary_source_families': first3_primary_source_families,
        'first3_primary_source_family_count': first3_primary_source_family_count,
        'primary_source_domains': primary_source_domains,
        'primary_source_domain_count': primary_source_domain_count,
        'primary_source_families': primary_source_families,
        'primary_source_family_count': primary_source_family_count,
        'dated_item_count': dated_item_count,
        'undated_item_count': undated_item_count,
        'explicit_dated_item_count': explicit_dated_item_count,
        'explicit_undated_item_count': explicit_undated_item_count,
        'items_missing_date_line_examples': items_missing_date_line_examples,
        'top3_missing_date_line_examples': top3_missing_date_line_examples,
        'recent_dated_item_count': recent_dated_item_count,
        'recent_dated_first3_count': recent_dated_first3_count,
        'explicit_recent_dated_item_count': explicit_recent_dated_item_count,
        'explicit_recent_dated_first3_count': explicit_recent_dated_first3_count,
        'top3_missing_recent_date_examples': top3_missing_recent_date_examples,
        'fresh_dated_item_count': fresh_dated_item_count,
        'fresh_dated_first3_count': fresh_dated_first3_count,
        'explicit_fresh_dated_item_count': explicit_fresh_dated_item_count,
        'explicit_fresh_dated_first3_count': explicit_fresh_dated_first3_count,
        'future_dated_item_count': future_dated_item_count,
        'future_dated_first3_count': future_dated_first3_count,
        'explicit_future_dated_item_count': explicit_future_dated_item_count,
        'explicit_future_dated_first3_count': explicit_future_dated_first3_count,
        'first3_evidenced_item_count': first3_evidenced_item_count,
        'first3_primary_fresh_item_count': first3_primary_fresh_item_count,
        'top3_missing_primary_fresh_examples': top3_missing_primary_fresh_examples,
        'recent_item_max_age_days': RECENT_ITEM_MAX_AGE_DAYS,
        'fresh_item_max_age_hours': FRESH_ITEM_MAX_AGE_HOURS,
        'future_date_tolerance_days': FUTURE_DATE_TOLERANCE_DAYS,
        'category_theme_hits': category_theme_hits,
        'category_theme_count': category_theme_count,
        'reasons': reasons,
        'text': ok_text if not reasons else '; '.join(reasons),
    }


def summarize_run(run, tz_name=DEFAULT_TZ, now_ms=None):
    if not run:
        return None
    usage = run.get('usage') or {}
    run_summary_text = run.get('summary')
    session_summary = load_session_final_text(run.get('sessionId'), preferred_agent_id=EXPECTED_AGENT_ID)
    summary_text = run_summary_text
    summary_source = 'runlog.summary'
    summary_path = None
    session_summary_length_chars = None
    session_summary_invalid_lines = None
    if session_summary and session_summary.get('text'):
        session_text = session_summary['text']
        session_summary_length_chars = session_summary.get('length_chars')
        session_summary_invalid_lines = session_summary.get('invalid_lines')
        if not isinstance(summary_text, str) or len(session_text) > len(summary_text):
            summary_text = session_text
            summary_source = 'session.final_text'
            summary_path = session_summary.get('path')
    error_text = run_summary_text or run.get('error') or run.get('deliveryError')
    if isinstance(error_text, str):
        error_text = ' '.join(error_text.split())[:240]
    summary_preview = None
    summary_preview_lines = []
    summary_length_chars = None
    summary_output_audit = audit_summary_output(summary_text, reference_ms=run.get('runAtMs') or now_ms)
    if isinstance(summary_text, str) and summary_text.strip():
        summary_length_chars = len(summary_text)
        summary_preview_lines = [line.strip() for line in summary_text.splitlines() if line.strip()][:3]
        if summary_preview_lines:
            summary_preview = ' | '.join(summary_preview_lines)[:280]
    run_at = run.get('runAtMs')
    return {
        'status': run.get('status'),
        'delivered': bool(run.get('delivered')),
        'delivery_status': run.get('deliveryStatus'),
        'run_at': run_at,
        'run_at_text': fmt_ts(run_at, tz_name),
        'run_at_hint': age_hint(run_at, now_ms) if now_ms is not None else None,
        'duration_ms': run.get('durationMs'),
        'duration_text': duration_hint(run.get('durationMs')),
        'model': run.get('model'),
        'provider': run.get('provider'),
        'usage': usage,
        'total_tokens': usage.get('total_tokens'),
        'input_tokens': usage.get('input_tokens'),
        'output_tokens': usage.get('output_tokens'),
        'summary_source': summary_source,
        'summary_path': summary_path,
        'run_summary_length_chars': len(run_summary_text) if isinstance(run_summary_text, str) else None,
        'session_summary_length_chars': session_summary_length_chars,
        'session_summary_invalid_lines': session_summary_invalid_lines,
        'summary_length_chars': summary_length_chars,
        'summary_preview_lines': summary_preview_lines,
        'summary_preview': summary_preview,
        'summary_output_audit': summary_output_audit,
        'error_text': error_text,
    }


def trailing_streak(runs, predicate):
    streak = 0
    for run in reversed(runs):
        if predicate(run):
            streak += 1
        else:
            break
    return streak


def find_session_path(session_id, preferred_agent_id=None):
    if not session_id:
        return None
    candidate_paths = []
    if preferred_agent_id:
        candidate_paths.append(AGENTS_DIR / preferred_agent_id / 'sessions' / f'{session_id}.jsonl')
    candidate_paths.extend(sorted(AGENTS_DIR.glob(f'*/sessions/{session_id}.jsonl')))
    seen = set()
    for candidate in candidate_paths:
        candidate_str = str(candidate)
        if candidate_str in seen:
            continue
        seen.add(candidate_str)
        if candidate.exists():
            return candidate
    return None


def load_session_final_text(session_id, preferred_agent_id=None):
    path = find_session_path(session_id, preferred_agent_id=preferred_agent_id)
    if not path:
        return None
    last_text = None
    total_lines = 0
    invalid_lines = 0
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        total_lines += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            invalid_lines += 1
            continue
        if row.get('type') != 'message':
            continue
        message = row.get('message') or {}
        if message.get('role') != 'assistant':
            continue
        text_chunks = [
            chunk.get('text', '')
            for chunk in (message.get('content') or [])
            if chunk.get('type') == 'text' and chunk.get('text')
        ]
        if text_chunks:
            last_text = '\n'.join(text_chunks)
    if not last_text:
        return None
    return {
        'path': str(path),
        'text': last_text,
        'length_chars': len(last_text),
        'total_lines': total_lines,
        'invalid_lines': invalid_lines,
    }


def load_runs(job_id):
    path = RUNS_DIR / f'{job_id}.jsonl'
    if not path.exists():
        return {
            'path': str(path),
            'exists': False,
            'rows': [],
            'total_lines': 0,
            'invalid_lines': 0,
        }
    rows = []
    total_lines = 0
    invalid_lines = 0
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        total_lines += 1
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            invalid_lines += 1
            continue
    return {
        'path': str(path),
        'exists': True,
        'rows': rows,
        'total_lines': total_lines,
        'invalid_lines': invalid_lines,
    }


def audit_runlog(runlog_info, finished_runs):
    exists = bool((runlog_info or {}).get('exists'))
    total_lines = int((runlog_info or {}).get('total_lines') or 0)
    invalid_lines = int((runlog_info or {}).get('invalid_lines') or 0)
    rows = (runlog_info or {}).get('rows') or []
    reasons = []

    if not exists:
        text = 'runlog nog niet aanwezig'
    else:
        if total_lines == 0:
            reasons.append('runlog bestaat maar is leeg')
        if invalid_lines:
            reasons.append(f'runlog heeft {invalid_lines} onleesbare regel(s)')
        if total_lines > 0 and not rows:
            reasons.append('runlog bevat geen leesbare events')
        text = 'runlog ok'
        if reasons:
            text = '; '.join(reasons)
        else:
            text = f'runlog ok ({len(rows)} events, {len(finished_runs)} finished)'

    return {
        'ok': not reasons,
        'exists': exists,
        'path': (runlog_info or {}).get('path'),
        'total_lines': total_lines,
        'invalid_lines': invalid_lines,
        'readable_events': len(rows),
        'finished_events': len(finished_runs),
        'reasons': reasons,
        'text': text,
    }


def filter_runs_for_current_config(runs, updated_at):
    if not runs:
        return []
    if not updated_at:
        return list(runs)
    return [run for run in runs if (run.get('runAtMs') or 0) >= updated_at]


def run_is_proof_qualified(run, delivery_mode):
    if not run or run.get('status') != 'ok':
        return False
    if delivery_mode in (None, 'none'):
        return True
    return bool(run.get('delivered'))


def audit_proof_freshness(updated_at, finished_runs, successful_runs, delivered_runs, first_run_pending, tz_name):
    latest_finished_at = ((finished_runs or [])[-1] or {}).get('runAtMs') if finished_runs else None
    latest_success_at = ((successful_runs or [])[-1] or {}).get('runAtMs') if successful_runs else None
    latest_delivered_at = ((delivered_runs or [])[-1] or {}).get('runAtMs') if delivered_runs else None

    stale_finished = bool(updated_at and latest_finished_at and updated_at > latest_finished_at)
    stale_success = bool(updated_at and latest_success_at and updated_at > latest_success_at)
    stale_delivered = bool(updated_at and latest_delivered_at and updated_at > latest_delivered_at)

    reasons = []
    if not finished_runs:
        text = 'geen runbewijs voor huidige config'
        if first_run_pending:
            text = 'eerste runbewijs voor huidige config nog in afwachting'
    elif stale_finished:
        reasons.append(
            f"config nieuwer dan laatste run ({fmt_ts(updated_at, tz_name)} > {fmt_ts(latest_finished_at, tz_name)})"
        )
        text = 'runbewijs verouderd voor huidige config'
    else:
        text = 'runbewijs actueel voor huidige config'

    if finished_runs and stale_success:
        reasons.append('laatste succesvolle run is nog van oudere config')
    if finished_runs and delivered_runs and stale_delivered:
        reasons.append('laatste afgeleverde run is nog van oudere config')

    if reasons:
        text = '; '.join([text] + reasons)

    return {
        'ok': first_run_pending or (bool(finished_runs) and not stale_finished),
        'has_run_proof': bool(finished_runs),
        'latest_finished_at': latest_finished_at,
        'latest_finished_at_text': fmt_ts(latest_finished_at, tz_name),
        'latest_success_at': latest_success_at,
        'latest_success_at_text': fmt_ts(latest_success_at, tz_name),
        'latest_delivered_at': latest_delivered_at,
        'latest_delivered_at_text': fmt_ts(latest_delivered_at, tz_name),
        'stale_finished': stale_finished,
        'stale_success': stale_success,
        'stale_delivered': stale_delivered,
        'reasons': reasons,
        'text': text,
    }


def audit_payload(job):
    payload = job.get('payload') or {}
    message = payload.get('message') or ''
    missing_categories = [marker for marker in REQUIRED_CATEGORY_MARKERS if marker not in message]
    missing_prompt_markers = [marker for marker in REQUIRED_PROMPT_MARKERS if marker not in message]
    missing_format_markers = [marker for marker in REQUIRED_FORMAT_MARKERS if marker not in message]
    tools_allow = set(payload.get('toolsAllow') or [])
    missing_tools = sorted(REQUIRED_TOOLS_ALLOW - tools_allow)
    unexpected_tools = sorted(tools_allow - REQUIRED_TOOLS_ALLOW)
    timeout_seconds = int(payload.get('timeoutSeconds') or 0)
    message_sha256 = hashlib.sha256(message.encode('utf-8')).hexdigest() if message else None
    light_context = bool(payload.get('lightContext'))

    reasons = []
    if missing_categories:
        reasons.append(f"{len(missing_categories)} briefingcategorie(ën) missen")
    if missing_prompt_markers:
        reasons.append(f"{len(missing_prompt_markers)} promptanker(s) missen")
    if missing_format_markers:
        reasons.append(f"{len(missing_format_markers)} formaat/taal-anker(s) missen")
    if missing_tools:
        reasons.append(f"toolsAllow mist {', '.join(missing_tools)}")
    if unexpected_tools:
        reasons.append(f"toolsAllow bevat extra tool(s): {', '.join(unexpected_tools)}")
    if timeout_seconds < 300:
        reasons.append(f'timeoutSeconds te laag ({timeout_seconds})')
    if payload.get('kind') != 'agentTurn':
        reasons.append(f"payload.kind is {payload.get('kind') or 'onbekend'}")
    if 'bronnenlijst met URLs' not in message:
        reasons.append('bronnenlijst met URLs ontbreekt')
    if 'Als er weinig echt nieuws is, zeg dat eerlijk' not in message:
        reasons.append('eerlijke low-news instructie ontbreekt')
    if not light_context:
        reasons.append('lightContext staat uit')

    return {
        'ok': not reasons,
        'missing_categories': missing_categories,
        'missing_prompt_markers': missing_prompt_markers,
        'missing_format_markers': missing_format_markers,
        'missing_tools_allow': missing_tools,
        'unexpected_tools_allow': unexpected_tools,
        'timeout_seconds': timeout_seconds,
        'light_context': light_context,
        'tools_allow': sorted(tools_allow),
        'message_sha256': message_sha256,
        'message_sha256_short': message_sha256[:12] if message_sha256 else None,
        'message_length': len(message),
        'reasons': reasons,
        'text': 'prompt/config ok' if not reasons else '; '.join(reasons),
    }


def audit_runtime(job, tz_name):
    schedule = job.get('schedule') or {}
    delivery = job.get('delivery') or {}

    reasons = []
    schedule_expr = schedule.get('expr')
    schedule_tz = schedule.get('tz') or tz_name
    delivery_channel = delivery.get('channel') or 'onbekend'
    delivery_to = str(delivery.get('to') or 'onbekend')
    delivery_mode = delivery.get('mode')
    session_target = job.get('sessionTarget') or 'onbekend'
    wake_mode = job.get('wakeMode') or 'onbekend'
    agent_id = job.get('agentId') or 'onbekend'
    session_key = job.get('sessionKey') or 'onbekend'

    if schedule.get('kind') != 'cron':
        reasons.append(f"schedule.kind is {schedule.get('kind') or 'onbekend'}")
    if schedule_expr != EXPECTED_SCHEDULE_EXPR:
        reasons.append(f"cron expr is {schedule_expr or 'onbekend'}")
    if schedule_tz != DEFAULT_TZ:
        reasons.append(f"cron tz is {schedule_tz}")
    if delivery_channel != EXPECTED_DELIVERY_CHANNEL:
        reasons.append(f"delivery channel is {delivery_channel}")
    if delivery_to != EXPECTED_DELIVERY_TO:
        reasons.append(f"delivery target is {delivery_to}")
    if delivery_mode != EXPECTED_DELIVERY_MODE:
        reasons.append(f"delivery mode is {delivery_mode or 'onbekend'}")
    if session_target != EXPECTED_SESSION_TARGET:
        reasons.append(f"sessionTarget is {session_target}")
    if wake_mode != EXPECTED_WAKE_MODE:
        reasons.append(f"wakeMode is {wake_mode}")
    if agent_id != EXPECTED_AGENT_ID:
        reasons.append(f"agentId is {agent_id}")
    if session_key != EXPECTED_SESSION_KEY:
        reasons.append(f"sessionKey is {session_key}")

    return {
        'ok': not reasons,
        'schedule_kind': schedule.get('kind'),
        'schedule_expr': schedule_expr,
        'schedule_tz': schedule_tz,
        'delivery_channel': delivery_channel,
        'delivery_to': delivery_to,
        'delivery_mode': delivery_mode,
        'session_target': session_target,
        'wake_mode': wake_mode,
        'agent_id': agent_id,
        'session_key': session_key,
        'expected_session_key': EXPECTED_SESSION_KEY,
        'reasons': reasons,
        'text': 'schedule/delivery/execution/session ok' if not reasons else '; '.join(reasons),
    }


def build_status(job_name=TARGET_JOB_NAME):
    jobs = load_jobs()
    job = next((job for job in jobs if job.get('name') == job_name), None)
    now_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    if not job:
        return {
            'ok': False,
            'found': False,
            'job_name': job_name,
            'text': f'AI-briefing job {job_name} niet gevonden',
        }

    schedule = job.get('schedule') or {}
    state = job.get('state') or {}
    delivery = job.get('delivery') or {}
    tz_name = schedule.get('tz') or DEFAULT_TZ
    runlog_info = load_runs(job['id'])
    run_file_exists = runlog_info.get('exists', False)
    runs = runlog_info.get('rows') or []
    finished_runs = [run for run in runs if run.get('action') == 'finished']
    delivered_runs = [run for run in finished_runs if run.get('delivered')]
    successful_runs = [run for run in finished_runs if run.get('status') == 'ok']
    last_run = finished_runs[-1] if finished_runs else None
    last_delivered = delivered_runs[-1] if delivered_runs else None
    last_success = successful_runs[-1] if successful_runs else None
    last_run_summary = summarize_run(last_run, tz_name=tz_name, now_ms=now_ms)
    last_success_summary = summarize_run(last_success, tz_name=tz_name, now_ms=now_ms)
    last_delivered_summary = summarize_run(last_delivered, tz_name=tz_name, now_ms=now_ms)
    recent_runs_summary = [
        summarize_run(run, tz_name=tz_name, now_ms=now_ms)
        for run in finished_runs[-3:]
    ]
    success_rate = (len(successful_runs) / len(finished_runs)) if finished_runs else None
    delivery_rate = (len(delivered_runs) / len(finished_runs)) if finished_runs else None
    success_streak = trailing_streak(finished_runs, lambda run: run.get('status') == 'ok') if finished_runs else 0
    delivery_streak = trailing_streak(finished_runs, lambda run: bool(run.get('delivered'))) if finished_runs else 0
    next_run_at = state.get('nextRunAtMs')
    previous_run_slot_at = previous_expected_run_at(next_run_at, schedule.get('expr'))
    last_run_at = (last_run or {}).get('runAtMs') or state.get('lastRunAtMs')
    created_at = job.get('createdAtMs')
    updated_at = job.get('updatedAtMs') or created_at
    current_config_runs = filter_runs_for_current_config(finished_runs, updated_at)
    current_config_successful_runs = filter_runs_for_current_config(successful_runs, updated_at)
    current_config_delivered_runs = filter_runs_for_current_config(delivered_runs, updated_at)
    proof_qualified_runs = [
        run for run in current_config_runs
        if run_is_proof_qualified(run, delivery.get('mode'))
    ]
    last_proof_qualified_run = proof_qualified_runs[-1] if proof_qualified_runs else None
    last_proof_qualified_run_at = (last_proof_qualified_run or {}).get('runAtMs')
    last_proof_qualified_run_summary = summarize_run(last_proof_qualified_run, tz_name=tz_name, now_ms=now_ms)
    first_run_pending = bool(
        not finished_runs
        and created_at
        and next_run_at
        and (
            previous_run_slot_at is None
            or created_at > previous_run_slot_at
        )
    )
    last_run_status = state.get('lastRunStatus') or state.get('lastStatus')
    last_delivery_status = state.get('lastDeliveryStatus')
    consecutive_errors = int(state.get('consecutiveErrors') or 0)

    delivery_channel = delivery.get('channel') or 'onbekend'
    delivery_to = delivery.get('to') or 'onbekend'
    proof_text = 'runlog aanwezig' if run_file_exists else 'runlog nog niet aangemaakt'
    payload_audit = audit_payload(job)
    runtime_audit = audit_runtime(job, tz_name)
    next_run_audit = audit_next_run(job, next_run_at, now_ms, tz_name)
    storage_audit = audit_storage(job['id'])
    runlog_audit = audit_runlog(runlog_info, finished_runs)
    uniqueness_audit = audit_uniqueness(jobs, job)
    proof_freshness = audit_proof_freshness(updated_at, finished_runs, successful_runs, delivered_runs, first_run_pending, tz_name)

    overdue_grace_ms = 15 * 60 * 1000
    overdue = bool(next_run_at and now_ms > (next_run_at + overdue_grace_ms))
    overdue_by_ms = max(0, now_ms - next_run_at) if overdue and next_run_at else 0
    overdue_hint = age_hint(now_ms - overdue_by_ms, now_ms) if overdue_by_ms else None
    proof_due_at = (next_run_at + overdue_grace_ms) if next_run_at and not finished_runs else None

    attention_reasons = []
    if not job.get('enabled'):
        attention_reasons.append('job staat uit')
    if not finished_runs and previous_run_slot_at and created_at and created_at <= previous_run_slot_at:
        attention_reasons.append(
            f'eerste runbewijs ontbreekt sinds vorige geplande slot {fmt_ts(previous_run_slot_at, tz_name)}'
        )
    if overdue:
        attention_reasons.append(f'volgende run is over tijd ({overdue_hint})')
    if consecutive_errors:
        attention_reasons.append(f'{consecutive_errors} opeenvolgende cronfout(en)')
    if last_run_status and last_run_status != 'ok':
        error_text = (last_run_summary or {}).get('error_text')
        if error_text:
            attention_reasons.append(f'laatste runstatus {last_run_status}: {error_text}')
        else:
            attention_reasons.append(f'laatste runstatus {last_run_status}')
    if finished_runs and delivery.get('mode') not in (None, 'none') and last_delivery_status not in (None, 'delivered', 'not-requested'):
        delivery_error_text = (last_run or {}).get('deliveryError') or (last_run_summary or {}).get('error_text')
        if isinstance(delivery_error_text, str):
            delivery_error_text = ' '.join(delivery_error_text.split())[:240]
        if delivery_error_text:
            attention_reasons.append(f'laatste delivery-status {last_delivery_status}: {delivery_error_text}')
        else:
            attention_reasons.append(f'laatste delivery-status {last_delivery_status}')
    if not payload_audit.get('ok'):
        attention_reasons.append(f"prompt/config: {payload_audit.get('text')}")
    if not runtime_audit.get('ok'):
        attention_reasons.append(f"schedule/delivery: {runtime_audit.get('text')}")
    if not next_run_audit.get('ok'):
        attention_reasons.append(f"next run: {next_run_audit.get('text')}")
    if not storage_audit.get('ok'):
        attention_reasons.append(f"storage: {storage_audit.get('text')}")
    if not runlog_audit.get('ok'):
        attention_reasons.append(f"runlog: {runlog_audit.get('text')}")
    if not uniqueness_audit.get('ok'):
        attention_reasons.append(f"uniqueness: {uniqueness_audit.get('text')}")
    if finished_runs and not proof_freshness.get('ok'):
        attention_reasons.append(f"proof freshness: {proof_freshness.get('text')}")
    last_run_output_audit = (last_run_summary or {}).get('summary_output_audit') or {}
    if last_run_output_audit.get('available') and not last_run_output_audit.get('ok'):
        attention_reasons.append(f"briefing-output: {last_run_output_audit.get('text')}")

    summary = {
        'ok': not attention_reasons,
        'found': True,
        'job_id': job.get('id'),
        'job_name': job.get('name'),
        'enabled': bool(job.get('enabled')),
        'delivery_channel': delivery_channel,
        'delivery_to': delivery_to,
        'delivery_text': f'{delivery_channel}:{delivery_to}',
        'delivery_mode': delivery.get('mode'),
        'schedule': schedule,
        'schedule_expr': schedule.get('expr'),
        'schedule_tz': tz_name,
        'payload_audit': payload_audit,
        'runtime_audit': runtime_audit,
        'next_run_audit': next_run_audit,
        'storage_audit': storage_audit,
        'runlog_audit': runlog_audit,
        'uniqueness_audit': uniqueness_audit,
        'proof_freshness': proof_freshness,
        'state': state,
        'created_at': created_at,
        'created_at_text': fmt_ts(created_at, tz_name),
        'created_at_hint': age_hint(created_at, now_ms),
        'updated_at': updated_at,
        'updated_at_text': fmt_ts(updated_at, tz_name),
        'updated_at_hint': age_hint(updated_at, now_ms),
        'run_file_exists': run_file_exists,
        'proof_text': proof_text,
        'runs_total': len(finished_runs),
        'runs_ok': len(successful_runs),
        'runs_delivered': len(delivered_runs),
        'current_config_runs_total': len(current_config_runs),
        'current_config_runs_ok': len(current_config_successful_runs),
        'current_config_runs_delivered': len(current_config_delivered_runs),
        'proof_target_runs': PROOF_TARGET_RUNS,
        'proof_qualified_runs': len(proof_qualified_runs),
        'proof_runs_remaining': max(0, PROOF_TARGET_RUNS - len(proof_qualified_runs)),
        'proof_target_met': len(proof_qualified_runs) >= PROOF_TARGET_RUNS,
        'last_proof_qualified_run': last_proof_qualified_run,
        'last_proof_qualified_run_at': last_proof_qualified_run_at,
        'last_proof_qualified_run_at_text': fmt_ts(last_proof_qualified_run_at, tz_name),
        'last_proof_qualified_run_hint': age_hint(last_proof_qualified_run_at, now_ms),
        'last_proof_qualified_run_summary': last_proof_qualified_run_summary,
        'success_rate': success_rate,
        'delivery_rate': delivery_rate,
        'success_rate_pct': round(success_rate * 100, 1) if success_rate is not None else None,
        'delivery_rate_pct': round(delivery_rate * 100, 1) if delivery_rate is not None else None,
        'success_streak': success_streak,
        'delivery_streak': delivery_streak,
        'has_run_proof': bool(finished_runs),
        'first_run_pending': first_run_pending,
        'last_run': last_run,
        'last_success': last_success,
        'last_delivered': last_delivered,
        'last_run_summary': last_run_summary,
        'last_success_summary': last_success_summary,
        'last_delivered_summary': last_delivered_summary,
        'recent_runs_summary': recent_runs_summary,
        'last_run_status': last_run_status,
        'last_delivery_status': last_delivery_status,
        'consecutive_errors': consecutive_errors,
        'overdue': overdue,
        'overdue_hint': overdue_hint,
        'attention_needed': bool(attention_reasons),
        'attention_reasons': attention_reasons,
        'attention_text': '; '.join(attention_reasons) if attention_reasons else None,
        'next_run_at': next_run_at,
        'next_run_at_text': fmt_ts(next_run_at, tz_name),
        'next_run_hint': future_hint(next_run_at, now_ms),
        'previous_run_slot_at': previous_run_slot_at,
        'previous_run_slot_at_text': fmt_ts(previous_run_slot_at, tz_name),
        'previous_run_slot_hint': age_hint(previous_run_slot_at, now_ms),
        'proof_due_at': proof_due_at,
        'proof_due_at_text': fmt_ts(proof_due_at, tz_name),
        'proof_due_hint': future_hint(proof_due_at, now_ms),
        'last_run_at': last_run_at,
        'last_run_at_text': fmt_ts(last_run_at, tz_name),
        'last_run_hint': age_hint(last_run_at, now_ms),
    }

    proof_target_due_at = projected_proof_target_due_at(
        next_run_at=next_run_at,
        remaining_runs=summary['proof_runs_remaining'],
        expr=summary['schedule_expr'],
    )
    summary['proof_target_due_at'] = proof_target_due_at
    summary['proof_target_due_at_text'] = fmt_ts(proof_target_due_at, tz_name)
    summary['proof_target_due_hint'] = future_hint(proof_target_due_at, now_ms)
    proof_target_run_slots = projected_proof_run_slots(
        next_run_at=next_run_at,
        remaining_runs=summary['proof_runs_remaining'],
        expr=summary['schedule_expr'],
    )
    summary['proof_target_run_slots'] = proof_target_run_slots
    summary['proof_target_run_slot_texts'] = [fmt_ts(slot, tz_name) for slot in proof_target_run_slots]
    summary['proof_target_run_slot_hints'] = [future_hint(slot, now_ms) for slot in proof_target_run_slots]
    if proof_target_run_slots:
        summary['proof_target_run_slots_text'] = ', '.join(summary['proof_target_run_slot_texts'])
    else:
        summary['proof_target_run_slots_text'] = None
    proof_next_qualifying_slot_at = proof_target_run_slots[0] if proof_target_run_slots else None
    summary['proof_next_qualifying_slot_at'] = proof_next_qualifying_slot_at
    summary['proof_next_qualifying_slot_at_text'] = fmt_ts(proof_next_qualifying_slot_at, tz_name)
    summary['proof_next_qualifying_slot_hint'] = future_hint(proof_next_qualifying_slot_at, now_ms)

    proof_runs_remaining = summary['proof_runs_remaining']
    proof_progress_text = (
        f"bewijsdoel gehaald ({len(proof_qualified_runs)}/{PROOF_TARGET_RUNS} gekwalificeerde runs voor huidige config)"
        if len(proof_qualified_runs) >= PROOF_TARGET_RUNS
        else f"bewijsprogressie {len(proof_qualified_runs)}/{PROOF_TARGET_RUNS} gekwalificeerde runs voor huidige config, nog {proof_runs_remaining} te gaan"
    )

    if finished_runs:
        status_text = f"{len(successful_runs)}/{len(finished_runs)} runs ok"
        if delivered_runs:
            status_text += f", {len(delivered_runs)} afgeleverd"
        if success_streak:
            status_text += f", streak {success_streak}"
        if last_run_summary and last_run_summary.get('duration_text'):
            status_text += f", laatste duur {last_run_summary['duration_text']}"
        if last_run_at:
            status_text += f", laatste {summary['last_run_hint']}"
    elif first_run_pending:
        status_text = f"eerste run nog niet geweest, eerste run {summary['next_run_hint']}"
        if summary.get('proof_due_hint'):
            status_text += f", bewijs verwacht {summary['proof_due_hint']}"
    else:
        status_text = f"nog geen runbewijs, volgende run {summary['next_run_hint']}"

    readiness_phase = 'attention'
    readiness_text = 'let op vereist'
    if not attention_reasons:
        if not finished_runs:
            readiness_phase = 'ready-for-first-run'
            readiness_text = 'klaar voor eerste run'
        elif len(proof_qualified_runs) < PROOF_TARGET_RUNS:
            readiness_phase = 'proving'
            readiness_text = proof_progress_text
        else:
            readiness_phase = 'proved'
            readiness_text = proof_progress_text
    elif finished_runs:
        readiness_text = f'{proof_progress_text}; runbewijs met aandachtspunt'

    if summary['proof_target_met']:
        proof_plan_text = f"bewijspad afgerond, {len(proof_qualified_runs)}/{PROOF_TARGET_RUNS} gekwalificeerde runs binnen"
    elif proof_next_qualifying_slot_at and proof_target_due_at:
        proof_plan_text = (
            f"bewijspad op schema, eerstvolgende kwalificatierun {summary['proof_next_qualifying_slot_at_text']}"
            f" ({summary['proof_next_qualifying_slot_hint']}), doel {summary['proof_target_due_at_text']}"
        )
    elif proof_next_qualifying_slot_at:
        proof_plan_text = (
            f"bewijspad wacht op kwalificatierun {summary['proof_next_qualifying_slot_at_text']}"
            f" ({summary['proof_next_qualifying_slot_hint']})"
        )
    else:
        proof_plan_text = 'bewijspad wacht op geldig kwalificatieslot'

    summary['text'] = status_text
    summary['proof_progress_text'] = proof_progress_text
    summary['proof_plan_text'] = proof_plan_text
    summary['readiness_phase'] = readiness_phase
    summary['readiness_text'] = readiness_text
    return summary


def render_summary_audit_text(data):
    if not data.get('available'):
        return data.get('text', 'geen briefinginhoud om te auditen')
    parts = [data.get('text', 'briefing-output onbekend')]
    if data.get('source_url_count') is not None:
        parts.append(f"bron-URLs {data['source_url_count']}")
    if data.get('unique_source_url_count') is not None:
        parts.append(f"unieke bron-URLs {data['unique_source_url_count']}")
    if data.get('source_domain_count') is not None:
        parts.append(f"brondomeinen {data['source_domain_count']}")
    if data.get('first3_source_domain_count') is not None:
        parts.append(f"top3 brondomeinen {data['first3_source_domain_count']}")
    if data.get('unique_item_title_count') is not None and data.get('item_count') is not None:
        parts.append(f"unieke titels {data['unique_item_title_count']}/{data['item_count']}")
    duplicate_examples = data.get('duplicate_item_title_examples') or []
    if duplicate_examples:
        parts.append(
            'dubbele titels ' + ', '.join(
                f"{example.get('title', 'onbekend')} x{example.get('count', 0)}"
                for example in duplicate_examples[:3]
            )
        )
    items_missing_source_examples = data.get('items_missing_source_examples') or []
    if items_missing_source_examples:
        parts.append('items zonder bron ' + ', '.join(items_missing_source_examples[:3]))
    top3_missing_source_examples = data.get('top3_missing_source_examples') or []
    if top3_missing_source_examples:
        parts.append('top3 zonder bron ' + ', '.join(top3_missing_source_examples[:3]))
    top3_missing_multi_source_examples = data.get('top3_missing_multi_source_examples') or []
    if top3_missing_multi_source_examples:
        parts.append('top3 zonder multi-source ' + ', '.join(top3_missing_multi_source_examples[:3]))
    top3_missing_multi_domain_source_examples = data.get('top3_missing_multi_domain_source_examples') or []
    if top3_missing_multi_domain_source_examples:
        parts.append('top3 zonder multi-domein bronregel ' + ', '.join(top3_missing_multi_domain_source_examples[:3]))
    top3_missing_primary_source_examples = data.get('top3_missing_primary_source_examples') or []
    if top3_missing_primary_source_examples:
        parts.append('top3 zonder primaire bron ' + ', '.join(top3_missing_primary_source_examples[:3]))
    top3_missing_recent_date_examples = data.get('top3_missing_recent_date_examples') or []
    if top3_missing_recent_date_examples:
        parts.append('top3 zonder recente datum ' + ', '.join(top3_missing_recent_date_examples[:3]))
    top3_missing_primary_fresh_examples = data.get('top3_missing_primary_fresh_examples') or []
    if top3_missing_primary_fresh_examples:
        parts.append('top3 zonder primaire+verse combo ' + ', '.join(top3_missing_primary_fresh_examples[:3]))
    if data.get('items_with_exact_field_order_count') is not None and data.get('item_count') is not None:
        parts.append(f"items met juiste labelvolgorde {data['items_with_exact_field_order_count']}/{data['item_count']}")
    mismatch_examples = data.get('items_field_order_mismatch_examples') or []
    if mismatch_examples:
        parts.append('labelvolgorde fout ' + ', '.join(example['title'] for example in mismatch_examples[:3]))
    if data.get('items_with_source_count') is not None and data.get('item_count') is not None:
        parts.append(f"items met bron {data['items_with_source_count']}/{data['item_count']}")
    if data.get('items_with_multiple_sources_count') is not None and data.get('item_count') is not None:
        parts.append(f"items met meerdere bron-URLs {data['items_with_multiple_sources_count']}/{data['item_count']}")
    if data.get('items_with_multi_domain_sources_count') is not None and data.get('item_count') is not None:
        parts.append(f"items met multi-domein bronregels {data['items_with_multi_domain_sources_count']}/{data['item_count']}")
    if data.get('first3_items_with_source_count') is not None:
        parts.append(f"top3 met bron {data['first3_items_with_source_count']}/3")
    if data.get('first3_items_with_multiple_sources_count') is not None:
        parts.append(f"top3 met meerdere bron-URLs {data['first3_items_with_multiple_sources_count']}/3")
    if data.get('first3_items_with_multi_domain_sources_count') is not None:
        parts.append(f"top3 met multi-domein bronregels {data['first3_items_with_multi_domain_sources_count']}/3")
    if data.get('first3_items_with_primary_source_count') is not None:
        parts.append(f"top3 met primaire bron {data['first3_items_with_primary_source_count']}/3")
    if data.get('first3_unique_source_url_count') is not None:
        parts.append(f"top3 unieke bron-URLs {data['first3_unique_source_url_count']}/3")
    if data.get('primary_source_domain_count') is not None:
        parts.append(f"primaire brondomeinen {data['primary_source_domain_count']}")
    if data.get('first3_primary_source_domain_count') is not None:
        parts.append(f"top3 primaire brondomeinen {data['first3_primary_source_domain_count']}")
    if data.get('first3_primary_source_family_count') is not None:
        parts.append(f"top3 primaire bronfamilies {data['first3_primary_source_family_count']}")
    if data.get('dated_item_count') is not None and data.get('item_count') is not None:
        parts.append(f"datums {data['dated_item_count']}/{data['item_count']}")
    if data.get('fresh_dated_first3_count') is not None:
        parts.append(
            f"vers top3 {data['fresh_dated_first3_count']}/3 ({data.get('fresh_item_max_age_hours', FRESH_ITEM_MAX_AGE_HOURS)}u)"
        )
    if data.get('recent_dated_first3_count') is not None:
        parts.append(
            f"recent top3 {data['recent_dated_first3_count']}/3 ({data.get('recent_item_max_age_days', RECENT_ITEM_MAX_AGE_DAYS)}d)"
        )
    if data.get('future_dated_item_count') is not None:
        parts.append(f"toekomstige datums {data['future_dated_item_count']}")
    if data.get('first3_evidenced_item_count') is not None:
        parts.append(f"top3 met bron+recente datum {data['first3_evidenced_item_count']}/3")
    if data.get('first3_primary_fresh_item_count') is not None:
        parts.append(
            f"top3 met primaire bron+verse datum {data['first3_primary_fresh_item_count']}/3"
        )
    if data.get('category_theme_count') is not None:
        parts.append(f"categorie-thema's {data['category_theme_count']}/{len(CATEGORY_THEME_KEYWORDS)}")
    if data.get('item_marker_min_count') is not None:
        parts.append(f"structuur {data['item_marker_min_count']}x")
    if data.get('reasons'):
        parts.append('redenen: ' + '; '.join(data['reasons']))
    return ' | '.join(parts)


def render_text(data):
    if not data.get('found'):
        return data.get('text', 'AI-briefingstatus onbekend')
    parts = [f"AI-briefing: {'aan' if data.get('enabled') else 'uit'}"]
    parts.append(data.get('text', 'onbekend'))
    if data.get('readiness_text'):
        parts.append(data['readiness_text'])
    if data.get('delivery_text'):
        parts.append(f"naar {data['delivery_text']}")
    if data.get('proof_text'):
        parts.append(data['proof_text'])
    payload_audit = data.get('payload_audit') or {}
    if data.get('attention_text'):
        parts.append(f"let op: {data['attention_text']}")
    else:
        runtime_audit = data.get('runtime_audit') or {}
        if runtime_audit.get('text'):
            parts.append(runtime_audit.get('text'))
        next_run_audit = data.get('next_run_audit') or {}
        if next_run_audit.get('text'):
            parts.append(next_run_audit.get('text'))
        storage_audit = data.get('storage_audit') or {}
        if storage_audit.get('text'):
            parts.append(storage_audit.get('text'))
        runlog_audit = data.get('runlog_audit') or {}
        if runlog_audit.get('text'):
            parts.append(runlog_audit.get('text'))
        uniqueness_audit = data.get('uniqueness_audit') or {}
        if uniqueness_audit.get('text'):
            parts.append(uniqueness_audit.get('text'))
        proof_freshness = data.get('proof_freshness') or {}
        if proof_freshness.get('text'):
            parts.append(proof_freshness.get('text'))
        if data.get('proof_progress_text'):
            parts.append(data.get('proof_progress_text'))
        if payload_audit.get('text'):
            parts.append(payload_audit.get('text'))
    runtime_audit = data.get('runtime_audit') or {}
    if runtime_audit.get('session_target') and runtime_audit.get('wake_mode'):
        parts.append(f"route {runtime_audit['session_target']}/{runtime_audit['wake_mode']} via {runtime_audit.get('agent_id') or 'onbekend'}")
    if data.get('updated_at_hint'):
        fingerprint = payload_audit.get('message_sha256_short')
        if fingerprint:
            parts.append(f"config {data['updated_at_hint']} gewijzigd, hash {fingerprint}")
        else:
            parts.append(f"config {data['updated_at_hint']} gewijzigd")
    if data.get('next_run_at_text'):
        parts.append(f"volgende {data['next_run_at_text']}")
    if data.get('proof_due_at_text'):
        parts.append(f"bewijs verwacht uiterlijk {data['proof_due_at_text']}")
    if data.get('proof_target_due_at_text'):
        parts.append(f"bewijsdoel bij groene runs uiterlijk {data['proof_target_due_at_text']}")
    if data.get('proof_plan_text'):
        parts.append(data['proof_plan_text'])
    if data.get('proof_target_run_slots_text'):
        parts.append(f"kwalificatie-slots {data['proof_target_run_slots_text']}")
    if data.get('last_run_at_text'):
        parts.append(f"laatste {data['last_run_at_text']}")
    last_run_summary = data.get('last_run_summary') or {}
    if last_run_summary.get('model'):
        model_text = last_run_summary['model']
        if last_run_summary.get('provider'):
            model_text = f"{last_run_summary['provider']}/{model_text}"
        parts.append(f"laatste model {model_text}")
    if last_run_summary.get('duration_text'):
        token_text = None
        if last_run_summary.get('total_tokens') is not None:
            token_text = f"{last_run_summary['total_tokens']} tokens"
        duration_text = f"laatste duur {last_run_summary['duration_text']}"
        if token_text:
            duration_text += f", {token_text}"
        parts.append(duration_text)
    if last_run_summary.get('summary_preview'):
        parts.append(f"laatste briefing-preview {last_run_summary['summary_preview']}")
    if last_run_summary.get('summary_source'):
        parts.append(f"briefingbron {last_run_summary['summary_source']}")
    summary_output_audit = last_run_summary.get('summary_output_audit') or {}
    if summary_output_audit.get('available'):
        parts.append(f"output-audit {summary_output_audit.get('text')}")
        if summary_output_audit.get('item_count') is not None:
            parts.append(f"items {summary_output_audit['item_count']}")
        if summary_output_audit.get('source_url_count') is not None:
            parts.append(f"bron-URLs {summary_output_audit['source_url_count']}")
        if summary_output_audit.get('unique_source_url_count') is not None:
            parts.append(f"unieke bron-URLs {summary_output_audit['unique_source_url_count']}")
        if summary_output_audit.get('unique_item_title_count') is not None and summary_output_audit.get('item_count') is not None:
            parts.append(f"unieke titels {summary_output_audit['unique_item_title_count']}/{summary_output_audit['item_count']}")
        duplicate_examples = summary_output_audit.get('duplicate_item_title_examples') or []
        if duplicate_examples:
            parts.append(
                'dubbele titels ' + ', '.join(
                    f"{example.get('title', 'onbekend')} x{example.get('count', 0)}"
                    for example in duplicate_examples[:3]
                )
            )
        if summary_output_audit.get('items_with_multiple_sources_count') is not None and summary_output_audit.get('item_count') is not None:
            parts.append(
                f"items met meerdere bron-URLs {summary_output_audit['items_with_multiple_sources_count']}/{summary_output_audit['item_count']}"
            )
        if summary_output_audit.get('items_with_multi_domain_sources_count') is not None and summary_output_audit.get('item_count') is not None:
            parts.append(
                f"items met multi-domein bronregels {summary_output_audit['items_with_multi_domain_sources_count']}/{summary_output_audit['item_count']}"
            )
        if summary_output_audit.get('first3_items_with_multiple_sources_count') is not None:
            parts.append(f"top3 met meerdere bron-URLs {summary_output_audit['first3_items_with_multiple_sources_count']}/3")
        if summary_output_audit.get('first3_items_with_multi_domain_sources_count') is not None:
            parts.append(
                f"top3 met multi-domein bronregels {summary_output_audit['first3_items_with_multi_domain_sources_count']}/3"
            )
        if summary_output_audit.get('first3_source_domain_count') is not None:
            parts.append(f"top3 brondomeinen {summary_output_audit['first3_source_domain_count']}")
        if summary_output_audit.get('first3_primary_source_domain_count') is not None:
            parts.append(f"top3 primaire brondomeinen {summary_output_audit['first3_primary_source_domain_count']}")
        if summary_output_audit.get('first3_primary_source_family_count') is not None:
            parts.append(f"top3 primaire bronfamilies {summary_output_audit['first3_primary_source_family_count']}")
        if summary_output_audit.get('first3_unique_source_url_count') is not None:
            parts.append(f"top3 unieke bron-URLs {summary_output_audit['first3_unique_source_url_count']}/3")
        if summary_output_audit.get('dated_item_count') is not None and summary_output_audit.get('item_count') is not None:
            parts.append(f"datums {summary_output_audit['dated_item_count']}/{summary_output_audit['item_count']}")
        if summary_output_audit.get('fresh_dated_first3_count') is not None:
            parts.append(
                f"vers top3 {summary_output_audit['fresh_dated_first3_count']}/3 ({summary_output_audit.get('fresh_item_max_age_hours', FRESH_ITEM_MAX_AGE_HOURS)}u)"
            )
        if summary_output_audit.get('recent_dated_first3_count') is not None:
            parts.append(
                f"recent top3 {summary_output_audit['recent_dated_first3_count']}/3 ({summary_output_audit.get('recent_item_max_age_days', RECENT_ITEM_MAX_AGE_DAYS)}d)"
            )
        if summary_output_audit.get('future_dated_item_count') is not None:
            parts.append(f"toekomstige datums {summary_output_audit['future_dated_item_count']}")
        if summary_output_audit.get('first3_evidenced_item_count') is not None:
            parts.append(f"top3 met bron+recente datum {summary_output_audit['first3_evidenced_item_count']}/3")
        if summary_output_audit.get('first3_primary_fresh_item_count') is not None:
            parts.append(
                f"top3 met primaire bron+verse datum {summary_output_audit['first3_primary_fresh_item_count']}/3"
            )
        if summary_output_audit.get('category_theme_count') is not None:
            parts.append(f"categorie-thema's {summary_output_audit['category_theme_count']}/{len(CATEGORY_THEME_KEYWORDS)}")
    if data.get('proof_progress_text') and data.get('runs_total'):
        success_bits = [data['proof_progress_text']]
    elif data.get('runs_total'):
        success_bits = []
    else:
        success_bits = []
    if data.get('runs_total'):
        if data.get('success_rate_pct') is not None:
            success_bits.append(f"succes {data['success_rate_pct']:.1f}%")
        if data.get('delivery_rate_pct') is not None:
            success_bits.append(f"delivery {data['delivery_rate_pct']:.1f}%")
        if data.get('success_streak'):
            success_bits.append(f"streak {data['success_streak']}")
        if data.get('delivery_streak'):
            success_bits.append(f"delivery-streak {data['delivery_streak']}")
        if success_bits:
            parts.append(', '.join(success_bits))
    recent_runs_summary = data.get('recent_runs_summary') or []
    if recent_runs_summary:
        recent_bits = []
        for run in recent_runs_summary[-3:]:
            run_bits = [run.get('status') or 'onbekend']
            if run.get('delivered'):
                run_bits.append('afgeleverd')
            if run.get('run_at_hint'):
                run_bits.append(run['run_at_hint'])
            elif run.get('run_at_text'):
                run_bits.append(run['run_at_text'])
            if run.get('duration_text'):
                run_bits.append(run['duration_text'])
            if run.get('error_text') and run.get('status') != 'ok':
                run_bits.append(run['error_text'])
            recent_bits.append(' / '.join(run_bits))
        parts.append(f"recente runs: {'; '.join(recent_bits)}")
    if last_run_summary.get('error_text') and data.get('attention_text'):
        parts.append(f"laatste fout {last_run_summary['error_text']}")
    return ' | '.join(parts)


def main():
    parser = argparse.ArgumentParser(description='Status van dagelijkse AI-briefing cronjob')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--job-name', default=TARGET_JOB_NAME, help='cronjobnaam')
    parser.add_argument('--summary-file', help='audit alleen briefing-output uit bestand')
    parser.add_argument('--summary-stdin', action='store_true', help='audit alleen briefing-output van stdin')
    args = parser.parse_args()

    if args.summary_file and args.summary_stdin:
        raise SystemExit('kies óf --summary-file óf --summary-stdin')

    if args.summary_file or args.summary_stdin:
        if args.summary_file:
            summary_text = Path(args.summary_file).read_text(encoding='utf-8')
        else:
            summary_text = sys.stdin.read()
        data = audit_summary_output(summary_text)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(render_summary_audit_text(data))
        return

    data = build_status(job_name=args.job_name)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_text(data))


if __name__ == '__main__':
    main()
