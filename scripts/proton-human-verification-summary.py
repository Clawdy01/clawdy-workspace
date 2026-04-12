#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
DATA = ROOT / 'browser-automation' / 'out' / 'proton-human-verification.json'


def load_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def build_summary():
    data = load_json(DATA, {}) or {}
    initial = data.get('initial') or {}
    final = data.get('final') or {}
    return {
        'checked_at': data.get('checkedAt'),
        'verification_screen': final.get('verificationScreen', initial.get('verificationScreen')),
        'dialog_text': final.get('dialogText') or initial.get('dialogText'),
        'input_labels': [row.get('label') or row.get('placeholder') or row.get('name') or row.get('id') for row in (final.get('inputs') or initial.get('inputs') or [])],
        'button_texts': [row.get('text') for row in (final.get('buttons') or initial.get('buttons') or []) if row.get('text')],
        'email_sent': bool(data.get('emailAction')),
        'code_attempted': bool(data.get('codeAction')),
        'screenshot': data.get('screenshot'),
    }


def render_text(summary):
    lines = ['Proton human verification']
    lines.append(f"- screen={summary.get('verification_screen')}, checked_at={summary.get('checked_at')}")
    lines.append(f"- inputs={', '.join(summary.get('input_labels') or []) or 'geen'}")
    lines.append(f"- buttons={', '.join(summary.get('button_texts') or []) or 'geen'}")
    lines.append(f"- email_sent={summary.get('email_sent')}, code_attempted={summary.get('code_attempted')}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte samenvatting van Proton human verification probe')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    summary = build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
