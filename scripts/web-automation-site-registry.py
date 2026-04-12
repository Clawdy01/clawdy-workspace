#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from shlex import split as shlex_split
from urllib.parse import urlparse

ROOT = Path('/home/clawdy/.openclaw/workspace')
REGISTRY_PATH = ROOT / 'state' / 'web-automation-sites.json'
DISPATCH = ROOT / 'scripts' / 'web-automation-dispatch.py'

KNOWN_SITES = {
    'account.proton.me': {'adapter': 'proton', 'label': 'Proton signup'},
    'proton.me': {'adapter': 'proton', 'label': 'Proton'},
    'app.slack.com': {'adapter': 'slack', 'label': 'Slack signin'},
    'slack.com': {'adapter': 'slack', 'label': 'Slack'},
    'notion.so': {'adapter': 'notion', 'label': 'Notion'},
    'www.notion.so': {'adapter': 'notion', 'label': 'Notion'},
    'github.com': {'adapter': 'github', 'label': 'GitHub'},
    'bitwarden.com': {'adapter': 'bitwarden', 'label': 'Bitwarden'},
    'vault.bitwarden.com': {'adapter': 'bitwarden', 'label': 'Bitwarden vault'},
    'vault.bitwarden.eu': {'adapter': 'bitwarden', 'label': 'Bitwarden vault'},
}


def read_registry():
    try:
        raw = json.loads(REGISTRY_PATH.read_text())
    except Exception:
        raw = {}
    if isinstance(raw, dict) and isinstance(raw.get('sites'), list):
        items = raw['sites']
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    cleaned = []
    for item in items:
        if isinstance(item, dict):
            cleaned.append(dict(item))
    return cleaned



def write_registry(items):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {'sites': sorted(items, key=lambda item: str(item.get('slug') or '').lower())}
    REGISTRY_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')



def normalize_slug(value):
    value = (value or '').strip().lower()
    value = re.sub(r'[^a-z0-9._-]+', '-', value)
    value = re.sub(r'-{2,}', '-', value).strip('-')
    return value



def normalize_url(value):
    parsed = urlparse((value or '').strip())
    if not parsed.scheme or not parsed.netloc:
        raise SystemExit('URL moet volledig zijn, bijvoorbeeld https://example.com/path')
    path = parsed.path or '/'
    if path != '/':
        path = path.rstrip('/') or '/'
    normalized = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"
    if parsed.query:
        normalized += f'?{parsed.query}'
    if parsed.fragment:
        normalized += f'#{parsed.fragment}'
    return normalized


def normalize_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {'1', 'true', 'yes', 'y', 'on'}:
        return True
    if text in {'0', 'false', 'no', 'n', 'off'}:
        return False
    return default



def detect_site_info(url, slug):
    host = (urlparse(url).netloc or '').lower()
    for known_host, info in KNOWN_SITES.items():
        if host == known_host or host.endswith(f'.{known_host}'):
            return {
                'host': host,
                'adapter': info['adapter'],
                'label': info['label'],
            }
    fallback = (slug or host or 'generic').split('-', 1)[0]
    return {
        'host': host,
        'adapter': fallback,
        'label': host or slug or 'Unknown site',
    }



def load_dispatch_catalog():
    try:
        proc = subprocess.run(
            ['python3', str(DISPATCH), 'catalog', '--json'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
    except subprocess.TimeoutExpired:
        return {'routes': set(), 'aliases': {}, 'available': False, 'error': 'catalog timeout'}
    if proc.returncode != 0:
        return {'routes': set(), 'aliases': {}, 'available': False, 'error': proc.stderr.strip() or proc.stdout.strip() or 'catalog failed'}
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {'routes': set(), 'aliases': {}, 'available': False, 'error': 'invalid catalog json'}
    return {
        'routes': {route.get('name') for route in payload.get('routes') or [] if route.get('name')},
        'aliases': payload.get('aliases') or {},
        'available': True,
        'error': None,
    }


CATALOG = load_dispatch_catalog()


def validate_item(item):
    warnings = []
    slug = normalize_slug(item.get('slug'))
    url = str(item.get('url') or '').strip()
    route = str(item.get('route') or '').strip()
    refresh_command = str(item.get('refreshCommand') or '').strip()

    if not slug:
        warnings.append('mist een geldige slug')
    if url:
        try:
            normalize_url(url)
        except SystemExit as exc:
            warnings.append(str(exc))
    if route:
        if not CATALOG.get('available'):
            warnings.append(f"dispatch catalog niet beschikbaar: {CATALOG.get('error')}")
        elif route not in CATALOG.get('routes', set()) and route not in (CATALOG.get('aliases') or {}):
            warnings.append(f"onbekende dispatch-route: {route}")
    route_args = item.get('routeArgs')
    if route_args is not None and not isinstance(route_args, list):
        warnings.append('routeArgs moet een lijst zijn')
    probe_args = item.get('probeArgs')
    if probe_args is not None and not isinstance(probe_args, list):
        warnings.append('probeArgs moet een lijst zijn')
    desktop_keep_screenshots = item.get('desktopKeepScreenshots')
    desktop_enabled = normalize_bool(item.get('desktopEnabled'), default=desktop_keep_screenshots is not None)
    if desktop_keep_screenshots is not None:
        try:
            desktop_keep_screenshots = int(desktop_keep_screenshots)
        except (TypeError, ValueError):
            warnings.append('desktopKeepScreenshots moet een positief getal zijn')
        else:
            if desktop_keep_screenshots <= 0:
                warnings.append('desktopKeepScreenshots moet een positief getal zijn')
    if desktop_enabled and not url:
        warnings.append('desktopEnabled vereist een URL zodat desktop-probe weet wat geopend moet worden')
    if refresh_command and not refresh_command.strip():
        warnings.append('refreshCommand is leeg')
    if not (url or route or refresh_command):
        warnings.append('geef minstens een URL, --route of --refresh-command op')
    return warnings


def matches_filters(item, *, slugs=None, adapters=None, desktop_only=False, warnings_only=False):
    slugs = {normalize_slug(value) for value in (slugs or []) if normalize_slug(value)}
    adapters = {str(value).strip().lower() for value in (adapters or []) if str(value).strip()}
    slug = normalize_slug(item.get('slug'))
    adapter = str(item.get('adapter') or '').strip().lower()
    desktop_enabled = normalize_bool(item.get('desktopEnabled'), default=item.get('desktopKeepScreenshots') is not None)
    warnings = validate_item(item)

    if slugs and slug not in slugs:
        return False
    if adapters and adapter not in adapters:
        return False
    if desktop_only and not desktop_enabled:
        return False
    if warnings_only and not warnings:
        return False
    return True



def filter_sites(items, *, slugs=None, adapters=None, desktop_only=False, warnings_only=False):
    return [
        item for item in items
        if matches_filters(item, slugs=slugs, adapters=adapters, desktop_only=desktop_only, warnings_only=warnings_only)
    ]



def render_text(items, include_validation=False, *, total_count=None, filters=None):
    if not items:
        suffix = ''
        if total_count not in (None, 0):
            suffix = f' (van {total_count})'
        return f'Web automation site registry: leeg{suffix}'
    count = len(items)
    if total_count not in (None, count):
        lines = [f'Web automation site registry: {count} site(s) (van {total_count})']
    else:
        lines = [f'Web automation site registry: {count} site(s)']
    if filters:
        active_filters = []
        if filters.get('slugs'):
            active_filters.append('slug=' + ','.join(filters['slugs']))
        if filters.get('adapters'):
            active_filters.append('adapter=' + ','.join(filters['adapters']))
        if filters.get('desktop_only'):
            active_filters.append('desktop-only')
        if filters.get('warnings_only'):
            active_filters.append('warnings-only')
        if active_filters:
            lines.append(f"- filters: {' | '.join(active_filters)}")
    for item in items:
        route = item.get('route') or 'probe-page'
        if route == 'probe-page' and item.get('probeArgs'):
            route = f"probe-page {' '.join(str(arg) for arg in item.get('probeArgs') or [])}".strip()
        stale_hint = f", stale-after={item.get('staleAfterSeconds')}s" if item.get('staleAfterSeconds') else ''
        desktop_enabled = normalize_bool(item.get('desktopEnabled'), default=item.get('desktopKeepScreenshots') is not None)
        desktop_bits = []
        if desktop_enabled:
            desktop_bits.append('desktop=aan')
        if item.get('desktopKeepScreenshots'):
            desktop_bits.append(f"keep={item.get('desktopKeepScreenshots')}")
        desktop_hint = f", {' '.join(desktop_bits)}" if desktop_bits else ''
        lines.append(
            f"- {item.get('slug')}: {item.get('label') or '-'} [{item.get('adapter') or '-'}] {item.get('url') or '-'} via {route}{stale_hint}{desktop_hint}"
        )
        if item.get('notes'):
            lines.append(f"  - notes: {item.get('notes')}")
        if include_validation:
            warnings = validate_item(item)
            if warnings:
                lines.append(f"  - warnings: {'; '.join(warnings)}")
    return '\n'.join(lines)



def list_sites(args, json_mode=False):
    all_items = read_registry()
    filtered_items = filter_sites(
        all_items,
        slugs=args.slug,
        adapters=args.adapter,
        desktop_only=args.desktop_only,
        warnings_only=args.warnings_only,
    )
    invalid_sites = [
        {
            'slug': item.get('slug'),
            'warnings': validate_item(item),
        }
        for item in filtered_items
        if validate_item(item)
    ]
    payload = {
        'registry_path': str(REGISTRY_PATH.relative_to(ROOT)),
        'site_count': len(filtered_items),
        'total_site_count': len(all_items),
        'filters': {
            'slugs': args.slug or [],
            'adapters': args.adapter or [],
            'desktop_only': bool(args.desktop_only),
            'warnings_only': bool(args.warnings_only),
        },
        'sites': filtered_items,
        'validation': {
            'catalog_available': CATALOG.get('available', False),
            'catalog_error': CATALOG.get('error'),
            'invalid_site_count': len(invalid_sites),
            'invalid_sites': invalid_sites,
        },
    }
    if json_mode:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(filtered_items, include_validation=True, total_count=len(all_items), filters=payload['filters']))



def upsert_site(args):
    slug = normalize_slug(args.slug)
    if not slug:
        raise SystemExit('slug is verplicht')
    url = normalize_url(args.url) if args.url else ''
    detected = detect_site_info(url, slug) if url else {'host': '', 'adapter': None, 'label': None}

    items = read_registry()
    existing = next((item for item in items if normalize_slug(item.get('slug')) == slug), None)
    route_args = args.route_arg or []
    probe_args = args.probe_arg or []
    record = dict(existing or {})
    record.update({
        'slug': slug,
        'label': args.label or record.get('label') or detected.get('label') or slug,
        'adapter': args.adapter or record.get('adapter') or detected.get('adapter'),
        'url': url or record.get('url') or '',
        'host': detected.get('host') or record.get('host') or '',
        'notes': args.notes if args.notes is not None else record.get('notes', ''),
    })

    if args.route is not None:
        if args.route:
            record['route'] = args.route
        else:
            record.pop('route', None)
    if args.refresh_command is not None:
        if args.refresh_command:
            record['refreshCommand'] = args.refresh_command
        else:
            record.pop('refreshCommand', None)
    if args.route_arg is not None:
        if route_args:
            record['routeArgs'] = route_args
        else:
            record.pop('routeArgs', None)
    if args.probe_arg is not None:
        if probe_args:
            record['probeArgs'] = probe_args
        else:
            record.pop('probeArgs', None)
    if args.stale_after is not None:
        if args.stale_after > 0:
            record['staleAfterSeconds'] = args.stale_after
        else:
            record.pop('staleAfterSeconds', None)
    if args.desktop_keep_screenshots is not None:
        if args.desktop_keep_screenshots > 0:
            record['desktopKeepScreenshots'] = args.desktop_keep_screenshots
        else:
            record.pop('desktopKeepScreenshots', None)
    if getattr(args, 'desktop_enabled', None) is not None:
        if args.desktop_enabled:
            record['desktopEnabled'] = True
        else:
            record.pop('desktopEnabled', None)

    if not (record.get('url') or record.get('route') or record.get('refreshCommand')):
        raise SystemExit('geef minstens een URL, --route of --refresh-command op')

    record = {k: v for k, v in record.items() if v not in (None, '', [])}
    warnings = validate_item(record)

    replaced = False
    updated = []
    for item in items:
        if normalize_slug(item.get('slug')) == slug:
            updated.append(record)
            replaced = True
        else:
            updated.append(item)
    if not replaced:
        updated.append(record)
    write_registry(updated)

    payload = {
        'action': 'updated' if replaced else 'created',
        'site': record,
        'warnings': warnings,
        'registry_path': str(REGISTRY_PATH.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        suffix = f" | warnings: {'; '.join(warnings)}" if warnings else ''
        print(f"{payload['action']}: {record.get('slug')} -> {record.get('url')} ({record.get('route') or 'probe-page'}){suffix}")



def load_sites_board(stale_after=900):
    try:
        proc = subprocess.run(
            ['python3', str(ROOT / 'scripts' / 'web-automation-sites.py'), '--json', '--stale-after', str(stale_after)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit('sites board timeout')
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or 'sites board failed')
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'invalid sites board json: {exc}')



def infer_probe_args_from_command(command, slug):
    if not command:
        return []
    try:
        parts = shlex_split(command)
    except ValueError:
        return []
    try:
        route_idx = parts.index('probe-page')
    except ValueError:
        return []
    args = parts[route_idx + 1 :]
    if not args:
        return []
    trimmed = []
    idx = 0
    while idx < len(args):
        arg = args[idx]
        if idx == 0 and not str(arg).startswith('-'):
            idx += 1
            continue
        if arg == '--slug':
            idx += 2
            continue
        trimmed.append(arg)
        idx += 1
    if '--slug' in trimmed:
        try:
            slug_idx = trimmed.index('--slug')
            if slug_idx + 1 < len(trimmed) and trimmed[slug_idx + 1] == slug:
                del trimmed[slug_idx:slug_idx + 2]
        except ValueError:
            pass
    return trimmed



def promote_site(args):
    slug = normalize_slug(args.slug)
    if not slug:
        raise SystemExit('slug is verplicht')

    board = load_sites_board(stale_after=args.stale_after or 900)
    site = next((item for item in board.get('sites') or [] if normalize_slug(item.get('slug')) == slug), None)
    if not site:
        raise SystemExit(f'geen site-artifact gevonden voor slug: {slug}')

    items = read_registry()
    existing = next((item for item in items if normalize_slug(item.get('slug')) == slug), None)
    record = dict(existing or {})
    route = args.route if args.route is not None else (site.get('route') or record.get('route') or '')
    refresh_command = args.refresh_command if args.refresh_command is not None else (site.get('refresh_command') or record.get('refreshCommand') or '')
    preferred_site_url = site.get('final_url') or site.get('url') or ''
    url = args.url if args.url is not None else (preferred_site_url or record.get('url') or '')
    probe_args = args.probe_arg if args.probe_arg is not None else infer_probe_args_from_command(site.get('refresh_command') or site.get('recommended_command'), slug)
    route_args = args.route_arg or []

    record.update({
        'slug': slug,
        'label': args.label or record.get('label') or site.get('label') or slug,
        'adapter': args.adapter or record.get('adapter') or site.get('adapter'),
        'url': normalize_url(url) if url else '',
        'host': site.get('host') or record.get('host') or '',
        'notes': args.notes if args.notes is not None else record.get('notes', ''),
    })

    if route:
        record['route'] = route
    else:
        record.pop('route', None)
    if refresh_command:
        record['refreshCommand'] = refresh_command
    else:
        record.pop('refreshCommand', None)
    if args.route_arg is not None:
        if route_args:
            record['routeArgs'] = route_args
        else:
            record.pop('routeArgs', None)
    elif record.get('route'):
        record.pop('routeArgs', None)
    if args.probe_arg is not None:
        if probe_args:
            record['probeArgs'] = probe_args
        else:
            record.pop('probeArgs', None)
    elif probe_args and not record.get('route') and not record.get('refreshCommand'):
        record['probeArgs'] = probe_args
    if args.stale_after is not None:
        if args.stale_after > 0:
            record['staleAfterSeconds'] = args.stale_after
        else:
            record.pop('staleAfterSeconds', None)
    if args.desktop_keep_screenshots is not None:
        if args.desktop_keep_screenshots > 0:
            record['desktopKeepScreenshots'] = args.desktop_keep_screenshots
        else:
            record.pop('desktopKeepScreenshots', None)
    if getattr(args, 'desktop_enabled', None) is not None:
        if args.desktop_enabled:
            record['desktopEnabled'] = True
        else:
            record.pop('desktopEnabled', None)

    record = {k: v for k, v in record.items() if v not in (None, '', [])}
    warnings = validate_item(record)

    replaced = False
    updated = []
    for item in items:
        if normalize_slug(item.get('slug')) == slug:
            updated.append(record)
            replaced = True
        else:
            updated.append(item)
    if not replaced:
        updated.append(record)
    write_registry(updated)

    payload = {
        'action': 'updated' if replaced else 'created',
        'source': 'artifact-promote',
        'site': record,
        'warnings': warnings,
        'registry_path': str(REGISTRY_PATH.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        suffix = f" | warnings: {'; '.join(warnings)}" if warnings else ''
        print(f"{payload['action']}: {record.get('slug')} -> {record.get('url')} ({record.get('route') or 'probe-page'}){suffix}")



def remove_site(args):
    slug = normalize_slug(args.slug)
    if not slug:
        raise SystemExit('slug is verplicht')
    items = read_registry()
    kept = [item for item in items if normalize_slug(item.get('slug')) != slug]
    removed = len(kept) != len(items)
    if removed:
        write_registry(kept)
    payload = {
        'action': 'removed' if removed else 'not-found',
        'slug': slug,
        'registry_path': str(REGISTRY_PATH.relative_to(ROOT)),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"{payload['action']}: {slug}")



def add_list_filters(parser):
    parser.add_argument('--slug', action='append', help='filter op slug, herhaalbaar')
    parser.add_argument('--adapter', action='append', help='filter op adapter, herhaalbaar')
    parser.add_argument('--desktop-only', action='store_true', help='toon alleen sites met beheerde desktop fallback')
    parser.add_argument('--warnings-only', action='store_true', help='toon alleen sites met validatie-waarschuwingen')



def main():
    parser = argparse.ArgumentParser(description='Beheer registry-items voor web automation sites')
    parser.add_argument('--json', action='store_true')
    sub = parser.add_subparsers(dest='command')

    list_parser = sub.add_parser('list', help='toon registry-sites')
    add_list_filters(list_parser)

    upsert = sub.add_parser('upsert', help='maak of update een registry-site')
    upsert.add_argument('--slug', required=True)
    upsert.add_argument('--url', help='volledige URL voor generieke probe of als observability-doel')
    upsert.add_argument('--label')
    upsert.add_argument('--adapter')
    upsert.add_argument('--route', help='dispatch route voor refresh, bijvoorbeeld proton-refresh')
    upsert.add_argument('--route-arg', action='append', help='extra route-arg, herhaalbaar')
    upsert.add_argument('--probe-arg', action='append', help='extra generic probe-page arg, herhaalbaar, bijvoorbeeld --probe-arg=--session --probe-arg=slack-shared')
    upsert.add_argument('--refresh-command', dest='refresh_command', help='expliciet refresh-commando, overschrijft route')
    upsert.add_argument('--stale-after', type=int, help='optionele site-specifieke stale-drempel in seconden, 0 wist de override')
    upsert.add_argument('--desktop-keep-screenshots', type=int, dest='desktop_keep_screenshots', help='optioneel aantal genummerde desktop screenshots om per target te bewaren, 0 wist de override')
    upsert.add_argument('--desktop-enabled', dest='desktop_enabled', action='store_true', default=None, help='markeer deze site als beheerd desktop fallback target')
    upsert.add_argument('--desktop-disabled', dest='desktop_enabled', action='store_false', help='verwijder beheerde desktop fallback intent voor deze site')
    upsert.add_argument('--notes', help='korte notities voor de site')

    promote = sub.add_parser('promote', help='promoveer een bestaand site-artifact naar de registry')
    promote.add_argument('--slug', required=True)
    promote.add_argument('--url', help='optionele override voor de opgeslagen URL')
    promote.add_argument('--label')
    promote.add_argument('--adapter')
    promote.add_argument('--route', help='optionele dispatch route override')
    promote.add_argument('--route-arg', action='append', help='extra route-arg, herhaalbaar')
    promote.add_argument('--probe-arg', action='append', help='extra generic probe-page arg, herhaalbaar')
    promote.add_argument('--refresh-command', dest='refresh_command', help='expliciet refresh-commando, overschrijft route')
    promote.add_argument('--stale-after', type=int, help='optionele stale-drempel in seconden, 0 wist de override')
    promote.add_argument('--desktop-keep-screenshots', type=int, dest='desktop_keep_screenshots', help='optioneel aantal genummerde desktop screenshots om per target te bewaren, 0 wist de override')
    promote.add_argument('--desktop-enabled', dest='desktop_enabled', action='store_true', default=None, help='markeer deze site als beheerd desktop fallback target')
    promote.add_argument('--desktop-disabled', dest='desktop_enabled', action='store_false', help='verwijder beheerde desktop fallback intent voor deze site')
    promote.add_argument('--notes', help='korte notities voor de site')

    remove = sub.add_parser('remove', help='verwijder een registry-site op slug')
    remove.add_argument('--slug', required=True)

    validate = sub.add_parser('validate', help='valideer registry-sites en dispatch-routes')
    add_list_filters(validate)

    args = parser.parse_args()
    if not args.command:
        args.command = 'list'
        args.slug = []
        args.adapter = []
        args.desktop_only = False
        args.warnings_only = False

    try:
        if args.command == 'list':
            list_sites(args, json_mode=args.json)
        elif args.command == 'upsert':
            upsert_site(args)
        elif args.command == 'promote':
            promote_site(args)
        elif args.command == 'remove':
            remove_site(args)
        elif args.command == 'validate':
            list_sites(args, json_mode=args.json)
        else:
            raise SystemExit(f'Onbekend commando: {args.command}')
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
