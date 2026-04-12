#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
DELIVERABLES = ROOT / 'state' / 'open-deliverables.json'
ART_DIR = ROOT / 'art'
TELEGRAM_HELPER = ROOT / 'scripts' / 'send-telegram-file.js'
TARGET_CHAT_ID = '16584407'


def load_json(path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def main():
    deliverables = load_json(DELIVERABLES, {'items': []})
    current = next((x for x in deliverables.get('items', []) if x.get('id') == 'd-current-images'), None)
    art_refs = sorted(p.name for p in ART_DIR.glob('clawdy-computermeisje*'))
    summary = {
        'deliverable_open': bool(current and current.get('status') == 'open'),
        'deliverable_title': (current or {}).get('title'),
        'telegram_helper_ready': TELEGRAM_HELPER.exists(),
        'telegram_chat_id': TARGET_CHAT_ID,
        'reference_art_count': len(art_refs),
        'reference_art': art_refs,
        'verified_image_write_route': False,
        'known_blocker': 'geen geverifieerde write-capable image-generation route beschikbaar in deze runtime',
        'next_step': 'koppel een echte beeldroute met write-rechten; genereer daarna PNG output en stuur die via send-telegram-file.js naar chat 16584407',
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
