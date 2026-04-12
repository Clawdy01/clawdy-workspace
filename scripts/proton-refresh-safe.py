#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
BROWSER = ROOT / 'browser-automation'

SAFE_STEPS = [
    ['node', str(BROWSER / 'proton_probe_status.js')],
    ['node', str(BROWSER / 'proton_probe_input_proxy.js')],
    ['node', str(BROWSER / 'proton_to_password_step.js')],
    ['node', str(BROWSER / 'proton_probe_password_validation.js')],
    ['node', str(BROWSER / 'proton_to_submit_ready.js')],
]
STEP_TIMEOUT_SECONDS = 75
SUMMARY_TIMEOUT_SECONDS = 20


def run_capture(cmd):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False, timeout=STEP_TIMEOUT_SECONDS)
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = exc
        timed_out = True
    if timed_out:
        return {
            'command': cmd,
            'ok': False,
            'returncode': 124,
            'stdout': (proc.stdout or '').strip() if getattr(proc, 'stdout', None) else '',
            'stderr': ((proc.stderr or '').strip() + ('\n' if getattr(proc, 'stderr', None) else '') + f'timeout after {STEP_TIMEOUT_SECONDS}s').strip(),
        }
    return {
        'command': cmd,
        'ok': proc.returncode == 0,
        'returncode': proc.returncode,
        'stdout': (proc.stdout or '').strip(),
        'stderr': (proc.stderr or '').strip(),
    }


def run_summary(json_mode=False):
    cmd = ['python3', str(ROOT / 'scripts' / 'proton-status-summary.py')]
    if json_mode:
        cmd.append('--json')
    try:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False, timeout=SUMMARY_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        return {
            'ok': False,
            'returncode': 124,
            'stdout': exc.stdout or '',
            'stderr': ((exc.stderr or '') + ('\n' if exc.stderr else '') + f'timeout after {SUMMARY_TIMEOUT_SECONDS}s'),
            'parsed': None,
        }
    parsed = None
    if json_mode and (proc.stdout or '').strip():
        try:
            parsed = json.loads(proc.stdout)
        except Exception:
            parsed = None
    return {
        'ok': proc.returncode == 0,
        'returncode': proc.returncode,
        'stdout': proc.stdout or '',
        'stderr': proc.stderr or '',
        'parsed': parsed,
    }


def render_text(payload):
    lines = ['Proton refresh safe']
    lines.append(f"- stappen: {payload.get('success_count', 0)} ok, {payload.get('failure_count', 0)} mislukt")
    first_failure = next((step for step in (payload.get('steps') or []) if not step.get('ok')), None)
    if first_failure:
        lines.append(f"- eerste failure: {' '.join(first_failure.get('command') or [])}")
        if first_failure.get('stderr'):
            lines.append(f"- stderr: {first_failure.get('stderr')[:220]}")
    summary = payload.get('summary') or {}
    parsed = summary.get('parsed') or {}
    if parsed:
        start = parsed.get('start') or {}
        route = parsed.get('route') or {}
        submit_ready = parsed.get('submit_ready') or {}
        lines.append(
            f"- status: signup={start.get('signup_visible')}, password-step={route.get('reached_password_step')}, submit-ready={submit_ready.get('submit_ready')}"
        )
    elif summary.get('stdout'):
        lines.append(summary.get('stdout').strip())
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Draai veilige Proton probes opnieuw en toon daarna de status')
    parser.add_argument('--json', action='store_true', help='toon machine-leesbare JSON in plaats van compacte tekst')
    args = parser.parse_args()

    steps = [run_capture(cmd) for cmd in SAFE_STEPS]
    summary = run_summary(json_mode=True)
    payload = {
        'ok': all(step.get('ok') for step in steps) and summary.get('ok'),
        'success_count': sum(1 for step in steps if step.get('ok')),
        'failure_count': sum(1 for step in steps if not step.get('ok')),
        'steps': steps,
        'summary': summary,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload))

    raise SystemExit(0 if payload.get('ok') else 1)


if __name__ == '__main__':
    main()
