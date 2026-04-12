#!/usr/bin/env python3
import argparse
import json
import time
from pathlib import Path

STATE = Path('/home/clawdy/.openclaw/workspace/state/open-deliverables.json')


def load():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"items": []}


def save(data):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def now():
    return int(time.time())


def cmd_list(args):
    data = load()
    items = data.get('items', [])
    if args.open_only:
        items = [x for x in items if x.get('status') == 'open']
    print(json.dumps({"items": items}, ensure_ascii=False, indent=2))


def cmd_add(args):
    data = load()
    items = data.setdefault('items', [])
    item = {
        "id": f"d{now()}",
        "title": args.title,
        "source": args.source or 'chat',
        "status": 'open',
        "createdAt": now(),
        "updatedAt": now(),
        "notes": args.notes or '',
    }
    items.append(item)
    save(data)
    print(json.dumps(item, ensure_ascii=False, indent=2))


def cmd_resolve(args):
    data = load()
    found = None
    for item in data.get('items', []):
        if item.get('id') == args.id:
            item['status'] = 'resolved'
            item['updatedAt'] = now()
            if args.notes:
                item['notes'] = ((item.get('notes') or '') + '\n' + args.notes).strip()
            found = item
            break
    if not found:
        raise SystemExit(f'unknown id: {args.id}')
    save(data)
    print(json.dumps(found, ensure_ascii=False, indent=2))


def cmd_reopen(args):
    data = load()
    found = None
    for item in data.get('items', []):
        if item.get('id') == args.id:
            item['status'] = 'open'
            item['updatedAt'] = now()
            if args.notes:
                item['notes'] = ((item.get('notes') or '') + '\n' + args.notes).strip()
            found = item
            break
    if not found:
        raise SystemExit(f'unknown id: {args.id}')
    save(data)
    print(json.dumps(found, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description='Track open direct deliverables')
    sub = p.add_subparsers(dest='cmd', required=True)

    p_list = sub.add_parser('list')
    p_list.add_argument('--open-only', action='store_true')
    p_list.set_defaults(func=cmd_list)

    p_add = sub.add_parser('add')
    p_add.add_argument('title')
    p_add.add_argument('--source')
    p_add.add_argument('--notes')
    p_add.set_defaults(func=cmd_add)

    p_res = sub.add_parser('resolve')
    p_res.add_argument('id')
    p_res.add_argument('--notes')
    p_res.set_defaults(func=cmd_resolve)

    p_re = sub.add_parser('reopen')
    p_re.add_argument('id')
    p_re.add_argument('--notes')
    p_re.set_defaults(func=cmd_reopen)

    args = p.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
