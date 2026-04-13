#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from workspace_secrets import SECRET_ALIASES, SECRETS, load_secrets


def build_plan(secrets):
    actions = []
    conflicts = []
    updated = dict(secrets)

    for canonical, aliases in SECRET_ALIASES.items():
        present = [name for name in (canonical, *aliases) if name in secrets]
        if not present:
            continue

        canonical_present = canonical in secrets
        canonical_value = secrets.get(canonical)
        alias_values = {alias: secrets[alias] for alias in aliases if alias in secrets}

        if canonical_present:
            for alias, value in alias_values.items():
                if value != canonical_value:
                    conflicts.append({
                        'canonical': canonical,
                        'alias': alias,
                        'reason': 'canonical-and-alias-differ',
                    })
                else:
                    actions.append({
                        'action': 'remove_alias',
                        'canonical': canonical,
                        'alias': alias,
                    })
                    updated.pop(alias, None)
            continue

        if alias_values:
            source_alias, source_value = next(iter(alias_values.items()))
            distinct_values = {value for value in alias_values.values()}
            if len(distinct_values) > 1:
                conflicts.append({
                    'canonical': canonical,
                    'aliases': sorted(alias_values.keys()),
                    'reason': 'aliases-differ',
                })
                continue

            updated[canonical] = source_value
            actions.append({
                'action': 'set_canonical',
                'canonical': canonical,
                'from': source_alias,
            })
            for alias in alias_values:
                actions.append({
                    'action': 'remove_alias',
                    'canonical': canonical,
                    'alias': alias,
                })
                updated.pop(alias, None)

    return updated, actions, conflicts


def emit_text(path, actions, conflicts, apply_mode):
    mode = 'apply' if apply_mode else 'dry-run'
    print(f'{mode}: {path}')
    if conflicts:
        print(f'conflicts: {len(conflicts)}')
        for item in conflicts:
            if 'alias' in item:
                print(f"- conflict {item['canonical']} vs {item['alias']}: {item['reason']}")
            else:
                aliases = ', '.join(item['aliases'])
                print(f"- conflict {item['canonical']} via [{aliases}]: {item['reason']}")
    else:
        print('conflicts: 0')

    if actions:
        print(f'actions: {len(actions)}')
        for item in actions:
            if item['action'] == 'set_canonical':
                print(f"- set {item['canonical']} from {item['from']}")
            else:
                print(f"- remove alias {item['alias']} (canonical {item['canonical']})")
    else:
        print('actions: 0')


def main():
    parser = argparse.ArgumentParser(description='Normalize secrets.json keys to canonical names.')
    parser.add_argument('--apply', action='store_true', help='Write canonicalized secrets.json back to disk.')
    parser.add_argument('--json', action='store_true', help='Emit machine-readable JSON summary.')
    args = parser.parse_args()

    path = Path(SECRETS)
    secrets = load_secrets()
    updated, actions, conflicts = build_plan(secrets)

    if args.apply and conflicts:
        payload = {
            'ok': False,
            'applied': False,
            'path': str(path),
            'actions': actions,
            'conflicts': conflicts,
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            emit_text(path, actions, conflicts, apply_mode=True)
        return 2

    applied = False
    if args.apply and updated != secrets:
        path.write_text(json.dumps(updated, indent=2, sort_keys=True) + '\n')
        applied = True

    payload = {
        'ok': not conflicts,
        'applied': applied,
        'path': str(path),
        'actions': actions,
        'conflicts': conflicts,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        emit_text(path, actions, conflicts, apply_mode=args.apply)
    return 0 if not conflicts else 2


if __name__ == '__main__':
    raise SystemExit(main())
