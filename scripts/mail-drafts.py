#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

from mail_draft_helpers import draft_for_message
from mail_heuristics import reply_needed

ROOT = Path('/home/clawdy/.openclaw/workspace')
MAIL_SUMMARY = ROOT / 'scripts' / 'mail-summary.py'
MAIL_TRIAGE = ROOT / 'scripts' / 'mail-triage.py'


def load_json_blob(from_stdin=False, input_path=None, default=None):
    default = default or {}
    if input_path:
        data = Path(input_path).read_text().strip()
        return json.loads(data) if data else default

    if from_stdin:
        data = sys.stdin.read().strip()
        return json.loads(data) if data else default

    return None


def run_json(command, error_label):
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'{error_label} failed: {proc.returncode}')
    data = proc.stdout.strip()
    if not data:
        raise SystemExit(f'invalid json from {error_label}: empty stdout')
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'invalid json from {error_label}: {exc}')


def load_messages(source='summary', from_stdin=False, input_path=None, limit=10):
    if source == 'summary':
        payload = load_json_blob(
            from_stdin=from_stdin,
            input_path=input_path,
            default={'new_count': 0, 'high_count': 0, 'messages': []},
        )
        if payload is not None:
            payload.setdefault('messages', [])
            payload.setdefault('new_count', len(payload['messages']))
            payload.setdefault('high_count', 0)
            payload['scope'] = payload.get('scope', 'new')
            return payload
        payload = run_json(['python3', str(MAIL_SUMMARY), '--json'], 'mail-summary')
        payload['scope'] = payload.get('scope', 'new')
        return payload

    cmd = ['python3', str(MAIL_TRIAGE), '--json', '-n', str(max(1, min(limit, 20)))]
    if source == 'latest':
        cmd.append('--all')
    payload = run_json(cmd, 'mail-triage')
    payload['messages'] = payload.pop('items', [])
    payload['new_count'] = payload.get('count', len(payload['messages']))
    return payload


def build_drafts(payload):
    messages = payload.get('messages') or []
    drafts = []
    for msg in messages:
        if msg.get('action_hint') == 'ter info' and not reply_needed(msg):
            continue
        draft = draft_for_message(msg)
        if draft:
            drafts.append(draft)
    return {
        'scope': payload.get('scope', 'new'),
        'new_count': payload.get('new_count', len(messages)),
        'high_count': payload.get('high_count', sum(1 for msg in messages if msg.get('urgency') == 'high')),
        'draft_count': len(drafts),
        'drafts': drafts,
    }


def render_text(result):
    if result['new_count'] == 0:
        return 'NO_NEW_MAIL'
    if not result['drafts']:
        return f"Geen duidelijke draft nodig in scope {result.get('scope', 'mail')}."

    lines = [f"Draftsuggesties ({result.get('scope', 'mail')}): {result['draft_count']}"]
    for item in result['drafts'][:5]:
        lines.append(f"• {item['sender']}: {item['subject']}")
        lines.append(f"  {item['draft']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Maak simpele concept-antwoorden op basis van nieuwe, ongelezen of recente mail')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--stdin', action='store_true', help='lees mail-summary JSON van stdin, alleen voor nieuwe-mail scope')
    parser.add_argument('--input', help='lees mail-summary JSON uit bestand, alleen voor nieuwe-mail scope')
    parser.add_argument('-n', '--limit', type=int, default=10, help='aantal mails voor unread/recent scopes')
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--unread', action='store_true', help='maak drafts op basis van ongelezen triage-mail')
    scope.add_argument('--all', action='store_true', help='maak drafts op basis van recente mail in plaats van alleen nieuwe mail')
    args = parser.parse_args()

    source = 'summary'
    if args.unread:
        source = 'unread'
    elif args.all:
        source = 'latest'

    result = build_drafts(
        load_messages(
            source=source,
            from_stdin=args.stdin,
            input_path=args.input,
            limit=args.limit,
        )
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))


if __name__ == '__main__':
    main()
