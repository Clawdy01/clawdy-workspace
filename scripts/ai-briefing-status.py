#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/home/clawdy/.openclaw')
JOBS_PATH = ROOT / 'cron' / 'jobs.json'
RUNS_DIR = ROOT / 'cron' / 'runs'
DEFAULT_TZ = 'Europe/Amsterdam'
TARGET_JOB_NAME = 'daily-ai-update'


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
    runs = load_runs(job['id'])
    finished_runs = [run for run in runs if run.get('action') == 'finished']
    delivered_runs = [run for run in finished_runs if run.get('delivered')]
    successful_runs = [run for run in finished_runs if run.get('status') == 'ok']
    last_run = finished_runs[-1] if finished_runs else None
    last_delivered = delivered_runs[-1] if delivered_runs else None
    last_success = successful_runs[-1] if successful_runs else None
    next_run_at = state.get('nextRunAtMs')
    last_run_at = (last_run or {}).get('runAtMs') or state.get('lastRunAtMs')

    summary = {
        'ok': True,
        'found': True,
        'job_id': job.get('id'),
        'job_name': job.get('name'),
        'enabled': bool(job.get('enabled')),
        'delivery_channel': delivery.get('channel'),
        'delivery_to': delivery.get('to'),
        'schedule': schedule,
        'state': state,
        'run_file_exists': (RUNS_DIR / f"{job['id']}.jsonl").exists(),
        'runs_total': len(finished_runs),
        'runs_ok': len(successful_runs),
        'runs_delivered': len(delivered_runs),
        'has_run_proof': bool(finished_runs),
        'last_run': last_run,
        'last_success': last_success,
        'last_delivered': last_delivered,
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
        if last_run_at:
            status_text += f", laatste {summary['last_run_hint']}"
    else:
        status_text = f"nog geen runbewijs, volgende run {summary['next_run_hint']}"
    summary['text'] = status_text
    return summary


def render_text(data):
    if not data.get('found'):
        return data.get('text', 'AI-briefingstatus onbekend')
    parts = [f"AI-briefing: {'aan' if data.get('enabled') else 'uit'}"]
    parts.append(data.get('text', 'onbekend'))
    if data.get('next_run_at_text'):
        parts.append(f"volgende {data['next_run_at_text']}")
    if data.get('last_run_at_text'):
        parts.append(f"laatste {data['last_run_at_text']}")
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
