#!/usr/bin/env python3
import argparse
import hashlib
import json
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
    "Wat moeten wij hiermee?",
    "Wat ik vandaag het belangrijkst vind",
    'Relevant voor Christian',
]
REQUIRED_TOOLS_ALLOW = {'web_search', 'web_fetch'}


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
    hours = minutes // 60
    if hours < 48:
        return f'over {hours} uur'
    days = hours // 24
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


def summarize_run(run):
    if not run:
        return None
    usage = run.get('usage') or {}
    return {
        'status': run.get('status'),
        'delivered': bool(run.get('delivered')),
        'delivery_status': run.get('deliveryStatus'),
        'run_at': run.get('runAtMs'),
        'duration_ms': run.get('durationMs'),
        'duration_text': duration_hint(run.get('durationMs')),
        'model': run.get('model'),
        'provider': run.get('provider'),
        'usage': usage,
        'total_tokens': usage.get('total_tokens'),
        'input_tokens': usage.get('input_tokens'),
        'output_tokens': usage.get('output_tokens'),
    }


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

    return {
        'ok': not reasons,
        'schedule_kind': schedule.get('kind'),
        'schedule_expr': schedule_expr,
        'schedule_tz': schedule_tz,
        'delivery_channel': delivery_channel,
        'delivery_to': delivery_to,
        'delivery_mode': delivery_mode,
        'reasons': reasons,
        'text': 'schedule/delivery ok' if not reasons else '; '.join(reasons),
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
    last_run_summary = summarize_run(last_run)
    last_success_summary = summarize_run(last_success)
    last_delivered_summary = summarize_run(last_delivered)
    next_run_at = state.get('nextRunAtMs')
    last_run_at = (last_run or {}).get('runAtMs') or state.get('lastRunAtMs')
    created_at = job.get('createdAtMs')
    updated_at = job.get('updatedAtMs') or created_at
    first_run_pending = bool(not finished_runs and created_at and next_run_at and created_at < next_run_at)
    last_run_status = state.get('lastRunStatus') or state.get('lastStatus')
    last_delivery_status = state.get('lastDeliveryStatus')
    consecutive_errors = int(state.get('consecutiveErrors') or 0)

    delivery_channel = delivery.get('channel') or 'onbekend'
    delivery_to = delivery.get('to') or 'onbekend'
    proof_text = 'runlog aanwezig' if run_file_exists else 'runlog nog niet aangemaakt'
    payload_audit = audit_payload(job)
    runtime_audit = audit_runtime(job, tz_name)

    overdue_grace_ms = 15 * 60 * 1000
    overdue = bool(next_run_at and now_ms > (next_run_at + overdue_grace_ms))
    overdue_by_ms = max(0, now_ms - next_run_at) if overdue and next_run_at else 0
    overdue_hint = age_hint(now_ms - overdue_by_ms, now_ms) if overdue_by_ms else None

    attention_reasons = []
    if not job.get('enabled'):
        attention_reasons.append('job staat uit')
    if overdue:
        attention_reasons.append(f'volgende run is over tijd ({overdue_hint})')
    if consecutive_errors:
        attention_reasons.append(f'{consecutive_errors} opeenvolgende cronfout(en)')
    if last_run_status and last_run_status != 'ok':
        attention_reasons.append(f'laatste runstatus {last_run_status}')
    if finished_runs and delivery.get('mode') not in (None, 'none') and last_delivery_status not in (None, 'delivered', 'not-requested'):
        attention_reasons.append(f'laatste delivery-status {last_delivery_status}')
    if not payload_audit.get('ok'):
        attention_reasons.append(f"prompt/config: {payload_audit.get('text')}")
    if not runtime_audit.get('ok'):
        attention_reasons.append(f"schedule/delivery: {runtime_audit.get('text')}")

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
        'has_run_proof': bool(finished_runs),
        'first_run_pending': first_run_pending,
        'last_run': last_run,
        'last_success': last_success,
        'last_delivered': last_delivered,
        'last_run_summary': last_run_summary,
        'last_success_summary': last_success_summary,
        'last_delivered_summary': last_delivered_summary,
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
        'last_run_at': last_run_at,
        'last_run_at_text': fmt_ts(last_run_at, tz_name),
        'last_run_hint': age_hint(last_run_at, now_ms),
    }

    if finished_runs:
        status_text = f"{len(successful_runs)}/{len(finished_runs)} runs ok"
        if delivered_runs:
            status_text += f", {len(delivered_runs)} afgeleverd"
        if last_run_summary and last_run_summary.get('duration_text'):
            status_text += f", laatste duur {last_run_summary['duration_text']}"
        if last_run_at:
            status_text += f", laatste {summary['last_run_hint']}"
    elif first_run_pending:
        status_text = f"eerste run nog niet geweest, eerste run {summary['next_run_hint']}"
    else:
        status_text = f"nog geen runbewijs, volgende run {summary['next_run_hint']}"
    summary['text'] = status_text
    return summary


def render_text(data):
    if not data.get('found'):
        return data.get('text', 'AI-briefingstatus onbekend')
    parts = [f"AI-briefing: {'aan' if data.get('enabled') else 'uit'}"]
    parts.append(data.get('text', 'onbekend'))
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
        if payload_audit.get('text'):
            parts.append(payload_audit.get('text'))
    if data.get('updated_at_hint'):
        fingerprint = payload_audit.get('message_sha256_short')
        if fingerprint:
            parts.append(f"config {data['updated_at_hint']} gewijzigd, hash {fingerprint}")
        else:
            parts.append(f"config {data['updated_at_hint']} gewijzigd")
    if data.get('next_run_at_text'):
        parts.append(f"volgende {data['next_run_at_text']}")
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
