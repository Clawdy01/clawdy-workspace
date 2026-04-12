#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
NEXT_STEP = ROOT / 'scripts' / 'proton-next-step.py'

SAFE_ROUTES = {
    'proton-refresh',
    'proton-password-step',
    'investigate-password-regression',
    'proton-submit-ready',
    'proton-verify-refresh',
    'proton-request-code',
    'proton-use-code',
    'continue-password-setup',
}
BLOCKED_ROUTES = {
    'manual-submit-decision',
    'wait-for-mail',
    'investigate-blocker',
    'noop',
    'unknown',
}


def run_json(cmd, timeout=30, default=None):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def run_capture(cmd, timeout=180):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = exc
        timed_out = True
    if timed_out:
        return {
            'command': cmd,
            'returncode': 124,
            'stdout': (getattr(proc, 'stdout', '') or '').strip(),
            'stderr': ((getattr(proc, 'stderr', '') or '').strip() + f'\ntimeout after {timeout}s').strip(),
        }
    return {
        'command': cmd,
        'returncode': proc.returncode,
        'stdout': (proc.stdout or '').strip(),
        'stderr': (proc.stderr or '').strip(),
    }


def next_step():
    return run_json(['python3', str(NEXT_STEP), '--json'], default={}) or {}


def build_command(route, current=None):
    current = current or {}
    recommended_command = (current.get('recommended_command') or '').strip()
    if route == 'proton-refresh':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-refresh', '--json']
    if route == 'proton-password-step':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-password-step']
    if route == 'investigate-password-regression':
        command = ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'investigate-password-regression']
        if '--refresh' in recommended_command:
            command.append('--refresh')
        command.append('--json')
        return command
    if route == 'proton-submit-ready':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-submit-ready']
    if route == 'proton-verify-refresh':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-verify', '--refresh', '--json']
    if route == 'proton-request-code':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-request-code', '--json']
    if route == 'proton-use-code':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-use-code', '--json']
    if route == 'continue-password-setup':
        return ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'continue-password-setup', '--json']
    return None


def summarize(before, after, actions):
    return {
        'before_route': before.get('recommended_route'),
        'before_reason': before.get('reason'),
        'before_command': before.get('recommended_command'),
        'after_route': after.get('recommended_route'),
        'after_reason': after.get('reason'),
        'after_command': after.get('recommended_command'),
        'actions': actions,
        'advanced': bool(actions),
        'blocked': after.get('recommended_route') in BLOCKED_ROUTES,
    }


def render_text(summary):
    lines = ['Proton safe autopilot']
    lines.append(f"- before={summary.get('before_route')} ({summary.get('before_reason')})")
    if summary.get('actions'):
        for item in summary['actions']:
            lines.append(
                f"- ran={item.get('route')} rc={item.get('returncode')} cmd={' '.join(item.get('command') or [])}"
            )
    else:
        lines.append('- ran=niets')
    lines.append(f"- after={summary.get('after_route')} ({summary.get('after_reason')})")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Voer veilig exact één of meer Proton automation vervolgstappen uit op basis van proton-next-step')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--max-steps', type=int, default=1)
    args = parser.parse_args()

    before = next_step()
    current = before
    actions = []

    for _ in range(max(1, args.max_steps)):
        route = current.get('recommended_route') or 'unknown'
        if route not in SAFE_ROUTES:
            break
        cmd = build_command(route, current=current)
        if not cmd:
            break
        timeout = 300 if route == 'continue-password-setup' else 180
        result = run_capture(cmd, timeout=timeout)
        result['route'] = route
        actions.append(result)
        if result.get('returncode') != 0:
            break
        current = next_step()

    after = current if actions and actions[-1].get('returncode') != 0 else next_step()
    summary = summarize(before, after, actions)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))
    raise SystemExit(0 if all(item.get('returncode') == 0 for item in actions) else 1)


if __name__ == '__main__':
    main()
