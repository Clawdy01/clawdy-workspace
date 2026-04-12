#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
EWS_TOOL = ROOT / 'scripts' / 'exchange-ews-tool.py'
MAILBOX = ROOT / 'scripts' / 'exchange-mailbox.py'
CHECK = ROOT / 'scripts' / 'exchange-ews-check.py'


def run_json(cmd):
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=120)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or 'command failed')
    return json.loads(proc.stdout)


def is_parked_task(task):
    subject = str(task.get('subject') or '').lower()
    body = str(task.get('body') or '').lower()
    return (
        'geparkeerd' in body
        or 'parked' in body
        or 'herstarten zodra' in subject
    )


def sort_tasks(tasks):
    def key(task):
        due = task.get('due_date') or '9999-99-99T99:99:99Z'
        parked = is_parked_task(task)
        return (parked, due, str(task.get('subject') or '').lower())
    return sorted(tasks, key=key)


def build_summary(hours: int, inbox_limit: int, task_limit: int):
    check = run_json(['python3', str(CHECK), '--json'])
    unread = run_json(['python3', str(MAILBOX), '--json', '--unread', '--limit', str(inbox_limit)])
    calendar = run_json(['python3', str(EWS_TOOL), '--json', '--calendar', '--hours', str(hours)])
    tasks = run_json(['python3', str(EWS_TOOL), '--json', '--tasks', '--limit', str(task_limit)])

    unread_items = unread.get('inbox') or []
    calendar_items = calendar.get('calendar') or []
    task_items = tasks.get('tasks') or []
    open_tasks = sort_tasks([t for t in task_items if (t.get('status') or '').lower() != 'completed'])
    active_open_tasks = [t for t in open_tasks if not is_parked_task(t)]
    parked_open_tasks = [t for t in open_tasks if is_parked_task(t)]

    next_action = None
    if unread_items:
        first = unread_items[0]
        sender = first.get('from_name') or first.get('from_email') or 'onbekend'
        next_action = f"review unread mail van {sender}: {first.get('subject') or '(geen onderwerp)'}"
    elif active_open_tasks:
        first = active_open_tasks[0]
        next_action = f"werk actieve taak bij: {first.get('subject') or '(geen onderwerp)'}"
    elif calendar_items:
        first = calendar_items[0]
        next_action = f"check eerstvolgende afspraak: {first.get('subject') or '(geen onderwerp)'}"

    return {
        'check': {
            'autodiscover_ok': check.get('autodiscover_ok'),
            'ews_ok': check.get('ews_ok'),
            'host': check.get('host'),
            'smtp': check.get('smtp'),
            'inbox_unread_count': check.get('inbox_unread_count'),
        },
        'unread': {
            'count': len(unread_items),
            'items': unread_items,
        },
        'calendar': {
            'hours': hours,
            'count': len(calendar_items),
            'items': calendar_items,
        },
        'tasks': {
            'count': len(task_items),
            'open_count': len(open_tasks),
            'active_open_count': len(active_open_tasks),
            'parked_open_count': len(parked_open_tasks),
            'items': task_items,
            'open_items': open_tasks,
            'active_open_items': active_open_tasks,
            'parked_open_items': parked_open_tasks,
        },
        'next_action': next_action,
    }


def render_text(summary):
    lines = ['Exchange summary']
    chk = summary['check']
    lines.append(f"- route: autodiscover={'ok' if chk['autodiscover_ok'] else 'fout'}, ews={'ok' if chk['ews_ok'] else 'fout'}")
    if chk.get('inbox_unread_count') is not None:
        lines.append(f"- inbox unread (server): {chk['inbox_unread_count']}")

    unread = summary['unread']
    lines.append(f"- unread nu: {unread['count']}")
    if unread['items']:
        item = unread['items'][0]
        sender = item.get('from_name') or item.get('from_email') or 'onbekend'
        lines.append(f"- eerstvolgende unread: {sender} — {item.get('subject') or '(geen onderwerp)'}")

    cal = summary['calendar']
    lines.append(f"- agenda komende {cal['hours']} uur: {cal['count']}")
    if cal['items']:
        item = cal['items'][0]
        lines.append(f"- eerstvolgende afspraak: {item.get('start') or '?'} — {item.get('subject') or '(geen onderwerp)'}")

    tasks = summary['tasks']
    lines.append(f"- taken: {tasks['count']} totaal, {tasks['open_count']} open ({tasks['active_open_count']} actief, {tasks['parked_open_count']} geparkeerd)")
    if tasks['active_open_items']:
        item = tasks['active_open_items'][0]
        due = f" due {item.get('due_date')}" if item.get('due_date') else ''
        lines.append(f"- eerstvolgende actieve taak: {item.get('subject') or '(geen onderwerp)'} [{item.get('status') or 'unknown'}]{due}")
    elif tasks['parked_open_items']:
        item = tasks['parked_open_items'][0]
        due = f" due {item.get('due_date')}" if item.get('due_date') else ''
        lines.append(f"- eerstvolgende geparkeerde taak: {item.get('subject') or '(geen onderwerp)'} [{item.get('status') or 'unknown'}]{due}")
    if summary.get('next_action'):
        lines.append(f"- next action: {summary['next_action']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte Exchange SE mailbox/agenda/taken samenvatting')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--hours', type=int, default=72)
    parser.add_argument('--inbox-limit', type=int, default=5)
    parser.add_argument('--task-limit', type=int, default=20)
    args = parser.parse_args()

    summary = build_summary(
        hours=max(1, min(args.hours, 24 * 14)),
        inbox_limit=max(1, min(args.inbox_limit, 20)),
        task_limit=max(1, min(args.task_limit, 100)),
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
