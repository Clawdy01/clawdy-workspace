#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from mail_heuristics import suggest_action

ROOT = Path('/home/clawdy/.openclaw/workspace')
CHECK = ROOT / 'scripts' / 'check_mail.py'


def run_check_mail():
    proc = subprocess.run(
        ['python3', str(CHECK)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or '').strip()
    err = (proc.stderr or '').strip()
    if proc.returncode == 0 and out == 'NO_NEW_MAIL':
        return {'new_count': 0, 'messages': []}
    if proc.returncode != 0:
        raise SystemExit(err or out or f'check_mail failed: {proc.returncode}')
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise SystemExit(f'Invalid JSON from check_mail: {e}\n{out}')


def summarize_messages(result):
    messages = result.get('messages') or []
    for msg in messages:
        msg['action_hint'] = suggest_action(msg)
    return {
        'new_count': result.get('new_count', len(messages)),
        'high_count': sum(1 for m in messages if m.get('urgency') == 'high'),
        'messages': messages,
    }


def fmt_message(msg, show_preview=False):
    urgency = msg.get('urgency', 'normal')
    prefix = '‼️' if urgency == 'high' else '•'
    sender = msg.get('sender_display') or msg.get('from') or 'onbekend'
    subject = msg.get('subject') or '(geen onderwerp)'
    action = msg.get('action_hint') or 'ter info'
    line = f"{prefix} {sender}: {subject} [{action}]"
    preview = (msg.get('preview') or '').strip()
    if show_preview and preview:
        line += f" — {preview[:140]}"
    return line


def render_text(summary, show_preview=False):
    messages = summary['messages']
    if not messages:
        return 'NO_NEW_MAIL'

    lines = [f"Nieuwe mail: {summary['new_count']} (hoog: {summary['high_count']})"]
    for msg in messages[:10]:
        lines.append(fmt_message(msg, show_preview=show_preview))
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte samenvatting van nieuwe mail met urgentie en actiehints')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--preview', action='store_true', help='toon ook korte preview per mail in tekstoutput')
    args = parser.parse_args()

    summary = summarize_messages(run_check_mail())
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary, show_preview=args.preview))


if __name__ == '__main__':
    main()
