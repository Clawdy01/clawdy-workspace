#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')


def run_status():
    try:
        proc = subprocess.run(
            ['openclaw', 'status', '--json'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit('openclaw status timed out')
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'openclaw status failed: {proc.returncode}')
    return json.loads(proc.stdout)


def age_text(ms):
    if ms is None:
        return 'onbekend'
    seconds = int(ms / 1000)
    if seconds < 60:
        return f'{seconds}s geleden'
    minutes = seconds // 60
    if minutes < 60:
        return f'{minutes}m geleden'
    hours = minutes // 60
    if hours < 48:
        return f'{hours}u geleden'
    days = hours // 24
    return f'{days}d geleden'


def channel_state(data, name):
    for line in data.get('channelSummary') or []:
        if line.lower().startswith(name.lower() + ':'):
            return line.split(':', 1)[1].strip()
    return 'onbekend'


def summarize(data):
    gateway = data.get('gateway') or {}
    tasks = data.get('tasks') or {}
    audit = data.get('taskAudit') or {}
    sessions = (data.get('sessions') or {}).get('recent') or []
    active_session = sessions[0] if sessions else {}
    heartbeat_agents = (data.get('heartbeat') or {}).get('agents') or []
    heartbeat = heartbeat_agents[0] if heartbeat_agents else {}
    by_status = tasks.get('byStatus') or {}
    by_runtime = tasks.get('byRuntime') or {}
    by_code = audit.get('byCode') or {}

    gateway_ok = bool(gateway.get('reachable')) and not gateway.get('misconfigured')
    gateway_bits = ['ok' if gateway_ok else 'probleem']
    if gateway.get('connectLatencyMs') is not None:
        gateway_bits.append(f"{gateway['connectLatencyMs']}ms")
    if gateway.get('url'):
        gateway_bits.append(gateway['url'])

    session_bits = None
    if active_session:
        flags = active_session.get('flags') or []
        reasoning_on = any(flag == 'reasoning:on' for flag in flags) or active_session.get('reasoningLevel') == 'on'
        session_bits = {
            'key': active_session.get('key', 'onbekend'),
            'age': age_text(active_session.get('age')),
            'model': active_session.get('model', 'onbekend'),
            'reasoning': 'aan' if reasoning_on else 'uit',
            'percent_used': active_session.get('percentUsed'),
        }

    summary = {
        'version': data.get('runtimeVersion', 'onbekend'),
        'gateway': {
            'ok': gateway_ok,
            'text': ', '.join(gateway_bits),
            'latency_ms': gateway.get('connectLatencyMs'),
            'url': gateway.get('url'),
        },
        'telegram': channel_state(data, 'Telegram'),
        'heartbeat': heartbeat.get('every', 'onbekend'),
        'tasks': {
            'active': tasks.get('active', 0),
            'failures': tasks.get('failures', 0),
            'lost': by_status.get('lost', 0),
            'cron': by_runtime.get('cron', 0),
            'cli': by_runtime.get('cli', 0),
        },
        'audit': {
            'errors': audit.get('errors', 0),
            'warnings': audit.get('warnings', 0),
            'lost': by_code.get('lost', 0),
            'timestamp_warns': by_code.get('inconsistent_timestamps', 0),
        },
        'session': session_bits,
    }
    return summary


def render_text(summary):
    lines = []
    lines.append('OpenClaw status')
    lines.append(f"- versie: {summary['version']}")
    lines.append(f"- gateway: {summary['gateway']['text']}")
    lines.append(f"- telegram: {summary['telegram']}")
    lines.append(f"- heartbeat: {summary['heartbeat']}")
    lines.append(
        f"- taken: {summary['tasks']['active']} actief, {summary['tasks']['failures']} failures, {summary['tasks']['lost']} lost, cron {summary['tasks']['cron']}"
    )
    lines.append(
        f"- audit: {summary['audit']['errors']} errors, {summary['audit']['warnings']} warns, timestamp {summary['audit']['timestamp_warns']}"
    )
    if summary['session']:
        session = summary['session']
        used = f", {session['percent_used']}% context" if session['percent_used'] is not None else ''
        lines.append(
            f"- sessie: {session['key']} ({session['age']}, model {session['model']}, reasoning {session['reasoning']}{used})"
        )
    if summary['audit']['lost']:
        lines.append(f"- let op: {summary['audit']['lost']} lost task")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte OpenClaw statussamenvatting')
    parser.add_argument('--json', action='store_true', help='geef compacte JSON-output')
    args = parser.parse_args()

    summary = summarize(run_status())
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
