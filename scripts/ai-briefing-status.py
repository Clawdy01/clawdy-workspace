#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/home/clawdy/.openclaw')
JOBS_PATH = ROOT / 'cron' / 'jobs.json'
RUNS_DIR = ROOT / 'cron' / 'runs'
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
    'filter marketing zonder echte verandering',
    'Relevant voor Christian',
    "Wat moeten wij hiermee?",
    "Wat ik vandaag het belangrijkst vind",
    'bronnenlijst met URLs',
]
REQUIRED_TOOLS_ALLOW = {'web_search', 'web_fetch'}
REQUIRED_OUTPUT_MARKERS = [
    'Wat moeten wij hiermee?',
    'Wat ik vandaag het belangrijkst vind',
]
REQUIRED_OUTPUT_MARKER_ALTERNATIVES = [
    ('bronnenlijst', 'bronnen'),
]
MIN_SOURCE_URLS = 3


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

    if not next_run_at:
        reasons.append('nextRunAtMs ontbreekt')
    else:
        next_dt = datetime.fromtimestamp(next_run_at / 1000, tz=timezone.utc).astimezone(ZoneInfo(tz_name))
        next_run_local_hour = next_dt.hour
        next_run_local_minute = next_dt.minute
        hours_until_next_run = round((next_run_at - now_ms) / 3600000, 1)
        if expected_hour is not None and next_dt.hour != expected_hour:
            reasons.append(f'next run uur is {next_dt.hour:02d}:{next_dt.minute:02d}')
        if expected_minute is not None and next_dt.minute != expected_minute:
            reasons.append(f'next run minuut is {next_dt.hour:02d}:{next_dt.minute:02d}')
        if hours_until_next_run < -0.1:
            reasons.append(f'next run ligt {abs(hours_until_next_run):.1f} uur in het verleden')
        elif hours_until_next_run > 36:
            reasons.append(f'next run ligt verdacht ver weg ({hours_until_next_run:.1f} uur)')

    text = 'next run slot ok'
    if reasons:
        text = '; '.join(reasons)
    elif next_run_at:
        text = f'next run slot ok ({fmt_ts(next_run_at, tz_name)})'

    return {
        'ok': not reasons,
        'expected_hour': expected_hour,
        'expected_minute': expected_minute,
        'next_run_local_hour': next_run_local_hour,
        'next_run_local_minute': next_run_local_minute,
        'hours_until_next_run': hours_until_next_run,
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


def audit_summary_output(summary_text):
    if not isinstance(summary_text, str) or not summary_text.strip():
        return {
            'available': False,
            'ok': True,
            'missing_markers': [],
            'source_url_count': 0,
            'reasons': [],
            'text': 'geen briefinginhoud om te auditen',
        }

    missing_markers = [marker for marker in REQUIRED_OUTPUT_MARKERS if marker not in summary_text]
    missing_alternative_groups = [
        list(group)
        for group in REQUIRED_OUTPUT_MARKER_ALTERNATIVES
        if not any(marker in summary_text for marker in group)
    ]
    source_url_count = len(re.findall(r'https?://\S+', summary_text))
    reasons = []
    if missing_markers:
        reasons.append(f"{len(missing_markers)} verplichte sectie(s) missen")
    if missing_alternative_groups:
        reasons.append(f"{len(missing_alternative_groups)} verplichte outputanker(s) missen")
    if source_url_count < MIN_SOURCE_URLS:
        reasons.append(f'te weinig bron-URLs ({source_url_count})')

    return {
        'available': True,
        'ok': not reasons,
        'missing_markers': missing_markers,
        'missing_alternative_groups': missing_alternative_groups,
        'source_url_count': source_url_count,
        'reasons': reasons,
        'text': 'briefing-output ok' if not reasons else '; '.join(reasons),
    }


def summarize_run(run, tz_name=DEFAULT_TZ, now_ms=None):
    if not run:
        return None
    usage = run.get('usage') or {}
    summary_text = run.get('summary')
    error_text = summary_text or run.get('error') or run.get('deliveryError')
    if isinstance(error_text, str):
        error_text = ' '.join(error_text.split())[:240]
    summary_preview = None
    summary_preview_lines = []
    summary_length_chars = None
    summary_output_audit = audit_summary_output(summary_text)
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


def load_runs(job_id):
    path = RUNS_DIR / f'{job_id}.jsonl'
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def audit_payload(job):
    payload = job.get('payload') or {}
    message = payload.get('message') or ''
    missing_categories = [marker for marker in REQUIRED_CATEGORY_MARKERS if marker not in message]
    missing_prompt_markers = [marker for marker in REQUIRED_PROMPT_MARKERS if marker not in message]
    tools_allow = set(payload.get('toolsAllow') or [])
    missing_tools = sorted(REQUIRED_TOOLS_ALLOW - tools_allow)
    timeout_seconds = int(payload.get('timeoutSeconds') or 0)
    message_sha256 = hashlib.sha256(message.encode('utf-8')).hexdigest() if message else None
    light_context = bool(payload.get('lightContext'))

    reasons = []
    if missing_categories:
        reasons.append(f"{len(missing_categories)} briefingcategorie(ën) missen")
    if missing_prompt_markers:
        reasons.append(f"{len(missing_prompt_markers)} promptanker(s) missen")
    if missing_tools:
        reasons.append(f"toolsAllow mist {', '.join(missing_tools)}")
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
        'missing_tools_allow': missing_tools,
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
    run_file_exists = (RUNS_DIR / f"{job['id']}.jsonl").exists()
    runs = load_runs(job['id'])
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
    uniqueness_audit = audit_uniqueness(jobs, job)

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
    if not uniqueness_audit.get('ok'):
        attention_reasons.append(f"uniqueness: {uniqueness_audit.get('text')}")
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
        'uniqueness_audit': uniqueness_audit,
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
        elif len(finished_runs) < 3:
            readiness_phase = 'proving'
            readiness_text = f'bewijs verzamelen ({len(finished_runs)}/3 runs)'
        else:
            readiness_phase = 'proved'
            readiness_text = f'runbewijs aanwezig ({len(finished_runs)} runs)'
    elif finished_runs:
        readiness_text = f'runbewijs met aandachtspunt ({len(finished_runs)} runs)'

    summary['text'] = status_text
    summary['readiness_phase'] = readiness_phase
    summary['readiness_text'] = readiness_text
    return summary


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
        uniqueness_audit = data.get('uniqueness_audit') or {}
        if uniqueness_audit.get('text'):
            parts.append(uniqueness_audit.get('text'))
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
    summary_output_audit = last_run_summary.get('summary_output_audit') or {}
    if summary_output_audit.get('available'):
        parts.append(f"output-audit {summary_output_audit.get('text')}")
        if summary_output_audit.get('source_url_count') is not None:
            parts.append(f"bron-URLs {summary_output_audit['source_url_count']}")
    if data.get('runs_total'):
        success_bits = []
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
    args = parser.parse_args()

    data = build_status(job_name=args.job_name)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_text(data))


if __name__ == '__main__':
    main()
