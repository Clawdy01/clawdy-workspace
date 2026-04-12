#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timedelta, UTC
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


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return None


def is_notification_mail(item):
    subject = str(item.get('subject') or '').lower()
    sender_name = str(item.get('from_name') or '').lower()
    sender_email = str(item.get('from_email') or '').lower()
    preview = str(item.get('preview') or '').lower()
    haystack = ' '.join([subject, sender_name, sender_email, preview])
    markers = [
        'github', 'gitlab', 'notification', 'noreply', 'no-reply', 'do-not-reply',
        'mailer-daemon', 'automated', 'automatisch', 'alert', 'digest', 'newsletter',
    ]
    return any(marker in haystack for marker in markers)


def sort_tasks(tasks):
    def key(task):
        due_dt = parse_dt(task.get('due_date'))
        due_key = due_dt.isoformat() if due_dt else '9999-99-99T99:99:99+00:00'
        parked = is_parked_task(task)
        return (parked, due_key, str(task.get('subject') or '').lower())
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
    actionable_unread_items = [item for item in unread_items if not is_notification_mail(item)]
    notification_unread_items = [item for item in unread_items if is_notification_mail(item)]

    now = datetime.now(UTC)
    next_24h = now + timedelta(hours=24)
    upcoming_soon_items = [
        item for item in calendar_items
        if (start := parse_dt(item.get('start'))) is not None and start <= next_24h
    ]
    overdue_active_tasks = [
        item for item in active_open_tasks
        if (due := parse_dt(item.get('due_date'))) is not None and due < now
    ]

    next_action = None
    if upcoming_soon_items:
        first = sorted(upcoming_soon_items, key=lambda item: parse_dt(item.get('start')) or next_24h)[0]
        next_action = f"check eerstvolgende afspraak binnen 24 uur: {first.get('subject') or '(geen onderwerp)'}"
    elif actionable_unread_items:
        first = actionable_unread_items[0]
        sender = first.get('from_name') or first.get('from_email') or 'onbekend'
        next_action = f"review unread mail van {sender}: {first.get('subject') or '(geen onderwerp)'}"
    elif overdue_active_tasks:
        first = overdue_active_tasks[0]
        next_action = f"werk overdue taak bij: {first.get('subject') or '(geen onderwerp)'}"
    elif active_open_tasks:
        first = active_open_tasks[0]
        next_action = f"werk actieve taak bij: {first.get('subject') or '(geen onderwerp)'}"
    elif notification_unread_items:
        first = notification_unread_items[0]
        sender = first.get('from_name') or first.get('from_email') or 'onbekend'
        next_action = f"scan notificatie-mail van {sender}: {first.get('subject') or '(geen onderwerp)'}"
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
            'actionable_count': len(actionable_unread_items),
            'notification_count': len(notification_unread_items),
            'items': unread_items,
            'actionable_items': actionable_unread_items,
            'notification_items': notification_unread_items,
        },
        'calendar': {
            'hours': hours,
            'count': len(calendar_items),
            'soon_count': len(upcoming_soon_items),
            'items': calendar_items,
            'soon_items': sorted(upcoming_soon_items, key=lambda item: parse_dt(item.get('start')) or next_24h),
        },
        'tasks': {
            'count': len(task_items),
            'open_count': len(open_tasks),
            'active_open_count': len(active_open_tasks),
            'parked_open_count': len(parked_open_tasks),
            'overdue_active_count': len(overdue_active_tasks),
            'items': task_items,
            'open_items': open_tasks,
            'active_open_items': active_open_tasks,
            'parked_open_items': parked_open_tasks,
            'overdue_active_items': overdue_active_tasks,
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
    lines.append(f"- unread nu: {unread['count']} ({unread['actionable_count']} actiegericht, {unread['notification_count']} notificatie)")
    if unread['actionable_items']:
        item = unread['actionable_items'][0]
        sender = item.get('from_name') or item.get('from_email') or 'onbekend'
        lines.append(f"- eerstvolgende actiegerichte unread: {sender} — {item.get('subject') or '(geen onderwerp)'}")
    elif unread['notification_items']:
        item = unread['notification_items'][0]
        sender = item.get('from_name') or item.get('from_email') or 'onbekend'
        lines.append(f"- eerstvolgende notificatie-unread: {sender} — {item.get('subject') or '(geen onderwerp)'}")

    cal = summary['calendar']
    lines.append(f"- agenda komende {cal['hours']} uur: {cal['count']} ({cal['soon_count']} binnen 24 uur)")
    if cal['items']:
        item = cal['items'][0]
        lines.append(f"- eerstvolgende afspraak: {item.get('start') or '?'} — {item.get('subject') or '(geen onderwerp)'}")

    tasks = summary['tasks']
    lines.append(f"- taken: {tasks['count']} totaal, {tasks['open_count']} open ({tasks['active_open_count']} actief, {tasks['parked_open_count']} geparkeerd, {tasks['overdue_active_count']} overdue)")
    if tasks['overdue_active_items']:
        item = tasks['overdue_active_items'][0]
        due = f" due {item.get('due_date')}" if item.get('due_date') else ''
        lines.append(f"- eerstvolgende overdue taak: {item.get('subject') or '(geen onderwerp)'} [{item.get('status') or 'unknown'}]{due}")
    elif tasks['active_open_items']:
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
