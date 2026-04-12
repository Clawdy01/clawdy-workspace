#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
INVENTORY = ROOT / 'TOOLING_INVENTORY.md'


def parse_inventory():
    sections = {}
    current = None
    for raw_line in INVENTORY.read_text().splitlines():
        line = raw_line.rstrip()
        if line.startswith('## '):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current and line.startswith('- '):
            sections[current].append(line[2:].strip())
    return sections


def filter_sections(sections, section_filter=None):
    if not section_filter:
        return sections
    needle = section_filter.lower()
    filtered = {}
    for name, items in sections.items():
        if needle in name.lower():
            filtered[name] = items
            continue
        matching_items = [item for item in items if needle in item.lower()]
        if matching_items:
            filtered[name] = matching_items
    return filtered


def render_text(sections, limit=4):
    lines = ['Toolsboard']
    for section, items in sections.items():
        if not items:
            continue
        preview = '; '.join(items[:limit])
        if len(items) > limit:
            preview += f' (+{len(items) - limit})'
        lines.append(f'- {section}: {preview}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compact toolsboard uit TOOLING_INVENTORY.md')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--section', help='toon alleen secties die deze tekst bevatten')
    parser.add_argument('--limit', type=int, default=4, help='aantal items per sectie in tekstoutput')
    args = parser.parse_args()

    sections = filter_sections(parse_inventory(), args.section)
    if args.json:
        print(json.dumps(sections, ensure_ascii=False, indent=2))
    else:
        print(render_text(sections, limit=max(1, args.limit)))


if __name__ == '__main__':
    main()
